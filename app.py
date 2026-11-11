from __future__ import annotations

import asyncio
import csv
import io
import json
import os
import platform
import random
import sqlite3
import socket
import threading
import time
from contextlib import closing
from datetime import datetime, timezone
from pathlib import Path
from typing import AsyncIterator, Literal

import gradio as gr
import psutil
import plotly.graph_objects as go
from fastapi import HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse
from gradio.routes import App as GradioApp
from pydantic import BaseModel, Field

from calculator import calculate, format_result
from research_agent_cluster import MAX_TARGETS, ResearchSynthesizerOrchestrator

APP_VERSION = "4.0.0"
HISTORY_CAPACITY = 600
PERSISTED_HISTORY_CAPACITY = 10_000
TelemetryMode = Literal["live", "simulated"]
OperationalState = Literal[
    "Normal Operations", "Load Test", "Simulated Incident"
]


class HostInfo(BaseModel):
    hostname: str
    platform: str
    processor: str


class TelemetrySnapshot(BaseModel):
    timestamp: str
    mode: TelemetryMode
    host: HostInfo
    cpu_percent: float
    memory_percent: float
    memory_used_bytes: int
    memory_total_bytes: int
    disk_percent: float
    disk_used_bytes: int
    disk_total_bytes: int
    network_sent_bytes: int
    network_recv_bytes: int
    network_sent_bytes_per_sec: float
    network_recv_bytes_per_sec: float
    active_connections: int | None
    connections_available: bool
    connections_note: str | None
    process_count: int
    uptime_seconds: float
    load_average_1m: float | None
    error_rate_percent: float | None
    alerts: list[str]
    events: list[str]


class CalculatorExpression(BaseModel):
    expression: str = Field(min_length=1, max_length=256)


class ResearchRequest(BaseModel):
    query: str = Field(min_length=1, max_length=1000)
    urls: list[str] = Field(min_length=1, max_length=MAX_TARGETS)


def _host_info() -> HostInfo:
    return HostInfo(
        hostname=socket.gethostname(),
        platform=platform.platform(),
        processor=platform.processor() or "Not reported by operating system",
    )


def _alerts_for(cpu: float, memory: float, disk: float) -> list[str]:
    alerts = []
    if cpu >= 85:
        alerts.append(f"CPU usage is high at {cpu:.1f}%.")
    if memory >= 85:
        alerts.append(f"Memory usage is high at {memory:.1f}%.")
    if disk >= 90:
        alerts.append(f"Disk usage is high at {disk:.1f}%.")
    return alerts


