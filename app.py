from __future__ import annotations

import csv
import io
import os
import platform
import random
import socket
import threading
import time
from collections import deque
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal

import gradio as gr
import pandas as pd
import psutil
import uvicorn
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, StreamingResponse
from pydantic import BaseModel

APP_VERSION = "2.0.0"
HISTORY_CAPACITY = 600
TelemetryMode = Literal["live", "simulated"]


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
    def __init__(self) -> None:
        self._history: deque[TelemetrySnapshot] = deque(maxlen=HISTORY_CAPACITY)
        self._lock = threading.Lock()
        self._random = random.Random()
        self._last_network: tuple[float, int, int] | None = None

    def snapshot(self, mode: TelemetryMode = "live") -> TelemetrySnapshot:
        with self._lock:
            if mode == "simulated":
                sample = self._simulated_snapshot()
            else:
                sample = self._live_snapshot()
            self._history.append(sample)
            return sample

    def history(self, mode: TelemetryMode, limit: int) -> list[TelemetrySnapshot]:
        with self._lock:
            matching = [sample for sample in self._history if sample.mode == mode]
            return matching[-limit:]

    def _live_snapshot(self) -> TelemetrySnapshot:
        memory = psutil.virtual_memory()
        disk_root = Path.home().anchor or "/"
        disk = psutil.disk_usage(disk_root)
        network = psutil.net_io_counters()
        if network is None:
            raise RuntimeError("The operating system did not provide network counters.")

        now = time.monotonic()
        sent_rate = 0.0
        recv_rate = 0.0
        if self._last_network is not None:
            previous_time, previous_sent, previous_recv = self._last_network
            elapsed = now - previous_time
            if elapsed > 0:
                sent_rate = max(0, network.bytes_sent - previous_sent) / elapsed
                recv_rate = max(0, network.bytes_recv - previous_recv) / elapsed
        self._last_network = (now, network.bytes_sent, network.bytes_recv)

        active_connections: int | None
        connections_available = True
        connections_note = None
        try:
            connections = psutil.net_connections(kind="inet")
            active_connections = sum(
                connection.status == psutil.CONN_ESTABLISHED
                for connection in connections
            )
        except (psutil.AccessDenied, NotImplementedError, OSError) as exc:
            active_connections = None
            connections_available = False
            connections_note = f"Connection count unavailable: {exc}"

        try:
            load_average = os.getloadavg()[0]
        except (AttributeError, OSError):
            load_average = None

        cpu = psutil.cpu_percent(interval=None)
        memory_percent = memory.percent
        disk_percent = disk.percent
        alerts = _alerts_for(cpu, memory_percent, disk_percent)
        events = [f"{'ALERT' if alerts else 'INFO'}: {alert}" for alert in alerts]
        if not events:
            events.append("INFO: Host telemetry collected successfully.")
        if connections_note:
            events.append(f"WARN: {connections_note}")

        boot_time = psutil.boot_time()
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
            uptime_seconds=max(0.0, time.time() - boot_time),
            load_average_1m=load_average,
            error_rate_percent=None,
            alerts=alerts,
            events=events,
        )

    def _simulated_snapshot(self) -> TelemetrySnapshot:
        cpu = round(self._random.uniform(8.0, 96.0), 1)
        memory = round(self._random.uniform(28.0, 94.0), 1)
        disk = round(self._random.uniform(22.0, 92.0), 1)
        alerts = _alerts_for(cpu, memory, disk)
        events = [
            f"{self._random.choice(['INFO', 'WARN', 'SUCCESS'])}: "
            f"{self._random.choice(['Service health check passed', 'Worker pool scaled', 'Cache refreshed', 'Request latency nominal'])}."
            for _ in range(3)
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
            network_sent_bytes_per_sec=round(self._random.uniform(0, 1_000_000), 1),
            network_recv_bytes_per_sec=round(self._random.uniform(0, 1_000_000), 1),
            active_connections=self._random.randint(10, 250),
            connections_available=True,
            connections_note=None,
            process_count=self._random.randint(80, 320),
            uptime_seconds=round(self._random.uniform(1_000, 1_000_000), 1),
            load_average_1m=round(self._random.uniform(0.1, 8.0), 2),
            error_rate_percent=round(self._random.uniform(0, 1.5), 2),
            alerts=alerts,
            events=events,
        )


collector = TelemetryCollector()
app = FastAPI(
    title="System Telemetry API",
    description="Live host and simulated telemetry for Telemetry Dashboard 2.0.",
    version=APP_VERSION,
)

