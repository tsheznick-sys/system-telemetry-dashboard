# Ghost Telemetry Engine 4.0

Telemetry 4.0 combines a Python host monitor and Gradio 6 dashboard with a
Flutter client for Android, iOS, and web. Both interfaces use the same versioned
JSON API. Live measurements describe the machine running the Python service;
the simulated mode is available for demos and UI checks.

## Run the Python service

Python 3.10 or later is recommended.

```sh
python -m pip install -r requirements.txt
python app.py
```

Open [http://127.0.0.1:7860](http://127.0.0.1:7860). The service listens on
`0.0.0.0:7860` for container and Codespaces port forwarding. Keep the forwarded
port private; the API does not provide authentication or TLS.

Configuration:

| Environment variable | Default | Description |
| --- | --- | --- |
| `TELEMETRY_CORS_ORIGINS` | `http://localhost:8080,http://127.0.0.1:8080,http://localhost:3000,http://127.0.0.1:3000` | Comma-separated browser origins allowed to call the API. Use the exact Flutter web origin. |
| `TELEMETRY_DB_PATH` | `~/.local/share/ghost-telemetry/telemetry.sqlite3` | SQLite database path used for durable telemetry history. Parent directories are created automatically. |

The app binds to all container interfaces to support forwarded ports. Its API
has **no authentication or TLS**. Do not expose it publicly or to an untrusted
network; keep the Codespaces port private or use an authenticated TLS-terminating
gateway before allowing untrusted clients.

## API

The telemetry API's OpenAPI schema is available at
`/gradio_api/api/v1/openapi.json`.

| Method and path | Description |
| --- | --- |
| `GET /gradio_api/api/v1/health` | Service version and health. |
| `GET /gradio_api/api/v1/metrics?mode=live` | Collect and return a current host sample. |
| `GET /gradio_api/api/v1/metrics?mode=simulated` | Generate a demo sample. |
| `GET /gradio_api/api/v1/history?mode=live&limit=120` | Return recent persisted samples for one mode. `limit` is 1–600. |
| `GET /gradio_api/api/v1/export.csv?mode=live&limit=120` | Download recent samples as CSV. |

Each metrics response includes an ISO-8601 UTC timestamp, mode, host identity,
CPU, memory, disk, network throughput and totals, process count, uptime, load
average when supported, threshold alerts, and events. Live error rate is
`null`: the host service does not instrument application requests. Active
connection counts can also be `null` on operating systems or permission levels
that do not allow enumerating sockets; the response includes an availability
flag and an explanation. History is written to SQLite and survives service
restarts. The database retains the latest 10,000 samples across both telemetry
modes, while each API request returns at most 600.

The Gradio dashboard at `/` streams an asynchronous update on each timer tick.
It can switch between live and simulated telemetry, adjust independent CPU and
memory alert thresholds, select Normal Operations, Load Test, or Simulated
Incident profiles, adjust its sample window and refresh interval, display
interactive Plotly trends, and export the chart data. Operational profiles only
affect simulated samples; they never create artificial load on the host.
The dashboard uses the same durable history as the API and Flutter client.

Run the Python API and dashboard tests with:

```sh
python -m unittest discover -s tests -v
```

## Run the Flutter client

The app source and web entry point are in [`../flutter_client`](../flutter_client).
Install the Flutter SDK, then from that directory:

```sh
flutter create --project-name telemetry_client --platforms android,ios,web .
flutter pub get
flutter run -d chrome
```

The generated project wrappers enable the Android and iOS targets as well.
The client polls every five seconds, keeps the server URL in local preferences,
and offers a source selector, metric cards, trends, alerts, and an event stream.
Use **Configure server** to enter the Python service URL. A phone must use the
server's private LAN IP (not `127.0.0.1`); `127.0.0.1` refers to the phone itself.

For Flutter web, set `TELEMETRY_CORS_ORIGINS` to the exact origin shown by the
web development server and restart the Python service. For native development
against an `http://` private-network URL, Android may require
`android:usesCleartextTraffic="true"` on the generated app and iOS may require
`NSAllowsLocalNetworking` plus `NSLocalNetworkUsageDescription` in the generated
`ios/Runner/Info.plist`. Prefer HTTPS when available. Do not enable broad
cleartext or ATS exceptions for an app that connects to untrusted networks.

With Flutter installed, run `flutter analyze` and `flutter test` from
`flutter_client/` to validate the client and its API-model test.