class TelemetryCollector:
    def __init__(self, history_db_path: str | Path | None = None) -> None:
        default_path = (
            Path.home()
            / ".local"
            / "share"
            / "ghost-telemetry"
            / "telemetry.sqlite3"
        )
        configured_path = history_db_path or os.getenv(
            "TELEMETRY_DB_PATH", str(default_path)
        )
        self.history_db_path = Path(configured_path).expanduser()
        self._history_lock = threading.Lock()
        self._network_lock = threading.Lock()
        self._random = random.Random()
        self._last_network: tuple[float, int, int] | None = None
        self._initialize_history()

    def _connect(self) -> sqlite3.Connection:
        self.history_db_path.parent.mkdir(parents=True, exist_ok=True)
        connection = sqlite3.connect(self.history_db_path, timeout=5)
        connection.row_factory = sqlite3.Row
        return connection

    def _initialize_history(self) -> None:
        with closing(self._connect()) as connection, connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS telemetry_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    mode TEXT NOT NULL CHECK (mode IN ('live', 'simulated')),
                    payload TEXT NOT NULL
                )
                """
            )
            connection.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_telemetry_history_mode_id
                ON telemetry_history (mode, id DESC)
                """
            )
            connection.execute("PRAGMA journal_mode = WAL")
            connection.execute("PRAGMA synchronous = NORMAL")

    def _record(self, sample: TelemetrySnapshot) -> None:
        with closing(self._connect()) as connection, connection:
            connection.execute(
                """
                INSERT INTO telemetry_history (timestamp, mode, payload)
                VALUES (?, ?, ?)
                """,
                (sample.timestamp, sample.mode, sample.model_dump_json()),
            )
            connection.execute(
                """
                DELETE FROM telemetry_history
                WHERE id NOT IN (
                    SELECT id FROM telemetry_history
                    ORDER BY id DESC
                    LIMIT ?
                )
                """,
                (PERSISTED_HISTORY_CAPACITY,),
            )

    def snapshot(
        self,
        mode: TelemetryMode = "live",
        operational_state: OperationalState = "Normal Operations",
    ) -> TelemetrySnapshot:
        if mode == "simulated":
            with self._history_lock:
                sample = self._simulated_snapshot(operational_state)
                self._record(sample)
                return sample

        sample = self._live_snapshot()
        with self._history_lock:
            self._record(sample)
        return sample

    def history(self, mode: TelemetryMode, limit: int) -> list[TelemetrySnapshot]:
        with self._history_lock:
            with closing(self._connect()) as connection:
                rows = connection.execute(
                    """
                    SELECT payload FROM telemetry_history
                    WHERE mode = ?
                    ORDER BY id DESC
                    LIMIT ?
                    """,
                    (mode, min(max(limit, 1), HISTORY_CAPACITY)),
                ).fetchall()
        return [
            TelemetrySnapshot.model_validate_json(row["payload"])
            for row in reversed(rows)
        ]

    def clear_history(self) -> None:
        with self._history_lock:
            with closing(self._connect()) as connection, connection:
                connection.execute("DELETE FROM telemetry_history")

    def _network_rates(self, sent_bytes: int, recv_bytes: int) -> tuple[float, float]:
        now = time.monotonic()
        with self._network_lock:
            previous = self._last_network
            self._last_network = (now, sent_bytes, recv_bytes)
        if previous is None:
            return 0.0, 0.0

        previous_time, previous_sent, previous_recv = previous
        elapsed = now - previous_time
        if elapsed <= 0:
            return 0.0, 0.0
        sent_rate = max(0, sent_bytes - previous_sent) / elapsed
        recv_rate = max(0, recv_bytes - previous_recv) / elapsed
        return sent_rate, recv_rate

    def _live_snapshot(self) -> TelemetrySnapshot:
        memory = psutil.virtual_memory()
        disk_root = Path.home().anchor or "/"
        disk = psutil.disk_usage(disk_root)
        network = psutil.net_io_counters()
        if network is None:
            raise RuntimeError("The operating system did not provide network counters.")

        sent_rate, recv_rate = self._network_rates(
            network.bytes_sent, network.bytes_recv
        )

        active_connections: int | None
        connections_available = True
        connections_note = None
        try:
            connections = psutil.net_connections(kind="inet")
            active_connections = sum(
                connection.status == psutil.CONN_ESTABLISHED
                for connection in connections
            )
        except (psutil.Error, NotImplementedError, OSError):
            active_connections = None
            connections_available = False
            connections_note = (
                "Connection count unavailable due to platform or permission limits."
            )

        try:
            load_average = os.getloadavg()[0]
        except (AttributeError, OSError):
            load_average = None

        cpu = psutil.cpu_percent(interval=None)
        memory_percent = memory.percent
        disk_percent = disk.percent
        alerts = _alerts_for(cpu, memory_percent, disk_percent)
        events = [f"ALERT: {alert}" for alert in alerts]
        if not events:
            events.append("INFO: Host telemetry collected successfully.")
        if connections_note:
            events.append(f"WARN: {connections_note}")

        return TelemetrySnapshot(
            timestamp=datetime.now(timezone.utc).isoformat(),
            mode="live",
            host=_host_info(),
            cpu_percent=cpu,
            memory_percent=memory_percent,
            memory_used_bytes=memory.used,
            memory_total_bytes=memory.total,
            disk_percent=disk_percent,
            disk_used_bytes=disk.used,
            disk_total_bytes=disk.total,
            network_sent_bytes=network.bytes_sent,
            network_recv_bytes=network.bytes_recv,
            network_sent_bytes_per_sec=sent_rate,
            network_recv_bytes_per_sec=recv_rate,
            active_connections=active_connections,
            connections_available=connections_available,
            connections_note=connections_note,
            process_count=len(psutil.pids()),
            uptime_seconds=max(0.0, time.time() - psutil.boot_time()),
            load_average_1m=load_average,
            error_rate_percent=None,
            alerts=alerts,
            events=events,
        )

    def _simulated_snapshot(
        self, operational_state: OperationalState
    ) -> TelemetrySnapshot:
        ranges = {
            "Normal Operations": ((10.0, 65.0), (25.0, 60.0), (0.0, 0.8)),
            "Load Test": ((75.0, 99.9), (80.0, 98.0), (1.5, 4.5)),
            "Simulated Incident": ((90.0, 100.0), (85.0, 99.0), (8.0, 15.0)),
        }
        cpu_range, memory_range, error_range = ranges[operational_state]
        cpu = round(self._random.uniform(*cpu_range), 1)
        memory = round(self._random.uniform(*memory_range), 1)
        disk = round(self._random.uniform(22.0, 92.0), 1)
        alerts = _alerts_for(cpu, memory, disk)
        events = [
            f"INFO: Simulation profile: {operational_state}.",
            f"{self._random.choice(['INFO', 'WARN', 'SUCCESS'])}: "
            f"{self._random.choice(['Service health check passed', 'Worker pool scaled', 'Cache refreshed', 'Request latency nominal'])}.",
        ]
        events.extend(f"ALERT: {alert}" for alert in alerts)
        memory_total = 16 * 1024**3
        disk_total = 512 * 1024**3
        return TelemetrySnapshot(
            timestamp=datetime.now(timezone.utc).isoformat(),
            mode="simulated",
            host=_host_info(),
            cpu_percent=cpu,
            memory_percent=memory,
            memory_used_bytes=int(memory_total * memory / 100),
            memory_total_bytes=memory_total,
            disk_percent=disk,
            disk_used_bytes=int(disk_total * disk / 100),
            disk_total_bytes=disk_total,
            network_sent_bytes=self._random.randint(1_000_000, 900_000_000),
            network_recv_bytes=self._random.randint(1_000_000, 900_000_000),
            network_sent_bytes_per_sec=round(
                self._random.uniform(0, 1_000_000), 1
            ),
            network_recv_bytes_per_sec=round(
                self._random.uniform(0, 1_000_000), 1
            ),
            active_connections=self._random.randint(10, 250),
            connections_available=True,
            connections_note=None,
            process_count=self._random.randint(80, 320),
            uptime_seconds=round(self._random.uniform(1_000, 1_000_000), 1),
            load_average_1m=round(self._random.uniform(0.1, 8.0), 2),
            error_rate_percent=round(self._random.uniform(*error_range), 2),
            alerts=alerts,
            events=events,
        )


