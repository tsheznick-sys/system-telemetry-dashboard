import asyncio
import csv
import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from fastapi.testclient import TestClient

import app as app_module
from app import (
    APP_VERSION,
    TelemetrySnapshot,
    app,
    demo,
    get_telemetry,
    TelemetryCollector,
    _render_dashboard,
)


class TelemetryApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.temp_directory = tempfile.TemporaryDirectory()
        cls.collector = TelemetryCollector(
            Path(cls.temp_directory.name) / "api-tests.sqlite3"
        )
        app_module.collector = cls.collector
        cls.client = TestClient(app)
        cls.client.__enter__()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.client.__exit__(None, None, None)
        cls.temp_directory.cleanup()

    def setUp(self) -> None:
        self.collector.clear_history()

    def test_health_reports_api_version(self) -> None:
        response = self.client.get("/api/v1/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok", "version": APP_VERSION})

    def test_ssr_proxy_api_alias_reports_health(self) -> None:
        response = self.client.get("/gradio_api/api/v1/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok", "version": APP_VERSION})

    def test_live_metrics_include_host_and_resource_data(self) -> None:
        response = self.client.get("/api/v1/metrics")

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["mode"], "live")
        self.assertTrue(payload["host"]["hostname"])
        self.assertGreaterEqual(payload["cpu_percent"], 0)
        self.assertLessEqual(payload["cpu_percent"], 100)
        self.assertGreater(payload["memory_total_bytes"], 0)
        self.assertGreater(payload["disk_total_bytes"], 0)
        self.assertIsNone(payload["error_rate_percent"])

    def test_simulated_metrics_and_filtered_history(self) -> None:
        self.client.get("/api/v1/metrics?mode=live")
        simulated = self.client.get("/api/v1/metrics?mode=simulated")
        history = self.client.get("/api/v1/history?mode=simulated&limit=1")

        self.assertEqual(simulated.status_code, 200)
        self.assertEqual(simulated.json()["mode"], "simulated")
        self.assertIsNotNone(simulated.json()["error_rate_percent"])
        self.assertEqual(len(history.json()), 1)
        self.assertEqual(history.json()[0]["mode"], "simulated")

    def test_rejects_unknown_mode_and_out_of_range_history_limit(self) -> None:
        self.assertEqual(self.client.get("/api/v1/metrics?mode=other").status_code, 422)
        self.assertEqual(self.client.get("/api/v1/history?limit=0").status_code, 422)
        self.assertEqual(self.client.get("/api/v1/history?limit=601").status_code, 422)

    def test_flutter_web_origin_passes_cors_preflight(self) -> None:
        response = self.client.options(
            "/api/v1/metrics",
            headers={
                "Origin": "http://localhost:8080",
                "Access-Control-Request-Method": "GET",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.headers["access-control-allow-origin"], "http://localhost:8080"
        )

    def test_csv_export_uses_documented_columns(self) -> None:
        self.client.get("/api/v1/metrics?mode=simulated")

        response = self.client.get("/api/v1/export.csv?mode=simulated")
        rows = list(csv.DictReader(io.StringIO(response.text)))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["content-type"], "text/csv; charset=utf-8")
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["mode"], "simulated")
        self.assertIn("cpu_percent", rows[0])

    def test_openapi_documents_versioned_telemetry_routes(self) -> None:
        response = self.client.get("/gradio_api/api/v1/openapi.json")

        self.assertEqual(response.status_code, 200)
        paths = response.json()["paths"]
        self.assertIn("/gradio_api/api/v1/health", paths)
        self.assertIn("/gradio_api/api/v1/metrics", paths)
        self.assertIn("/gradio_api/api/v1/history", paths)
        self.assertIn("/gradio_api/api/v1/export.csv", paths)

    def test_dashboard_config_uses_timer_and_plotly_component(self) -> None:
        config = demo.get_config_file()
        component_types = {
            component["type"] for component in config["components"]
        }

        self.assertIn("timer", component_types)
        self.assertIn("plot", component_types)
        self.assertEqual(demo.title, "Ghost Telemetry Engine v4.0")

    def test_async_dashboard_callback_streams_plot_and_metrics(self) -> None:
        async def first_update():
            stream = get_telemetry(
                "simulated", 30, 80, 80, "Simulated Incident"
            )
            return await anext(stream)

        cpu, memory, connections, error_rate, summary, chart, events = asyncio.run(
            first_update()
        )

        self.assertGreaterEqual(cpu, 90)
        self.assertGreaterEqual(memory, 85)
        self.assertIsNotNone(connections)
        self.assertGreaterEqual(error_rate, 8)
        self.assertIn("Simulated telemetry", summary)
        self.assertEqual(len(chart.data), 2)
        self.assertTrue(events)

    def test_dashboard_thresholds_control_alerts_and_event_severity(self) -> None:
        sample = self.collector.snapshot("simulated")
        sample = sample.model_copy(
            update={
                "cpu_percent": 70.0,
                "memory_percent": 72.0,
                "disk_percent": 20.0,
                "error_rate_percent": 4.0,
                "alerts": [],
                "events": ["INFO: simulated sample"],
            }
        )
        with (
            patch.object(self.collector, "snapshot", return_value=sample),
            patch.object(self.collector, "history", return_value=[sample]),
        ):
            *_, summary, chart, events = _render_dashboard(
                "simulated", 20, 60, 65, "Normal Operations"
            )

        self.assertIn("threshold 60%", summary)
        self.assertIn("threshold 65%", summary)
        self.assertIn("CRITICAL:", events)
        self.assertIn("CPU usage is high", events)
        self.assertEqual(len(chart.data), 2)

    def test_history_persists_across_collector_restarts(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            database_path = Path(directory) / "persistent-history.sqlite3"
            first_process = TelemetryCollector(database_path)
            saved_sample = first_process.snapshot("simulated")

            restarted_process = TelemetryCollector(database_path)
            restored = restarted_process.history("simulated", 10)

        self.assertEqual(len(restored), 1)
        self.assertEqual(restored[0].timestamp, saved_sample.timestamp)
        self.assertEqual(restored[0].mode, saved_sample.mode)

    def test_persistent_history_is_bounded(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            database_path = Path(directory) / "bounded-history.sqlite3"
            bounded_collector = TelemetryCollector(database_path)
            with patch.object(app_module, "PERSISTED_HISTORY_CAPACITY", 2):
                samples = [
                    bounded_collector.snapshot("simulated") for _ in range(3)
                ]

            restarted_process = TelemetryCollector(database_path)
            restored = restarted_process.history("simulated", 10)

        self.assertEqual(len(restored), 2)
        self.assertEqual(
            [sample.timestamp for sample in restored],
            [sample.timestamp for sample in samples[-2:]],
        )


if __name__ == "__main__":
    unittest.main()
