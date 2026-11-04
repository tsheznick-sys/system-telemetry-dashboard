import csv
import io
import unittest

from fastapi.testclient import TestClient

from app import APP_VERSION, app, collector


class TelemetryApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.client = TestClient(app)
        cls.client.__enter__()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.client.__exit__(None, None, None)

    def setUp(self) -> None:
        with collector._lock:
            collector._history.clear()

    def test_health_reports_api_version(self) -> None:
        response = self.client.get("/api/v1/health")

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

    def test_dashboard_redirects_to_gradio(self) -> None:
        response = self.client.get("/", follow_redirects=False)

        self.assertEqual(response.status_code, 307)
        self.assertEqual(response.headers["location"], "/dashboard")

    def test_dashboard_is_served(self) -> None:
        response = self.client.get("/dashboard/")

        self.assertEqual(response.status_code, 200)
        self.assertIn("Telemetry Dashboard 2.0", response.text)


if __name__ == "__main__":
    unittest.main()