collector = TelemetryCollector()
app = GradioApp(
    title="Ghost Telemetry API",
    description="Persistent live host and simulated telemetry for Ghost Telemetry Engine.",
    version=APP_VERSION,
)

cors_origins = [
    origin.strip()
    for origin in os.getenv(
        "TELEMETRY_CORS_ORIGINS",
        "http://localhost:8080,http://127.0.0.1:8080,"
        "http://localhost:3000,http://127.0.0.1:3000",
    ).split(",")
    if origin.strip()
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_methods=["GET", "POST"],
    allow_headers=["Accept", "Content-Type"],
    max_age=600,
)


@app.get("/api/v1/health", include_in_schema=False)
def health() -> dict[str, str]:
    return {"status": "ok", "version": APP_VERSION}


@app.get("/calculator", include_in_schema=False)
def calculator_page() -> FileResponse:
    return FileResponse(Path(__file__).with_name("calculator.html"))


@app.post("/api/v1/calculate", include_in_schema=False)
def calculate_expression(
    request: CalculatorExpression,
) -> dict[str, int | float | str]:
    try:
        value = calculate(request.expression)
    except (
        SyntaxError,
        TypeError,
        ValueError,
        OverflowError,
        ZeroDivisionError,
    ) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"value": value, "result": format_result(value)}


async def execute_research(query: str, urls: list[str]) -> dict[str, object]:
    output_dir = Path(
        os.getenv(
            "RESEARCH_OUTPUT_DIR",
            str(Path.home() / ".local" / "share" / "ghost-telemetry" / "research"),
        )
    )
    orchestrator = ResearchSynthesizerOrchestrator(output_dir=output_dir)
    return await orchestrator.execute_research_pipeline(query, urls)


@app.post("/api/v1/research")
async def run_research(request: ResearchRequest) -> dict[str, object]:
    try:
        return await execute_research(request.query, request.urls)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


app.add_api_route(
    "/gradio_api/calculator",
    calculator_page,
    methods=["GET"],
    include_in_schema=False,
)
app.add_api_route(
    "/gradio_api/api/v1/calculate",
    calculate_expression,
    methods=["POST"],
    include_in_schema=False,
)
app.add_api_route(
    "/gradio_api/api/v1/research",
    run_research,
    methods=["POST"],
    include_in_schema=False,
)


@app.get(
    "/api/v1/metrics",
    response_model=TelemetrySnapshot,
    include_in_schema=False,
)
def get_metrics(mode: TelemetryMode = "live") -> TelemetrySnapshot:
    return collector.snapshot(mode)


@app.get(
    "/api/v1/history",
    response_model=list[TelemetrySnapshot],
    include_in_schema=False,
)
def get_history(
    mode: TelemetryMode = "live",
    limit: int = Query(default=120, ge=1, le=HISTORY_CAPACITY),
) -> list[TelemetrySnapshot]:
    return collector.history(mode, limit)


@app.get("/api/v1/export.csv", include_in_schema=False)
def export_csv(
    mode: TelemetryMode = "live",
    limit: int = Query(default=120, ge=1, le=HISTORY_CAPACITY),
) -> StreamingResponse:
    fields = [
        "timestamp",
        "mode",
        "cpu_percent",
        "memory_percent",
        "disk_percent",
        "network_sent_bytes_per_sec",
        "network_recv_bytes_per_sec",
        "active_connections",
        "process_count",
        "uptime_seconds",
        "error_rate_percent",
    ]
    output = io.StringIO(newline="")
    writer = csv.DictWriter(output, fieldnames=fields)
    writer.writeheader()
    writer.writerows(
        sample.model_dump(include=set(fields))
        for sample in collector.history(mode, limit)
    )
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={
            "Content-Disposition": f'attachment; filename="telemetry-{mode}.csv"'
        },
    )


