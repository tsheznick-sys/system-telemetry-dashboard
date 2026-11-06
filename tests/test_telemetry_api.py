import asyncio
import csv
import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from fastapi.testclient import TestClient

import app as app_module
import calculator_server as calculator_server_module
from app import (
    APP_VERSION,
    TelemetrySnapshot,
    app,
    demo,
    get_telemetry,
    TelemetryCollector,
    _render_dashboard,
)


class CalculatorServerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(calculator_server_module.app)

    def test_standalone_page_and_api_are_available(self) -> None:
        page = self.client.get("/")
        result = self.client.post(
            "/api/v1/calculate",
            json={"expression": "sqrt(9) + 1"},
        )

        self.assertEqual(page.status_code, 200)
        self.assertIn("Calculator · Ghost Telemetry", page.text)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.json(), {"value": 4, "result": "4"})

    def test_standalone_service_does_not_expose_telemetry_routes(self) -> None:
        response = self.client.get("/api/v1/metrics")

        self.assertEqual(response.status_code, 404)

    def test_standalone_calculator_rejects_bad_expressions(self) -> None:
        response = self.client.post(
            "/api/v1/calculate",
            json={"expression": "1 / 0"},
        )

        self.assertEqual(response.status_code, 400)


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

    def test_calculator_page_is_served(self) -> None:
        for path in ("/calculator", "/gradio_api/calculator"):
            with self.subTest(path=path):
                response = self.client.get(path)

                self.assertEqual(response.status_code, 200)
                self.assertIn("text/html", response.headers["content-type"])
                self.assertIn("Calculator · Ghost Telemetry", response.text)
                self.assertIn("A focused scientific calculator", response.text)

    def test_calculator_api_evaluates_safe_expressions(self) -> None:
        for path in ("/api/v1/calculate", "/gradio_api/api/v1/calculate"):
            with self.subTest(path=path):
                response = self.client.post(
                    path,
                    json={"expression": "sqrt(9) + 1"},
                )

                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.json(), {"value": 4, "result": "4"})

    def test_calculator_api_rejects_invalid_and_expensive_expressions(self) -> None:
        invalid = self.client.post(
            "/api/v1/calculate",
            json={"expression": "1 / 0"},
        )
        expensive = self.client.post(
            "/api/v1/calculate",
            json={"expression": "2 ** 1000"},
        )
        xor = self.client.post(
            "/api/v1/calculate",
            json={"expression": "2 ^ 3"},
        )
        pow_call = self.client.post(
            "/api/v1/calculate",
            json={"expression": "pow(2, 3, 4)"},
        )

        self.assertEqual(invalid.status_code, 400)
        self.assertEqual(expensive.status_code, 400)
        self.assertEqual(xor.status_code, 400)
        self.assertEqual(pow_call.status_code, 400)

    def test_research_api_returns_dossier_and_source_results(self) -> None:
        async def fake_research(_query: str, _urls: list[str]) -> dict[str, object]:
            return {
                "query": "test query",
                "results": [{"url": "https://example.org", "status": "SUCCESS"}],
                "matches": [],
                "dossier": "# Research report",
                "elapsed_seconds": 0.1,
                "output_files": {"dossier": "/tmp/report.md", "csv": "/tmp/report.csv"},
            }

        with patch.object(app_module, "execute_research", side_effect=fake_research):
            for path in ("/api/v1/research", "/gradio_api/api/v1/research"):
                with self.subTest(path=path):
                    response = self.client.post(
                        path,
                        json={
                            "query": "test query",
                            "urls": ["https://example.org/research"],
                        },
                    )

                    self.assertEqual(response.status_code, 200)
                    self.assertEqual(response.json()["dossier"], "# Research report")
                    self.assertEqual(
                        response.json()["results"][0]["status"], "SUCCESS"
                    )

    def test_research_api_limits_number_of_targets(self) -> None:
        response = self.client.post(
            "/api/v1/research",
            json={
                "query": "test query",
                "urls": [f"https://example.org/{index}" for index in range(6)],
            },
        )

        self.assertEqual(response.status_code, 422)

    def test_research_scraper_rejects_private_addresses(self) -> None:
        from research_agent_cluster import ResearchScraperAgent

        agent = ResearchScraperAgent()
        with self.assertRaises(ValueError):
            asyncio.run(agent._validated_url("https://127.0.0.1/"))

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
        self.assertIn("/api/v1/research", paths)

    def test_dashboard_config_uses_timer_and_plotly_component(self) -> None:
        config = demo.get_config_file()
        component_types = {
            component["type"] for component in config["components"]
        }

        self.assertIn("timer", component_types)
        self.assertIn("plot", component_types)
        self.assertIn("accordion", component_types)
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