cors_origins = [
    origin.strip()
    for origin in os.getenv(
        "TELEMETRY_CORS_ORIGINS",
        "http://localhost:8080,http://127.0.0.1:8080,http://localhost:3000,http://127.0.0.1:3000",
    ).split(",")
    if origin.strip()
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/api/v1/health")
def health() -> dict[str, str]:
    return {"status": "ok", "version": APP_VERSION}


@app.get("/api/v1/metrics", response_model=TelemetrySnapshot)
def get_metrics(mode: TelemetryMode = "live") -> TelemetrySnapshot:
    return collector.snapshot(mode)


@app.get("/api/v1/history", response_model=list[TelemetrySnapshot])
def get_history(
    mode: TelemetryMode = "live",
    limit: int = Query(default=120, ge=1, le=HISTORY_CAPACITY),
) -> list[TelemetrySnapshot]:
    return collector.history(mode, limit)


@app.get("/api/v1/export.csv")
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
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=fields)
    writer.writeheader()
    writer.writerows(
        sample.model_dump(include=set(fields))
        for sample in collector.history(mode, limit)
    )
    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="telemetry-{mode}.csv"'},
    )


@app.get("/", include_in_schema=False)
def index() -> RedirectResponse:
    return RedirectResponse("/dashboard")


def _format_bytes(value: int) -> str:
    size = float(value)
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if size < 1024 or unit == "TB":
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} TB"


def _render_dashboard(
    mode: TelemetryMode, history_limit: int
) -> tuple[str, pd.DataFrame, str]:
    current = collector.snapshot(mode)
    history = collector.history(mode, history_limit)
    points = [
        {"timestamp": sample.timestamp, "metric": label, "value": value}
        for sample in history
        for label, value in (
            ("CPU", sample.cpu_percent),
            ("Memory", sample.memory_percent),
            ("Disk", sample.disk_percent),
        )
    ]
    chart = pd.DataFrame(points, columns=["timestamp", "metric", "value"])
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
        "\n".join(f"- **Alert:** {alert}" for alert in current.alerts)
        if current.alerts
        else "All monitored thresholds are clear."
    )
    summary = f"""
### {current.host.hostname} · {current.mode.title()} telemetry

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
    events = "\n".join(
        f"[{current.timestamp[11:19]}] {event}" for event in reversed(current.events)
    )
    return summary, chart, events


with gr.Blocks(
    title="Telemetry Dashboard 2.0",
) as dashboard:
    gr.Markdown(
        """
        # SYSTEM TELEMETRY <span style="color:#22d3ee">/ 2.0</span>
        Live host visibility, historical trends, and actionable health signals.
        """
    )
    with gr.Row():
        mode_selector = gr.Dropdown(
            choices=[("Live host", "live"), ("Simulated demo", "simulated")],
            value="live",
            label="Telemetry source",
        )
        history_selector = gr.Dropdown(
            choices=[30, 60, 120, 300],
            value=120,
            label="History points",
        )
        refresh_interval = gr.Dropdown(
            choices=[2, 5, 10, 15, 30],
            value=5,
            label="Refresh interval (seconds)",
        )
        refresh_button = gr.Button("Refresh now", variant="primary")
    summary_output = gr.Markdown()
    trend_chart = gr.LinePlot(
        x="timestamp",
        y="value",
        color="metric",
        title="Resource utilization history",
        y_lim=[0, 100],
        height=320,
        buttons=["fullscreen", "export"],
    )
    events_output = gr.Textbox(
        label="Latest events",
        lines=6,
        max_lines=10,
        interactive=False,
    )
    refresh_timer = gr.Timer(value=5)
    outputs = [summary_output, trend_chart, events_output]
    inputs = [mode_selector, history_selector]
    refresh_timer.tick(_render_dashboard, inputs=inputs, outputs=outputs)
    refresh_button.click(_render_dashboard, inputs=inputs, outputs=outputs)
    mode_selector.change(_render_dashboard, inputs=inputs, outputs=outputs)
    history_selector.change(_render_dashboard, inputs=inputs, outputs=outputs)
    refresh_interval.change(
        lambda seconds: seconds,
        inputs=refresh_interval,
        outputs=refresh_timer,
        queue=False,
    )
    dashboard.load(_render_dashboard, inputs=inputs, outputs=outputs)


app = gr.mount_gradio_app(
    app,
    dashboard,
    path="/dashboard",
    theme=gr.themes.Soft(
        primary_hue="cyan", secondary_hue="blue", neutral_hue="slate"
    ),
)


if __name__ == "__main__":
    uvicorn.run(
        app,
        host=os.getenv("TELEMETRY_HOST", "127.0.0.1"),
        port=int(os.getenv("TELEMETRY_PORT", "7860")),
    )