@app.get("/api/v1/openapi.json", include_in_schema=False)
def telemetry_openapi() -> dict[str, object]:
    return app.openapi()


app.add_api_route(
    "/gradio_api/api/v1/health",
    health,
    methods=["GET"],
)
app.add_api_route(
    "/gradio_api/api/v1/metrics",
    get_metrics,
    methods=["GET"],
    response_model=TelemetrySnapshot,
)
app.add_api_route(
    "/gradio_api/api/v1/history",
    get_history,
    methods=["GET"],
    response_model=list[TelemetrySnapshot],
)
app.add_api_route(
    "/gradio_api/api/v1/export.csv",
    export_csv,
    methods=["GET"],
)
app.add_api_route(
    "/gradio_api/api/v1/openapi.json",
    telemetry_openapi,
    methods=["GET"],
    response_class=JSONResponse,
)


def _format_bytes(value: int) -> str:
    size = float(value)
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if size < 1024 or unit == "TB":
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} TB"


def _render_dashboard(
    mode: TelemetryMode,
    history_limit: int,
    cpu_threshold: int = 80,
    memory_threshold: int = 80,
    operational_state: OperationalState = "Normal Operations",
) -> tuple[float, float, int | None, float | None, str, go.Figure, str]:
    current = collector.snapshot(mode, operational_state)
    history = collector.history(mode, history_limit)
    dashboard_alerts = []
    if current.cpu_percent >= cpu_threshold:
        dashboard_alerts.append(
            f"CPU usage is high at {current.cpu_percent:.1f}% "
            f"(threshold {cpu_threshold}%)."
        )
    if current.memory_percent >= memory_threshold:
        dashboard_alerts.append(
            f"Memory usage is high at {current.memory_percent:.1f}% "
            f"(threshold {memory_threshold}%)."
        )
    if current.disk_percent >= 90:
        dashboard_alerts.append(
            f"Disk usage is high at {current.disk_percent:.1f}%."
        )

    chart = go.Figure()
    for label, color, value_getter in (
        ("CPU Load (%)", "#00F2FF", lambda sample: sample.cpu_percent),
        ("Memory Usage (%)", "#FF0055", lambda sample: sample.memory_percent),
    ):
        chart.add_trace(
            go.Scatter(
                x=[sample.timestamp[11:19] for sample in history],
                y=[value_getter(sample) for sample in history],
                mode="lines+markers",
                name=label,
                line={"color": color, "width": 2.4},
                marker={"size": 5, "opacity": 0.9},
                fill="tozeroy",
                fillcolor="rgba(0, 242, 255, 0.07)" if label.startswith("CPU") else "rgba(255, 0, 85, 0.07)",
                hovertemplate="%{x} · " + label + " %{y:.1f}%<extra></extra>",
            )
        )
    chart.update_layout(
        template="plotly_dark",
        margin={"l": 24, "r": 16, "t": 34, "b": 24},
        height=340,
        hovermode="x unified",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"family": "Inter, ui-sans-serif, system-ui, sans-serif", "color": "#c6d3e2", "size": 12},
        xaxis={
            "showgrid": False,
            "title": {"text": "Sample time", "font": {"size": 11, "color": "#8b9bb0"}},
            "zeroline": False,
            "showspikes": True,
            "spikethickness": 1,
            "spikecolor": "rgba(148, 184, 220, 0.35)",
        },
        yaxis={
            "range": [0, 100],
            "gridcolor": "rgba(148, 184, 220, 0.10)",
            "zeroline": False,
            "title": {"text": "Utilization (%)", "font": {"size": 11, "color": "#8b9bb0"}},
            "ticksuffix": "%",
        },
        legend={
            "orientation": "h",
            "y": 1.18,
            "x": 0,
            "bgcolor": "rgba(0,0,0,0)",
            "font": {"size": 11, "color": "#aab8c8"},
        },
    )
    connection_text = (
        str(current.active_connections)
        if current.connections_available
        else "Unavailable"
    )
    load_text = (
        f"{current.load_average_1m:.2f}"
        if current.load_average_1m is not None
        else "Unavailable"
    )
    error_text = (
        f"{current.error_rate_percent:.2f}%"
        if current.error_rate_percent is not None
        else "Not instrumented"
    )
    alerts = (
        "\n".join(f"- **Alert:** {alert}" for alert in dashboard_alerts)
        if dashboard_alerts
        else "All monitored thresholds are clear."
    )
    profile_note = (
        f"**Simulation profile:** {operational_state}"
        if mode == "simulated"
        else (
            f"**Simulation profile:** {operational_state} "
            "(not applied to live host metrics)"
        )
    )
    summary = f"""
### {current.host.hostname} · {current.mode.title()} telemetry

{profile_note} · **Alert thresholds:** CPU {cpu_threshold}% / Memory {memory_threshold}%

| CPU | Memory | Disk | Active connections |
|---:|---:|---:|---:|
| **{current.cpu_percent:.1f}%** | **{current.memory_percent:.1f}%** · {_format_bytes(current.memory_used_bytes)} | **{current.disk_percent:.1f}%** · {_format_bytes(current.disk_used_bytes)} | **{connection_text}** |

| Network sent / sec | Network received / sec | Processes | Load average (1m) | Error rate |
|---:|---:|---:|---:|---:|
| {_format_bytes(int(current.network_sent_bytes_per_sec))}/s | {_format_bytes(int(current.network_recv_bytes_per_sec))}/s | {current.process_count} | {load_text} | {error_text} |

**Uptime:** {current.uptime_seconds / 3600:.1f} hours · **Platform:** {current.host.platform} · **Updated:** {current.timestamp}

### Health alerts
{alerts}
"""
    events_list = list(current.events)
    if mode == "live" and operational_state != "Normal Operations":
        events_list.insert(
            0,
            f"INFO: {operational_state} is a simulation-only profile; live host metrics are unchanged.",
        )
    log_level = (
        "CRITICAL"
        if current.error_rate_percent is not None
        and current.error_rate_percent > 3.0
        else "WARN"
        if dashboard_alerts
        else "INFO"
    )
    events_list.insert(
        0,
        f"{log_level}: NODE_{random.randint(100, 999)} telemetry sample collected.",
    )
    events_list.append(
        "METRIC: "
        f"CPU {current.cpu_percent:.1f}% | RAM {current.memory_percent:.1f}% | "
        f"ERR {current.error_rate_percent:.2f}%"
        if current.error_rate_percent is not None
        else (
            f"METRIC: CPU {current.cpu_percent:.1f}% | "
            f"RAM {current.memory_percent:.1f}% | ERR not instrumented"
        )
    )
    if dashboard_alerts:
        events_list = [
            event for event in events_list if not event.startswith("ALERT:")
        ]
        events_list.extend(f"ALERT: {alert}" for alert in dashboard_alerts)
    events = "\n".join(
        f"[{current.timestamp[11:19]}] {event}" for event in reversed(events_list)
    )
    return (
        current.cpu_percent,
        current.memory_percent,
        current.active_connections,
        current.error_rate_percent,
        summary,
        chart,
        events,
    )


