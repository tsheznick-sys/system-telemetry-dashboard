# System Telemetry Dashboard 2.0

Telemetry 2.0 combines a Python host monitor and Gradio dashboard with a Flutter
client for Android, iOS, and web. Both interfaces use the same versioned JSON
API. Live measurements describe the machine running the Python service; the
simulated mode is available for demos and UI checks.

## Run the Python service

Python 3.10 or later is recommended.

```sh
python -m pip install -r requirements.txt
python app.py
```

Open [http://127.0.0.1:7860](http://127.0.0.1:7860). The service binds to
`127.0.0.1` by default, so it is only reachable from the same machine.

Configuration:

| Environment variable | Default | Description |
| --- | --- | --- |
| `TELEMETRY_HOST` | `127.0.0.1` | Uvicorn bind address. Set to `0.0.0.0` only when intentionally serving trusted private-network clients. |
| `TELEMETRY_PORT` | `7860` | HTTP port. |
| `TELEMETRY_CORS_ORIGINS` | `http://localhost:8080,http://127.0.0.1:8080,http://localhost:3000,http://127.0.0.1:3000` | Comma-separated browser origins allowed to call the API. Use the exact Flutter web origin. |

For example, to make the API available to a Flutter app on a trusted local
network, set `TELEMETRY_HOST=0.0.0.0`, allow the port through the host firewall
only on the private network, and configure the Flutter app with the server's
private IP address. This API has **no authentication or TLS**. Do not expose it
to the public internet or an untrusted network; use a VPN or add an authenticated
TLS-terminating gateway before allowing untrusted clients.

## API

Interactive OpenAPI documentation is available at `/docs`.

| Method and path | Description |
| --- | --- |
| `GET /api/v1/health` | Service version and health. |
| `GET /api/v1/metrics?mode=live` | Collect and return a current host sample. |
| `GET /api/v1/metrics?mode=simulated` | Generate a demo sample. |
| `GET /api/v1/history?mode=live&limit=120` | Return recent in-memory samples for one mode. `limit` is 1–600. |
| `GET /api/v1/export.csv?mode=live&limit=120` | Download recent samples as CSV. |

Each metrics response includes an ISO-8601 UTC timestamp, mode, host identity,
CPU, memory, disk, network throughput and totals, process count, uptime, load
average when supported, threshold alerts, and events. Live error rate is
`null`: the host service does not instrument application requests. Active
connection counts can also be `null` on operating systems or permission levels
that do not allow enumerating sockets; the response includes an availability
flag and an explanation. History is kept in memory (up to 600 samples) and is
cleared when the service restarts.

The dashboard at `/dashboard` polls the same collector, can switch between live
and simulated telemetry, adjust its sample window and refresh interval, display
resource trends and threshold alerts, and export the chart data.

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