async def get_telemetry(
    mode: TelemetryMode,
    history_limit: int,
    cpu_threshold: int,
    memory_threshold: int,
    operational_state: OperationalState,
) -> AsyncIterator[tuple[float, float, int | None, float | None, str, go.Figure, str]]:
    await asyncio.sleep(0)
    yield await asyncio.to_thread(
        _render_dashboard,
        mode,
        history_limit,
        cpu_threshold,
        memory_threshold,
        operational_state,
    )


async def run_research_from_dashboard(
    query: str, urls_text: str
) -> str:
    urls = [line.strip() for line in urls_text.splitlines() if line.strip()]
    if not query.strip():
        raise gr.Error("Enter a research question.")
    if not 1 <= len(urls) <= MAX_TARGETS:
        raise gr.Error(f"Provide between 1 and {MAX_TARGETS} HTTPS URLs.")
    try:
        result = await execute_research(query, urls)
    except ValueError as exc:
        raise gr.Error(str(exc)) from exc
    return str(result["dossier"])


def update_refresh_interval(seconds: int) -> float:
    return float(seconds)


with gr.Blocks(title="Ghost Telemetry Engine v4.0") as demo:
    gr.HTML(
        """
        <div class="gh-topbar">
          <div class="gh-brand">
            <div class="gh-mark" aria-hidden="true">⚡</div>
            <div class="gh-titles">
              <div class="gh-title">GHOST TELEMETRY <span>/ 4.0</span></div>
              <div class="gh-sub">Live host diagnostics · Durable history · Operational simulation profiles</div>
            </div>
          </div>
          <div class="gh-actions">
            <span class="gh-pill"><span class="gh-dot"></span>LIVE</span>
            <a class="gh-link" href="/gradio_api/calculator">Calculator →</a>
            <a class="gh-link" href="/api/v1/openapi.json">API →</a>
          </div>
        </div>
        """
    )
    with gr.Row():
        with gr.Column(scale=1, elem_classes=["control-panel"]):
            gr.Markdown("### 🎛️ Operational Controls")
            mode_selector = gr.Radio(
                choices=[("Live Host", "live"), ("Simulated", "simulated")],
                value="live",
                label="Telemetry source",
            )
            operational_state = gr.Radio(
                choices=[
                    "Normal Operations",
                    "Load Test",
                    "Simulated Incident",
                ],
                value="Normal Operations",
                label="Simulation profile",
                info="Profiles affect simulated telemetry only.",
            )
            cpu_alert_limit = gr.Slider(
                minimum=50,
                maximum=95,
                value=80,
                step=5,
                label="CPU warning threshold (%)",
            )
            memory_alert_limit = gr.Slider(
                minimum=50,
                maximum=95,
                value=80,
                step=5,
                label="Memory warning threshold (%)",
            )
            history_selector = gr.Dropdown(
                choices=[20, 30, 60, 120],
                value=20,
                label="Chart history points",
            )
            refresh_interval = gr.Dropdown(
                choices=[2, 5, 10, 15, 30],
                value=2,
                label="Refresh interval (seconds)",
            )
            refresh_button = gr.Button(
                "Trigger Diagnostic Sweep", variant="primary"
            )
        with gr.Column(scale=3, elem_classes=["telemetry-panel"]):
            gr.Markdown("### 📊 Live Performance Telemetry")
            with gr.Row():
                cpu_box = gr.Number(label="CPU Core Load (%)", interactive=False)
                mem_box = gr.Number(label="RAM Allocation (%)", interactive=False)
                conn_box = gr.Number(label="Active Sockets", interactive=False)
                err_box = gr.Number(label="Error Rate (%)", interactive=False)
            summary_output = gr.Markdown()
            telemetry_plot = gr.Plot(label="Real-Time Metrics Stream")
    events_output = gr.Textbox(
        label="System Console Event Stream",
        lines=6,
        interactive=False,
        max_lines=10,
    )
    refresh_timer = gr.Timer(2)
    outputs = [
        cpu_box,
        mem_box,
        conn_box,
        err_box,
        summary_output,
        telemetry_plot,
        events_output,
    ]
    inputs = [
        mode_selector,
        history_selector,
        cpu_alert_limit,
        memory_alert_limit,
        operational_state,
    ]
    refresh_timer.tick(get_telemetry, inputs=inputs, outputs=outputs)
    refresh_button.click(get_telemetry, inputs=inputs, outputs=outputs)
    for control in (
        mode_selector,
        history_selector,
        cpu_alert_limit,
        memory_alert_limit,
        operational_state,
    ):
        control.change(get_telemetry, inputs=inputs, outputs=outputs)
    refresh_interval.change(
        update_refresh_interval,
        inputs=refresh_interval,
        outputs=refresh_timer,
        queue=False,
    )
    demo.load(get_telemetry, inputs=inputs, outputs=outputs)
    gr.HTML(
        """
        <div class="gh-footer">
          Ghost Telemetry Engine v4.0 · self-hosted diagnostics ·
          <a href="/gradio_api/calculator">Calculator</a> ·
          <a href="/api/v1/openapi.json">OpenAPI schema</a> ·
          seeded, self-verifying simulations in <code>modules/</code> + <code>advanced_modules/</code>
        </div>
        """
    )
    with gr.Accordion("Public Web Research", open=False):
        gr.Markdown(
            "Fetch up to five public HTTPS pages. Requests are limited to public "
            "IP addresses and 1 MB per page. Ranking uses lexical similarity; "
            "no LLM is used."
        )
        research_query = gr.Textbox(
            label="Research question",
            placeholder="What are the main findings across these sources?",
            max_lines=3,
        )
        research_urls = gr.Textbox(
            label="Public HTTPS URLs (one per line)",
            placeholder="https://example.org/research",
            lines=4,
        )
        research_button = gr.Button("Research sources", variant="primary")
        research_output = gr.Markdown()
        research_button.click(
            run_research_from_dashboard,
            inputs=[research_query, research_urls],
            outputs=research_output,
        )


custom_css = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;650;700&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --gh-bg: #05080d;
    --gh-panel: rgba(13, 19, 29, 0.86);
    --gh-panel-solid: #0d131d;
    --gh-panel-raised: #111927;
    --gh-border: rgba(148, 184, 220, 0.14);
    --gh-border-strong: rgba(148, 184, 220, 0.24);
    --gh-text: #e6edf6;
    --gh-muted: #8b9bb0;
    --gh-accent: #22d3ee;
    --gh-accent-strong: #06b6d4;
    --gh-accent-deep: #0891b2;
    --gh-ok: #34d399;
    --gh-warn: #ffb45c;
    --gh-danger: #ff5c7a;
    --gh-gold: #c9a227;
    --gh-radius: 16px;
    --gh-radius-sm: 12px;
    --gh-shadow: 0 24px 64px rgba(0, 0, 0, 0.35);
    --gh-mono: 'JetBrains Mono', ui-monospace, monospace;
}

*:focus-visible {
    outline: 2px solid var(--gh-accent) !important;
    outline-offset: 2px !important;
    border-radius: 6px;
}

body, .gradio-container {
    background:
        radial-gradient(1100px 520px at 12% -10%, rgba(34, 211, 238, 0.10), transparent 60%),
        radial-gradient(900px 520px at 105% 110%, rgba(8, 145, 178, 0.12), transparent 55%),
        var(--gh-bg) !important;
    color: var(--gh-text) !important;
    font-family: 'Inter', ui-sans-serif, system-ui, sans-serif !important;
}
.gradio-container {
    max-width: 1480px !important;
    margin: 0 auto !important;
    padding: 18px 26px 44px !important;
}

/* ---------- Brand header ---------- */
.gh-topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 18px;
    padding: 14px 20px;
    border: 1px solid var(--gh-border);
    border-radius: var(--gh-radius);
    background: linear-gradient(180deg, rgba(17, 25, 39, 0.9), rgba(13, 19, 29, 0.9));
    box-shadow: var(--gh-shadow);
    backdrop-filter: blur(14px);
    margin-bottom: 18px;
}
.gh-brand { display: flex; align-items: center; gap: 14px; min-width: 0; }
.gh-mark {
    display: grid;
    width: 46px; height: 46px;
    place-items: center;
    border-radius: 14px;
    font-size: 24px;
    color: #06121a;
    background: linear-gradient(135deg, #67e8f9 0%, #22d3ee 45%, #0891b2 100%);
    box-shadow: 0 8px 26px rgba(34, 211, 238, 0.35), inset 0 1px 0 rgba(255, 255, 255, 0.5);
}
.gh-title {
    font-size: clamp(19px, 2.3vw, 26px);
    font-weight: 700;
    letter-spacing: -0.02em;
    color: #f2f7fd;
    white-space: nowrap;
}
.gh-title span { color: var(--gh-accent); font-weight: 650; }
.gh-sub { color: var(--gh-muted); font-size: 12.5px; margin-top: 2px; }
.gh-actions { display: flex; align-items: center; gap: 10px; flex-wrap: wrap; justify-content: flex-end; }
.gh-pill {
    display: inline-flex; align-items: center; gap: 8px;
    padding: 7px 14px;
    border-radius: 999px;
    font-size: 11px; font-weight: 700; letter-spacing: 0.14em;
    color: #052019;
    background: linear-gradient(180deg, #4ade9c, #22c55e);
    box-shadow: 0 0 18px rgba(52, 211, 153, 0.4);
}
.gh-dot { width: 8px; height: 8px; border-radius: 50%; background: #052e1c; animation: gh-pulse 1.6s ease-in-out infinite; }
@keyframes gh-pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.35; } }
.gh-link {
    display: inline-flex; align-items: center; gap: 6px;
    padding: 8px 14px;
    border: 1px solid var(--gh-border-strong);
    border-radius: 999px;
    color: #cfe3f5; text-decoration: none;
    font-size: 12.5px; font-weight: 600;
    transition: border-color 160ms ease, color 160ms ease, background 160ms ease;
}
.gh-link:hover { border-color: var(--gh-accent); color: #ffffff; background: rgba(34, 211, 238, 0.08); }
.gh-footer {
    margin-top: 20px;
    padding: 14px 6px 0;
    border-top: 1px solid var(--gh-border);
    color: var(--gh-muted);
    font-size: 12px;
    text-align: center;
}
.gh-footer a { color: #9adfef; text-decoration: none; }
.gh-footer a:hover { text-decoration: underline; }

/* ---------- Panels ---------- */
.control-panel, .telemetry-panel {
    border: 1px solid var(--gh-border) !important;
    background: var(--gh-panel) !important;
    padding: 18px !important;
    border-radius: var(--gh-radius) !important;
    box-shadow: var(--gh-shadow);
    backdrop-filter: blur(14px);
}
.control-panel h3, .telemetry-panel h3 {
    margin-top: 0 !important;
    font-size: 15px !important;
    font-weight: 650 !important;
    letter-spacing: 0.01em;
    color: #eaf2fb !important;
    border-bottom: 1px solid var(--gh-border);
    padding-bottom: 10px;
}

/* ---------- KPI number boxes ---------- */
.gradio-number input, input[type='number'] {
    font-variant-numeric: tabular-nums !important;
    font-family: var(--gh-mono) !important;
    font-size: 22px !important;
    font-weight: 500 !important;
    letter-spacing: -0.02em !important;
    color: #f0f6fd !important;
    background: var(--gh-panel-raised) !important;
    border: 1px solid var(--gh-border) !important;
    border-radius: var(--gh-radius-sm) !important;
}
.gradio-number label span, .gradio-slider label span, .gradio-radio label span {
    color: var(--gh-muted) !important;
    font-size: 11px !important;
    font-weight: 650 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
}

/* ---------- Sliders & radios ---------- */
input[type='range'] { accent-color: var(--gh-accent-strong); }
.gradio-radio fieldset, .gradio-dropdown, .gradio-textbox {
    border-radius: var(--gh-radius-sm) !important;
}
.gradio-radio label { transition: border-color 150ms ease, background 150ms ease; border-radius: 10px !important; }
.gradio-radio label:hover { background: rgba(34, 211, 238, 0.06); }

/* ---------- Buttons ---------- */
button.primary, button.gr-button-primary {
    background: linear-gradient(135deg, #67e8f9 0%, #22d3ee 45%, #0891b2 100%) !important;
    border: 0 !important;
    color: #05131c !important;
    font-weight: 700 !important;
    letter-spacing: 0.02em !important;
    border-radius: var(--gh-radius-sm) !important;
    box-shadow: 0 10px 30px rgba(34, 211, 238, 0.28), inset 0 1px 0 rgba(255, 255, 255, 0.55) !important;
    transition: transform 140ms ease, box-shadow 140ms ease, filter 140ms ease !important;
}
button.primary:hover { transform: translateY(-1px); filter: brightness(1.05); box-shadow: 0 14px 36px rgba(34, 211, 238, 0.36), inset 0 1px 0 rgba(255,255,255,0.55) !important; }
button.primary:active { transform: translateY(0); }

/* ---------- Markdown / prose (summary) ---------- */
.gradio-markdown, .prose { color: var(--gh-text) !important; }
.gradio-markdown h1, .prose h1 {
    font-size: 22px !important; letter-spacing: -0.02em;
    background: linear-gradient(90deg, #f2f7fd, #9adcff);
    -webkit-background-clip: text; background-clip: text; color: transparent !important;
}
.gradio-markdown h3, .prose h3 { color: #d7e6f5 !important; border-bottom: 1px solid var(--gh-border); padding-bottom: 6px; }
.gradio-markdown table, .prose table {
    border-collapse: collapse;
    width: 100%;
    margin: 10px 0 14px;
    border: 1px solid var(--gh-border);
    border-radius: var(--gh-radius-sm);
    overflow: hidden;
    font-variant-numeric: tabular-nums;
}
.gradio-markdown th, .prose th {
    background: rgba(34, 211, 238, 0.08) !important;
    color: #a9ecfb !important;
    font-size: 10.5px !important;
    text-transform: uppercase; letter-spacing: 0.09em;
    padding: 8px 10px !important;
    border-bottom: 1px solid var(--gh-border-strong) !important;
    text-align: left !important;
}
.gradio-markdown td, .prose td {
    padding: 8px 10px !important;
    border-bottom: 1px solid rgba(148, 184, 220, 0.08) !important;
}
.gradio-markdown tr:nth-child(even) td, .prose tr:nth-child(even) td { background: rgba(255, 255, 255, 0.02); }
.gradio-markdown code, .prose code {
    background: rgba(34, 211, 238, 0.09) !important;
    color: #8be9ff !important;
    border-radius: 6px;
    padding: 1px 6px;
    font-family: var(--gh-mono) !important;
    font-size: 0.86em;
}
.gradio-markdown strong, .prose strong { color: #ffffff !important; }

/* ---------- Plot & console ---------- */
.gradio-plot, .gradio-plot > div { border-radius: var(--gh-radius-sm) !important; overflow: hidden; }
textarea, .gradio-textbox textarea {
    font-family: var(--gh-mono) !important;
    font-size: 12.5px !important;
    line-height: 1.55 !important;
    background: #070c14 !important;
    border: 1px solid var(--gh-border) !important;
    border-radius: var(--gh-radius-sm) !important;
    color: #b9f3ff !important;
}

/* ---------- Scrollbars ---------- */
::-webkit-scrollbar { width: 10px; height: 10px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(148, 184, 220, 0.22); border-radius: 8px; }
::-webkit-scrollbar-thumb:hover { background: rgba(148, 184, 220, 0.36); }

/* ---------- Reduced motion ---------- */
@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after { animation-duration: 0.01ms !important; animation-iteration-count: 1 !important; transition-duration: 0.01ms !important; }
}
"""


if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        ssr_mode=True,
        _app=app,
        theme=gr.themes.Base(primary_hue="cyan", neutral_hue="slate", font=["Inter", "ui-sans-serif", "system-ui", "sans-serif"], font_mono=["JetBrains Mono", "ui-monospace", "monospace"]),
        css=custom_css,
        footer_links=["api", "gradio"],
    )
