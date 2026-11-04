# Telemetry Client

Flutter client for the Ghost Telemetry Engine 3.0 API. The client supports
Android, iOS, and web and stores its configured server URL on the device.

See [`../docs/telemetry-v3.md`](../docs/telemetry-v3.md) for backend setup, API
details, network access guidance, and platform-specific setup instructions.

From this directory, generate the Flutter platform wrappers if they are not
present, then install dependencies and start a target:

```sh
flutter create --project-name telemetry_client --platforms android,ios,web .
flutter pub get
flutter run -d chrome
```

The default server URL is `http://127.0.0.1:7860`. Use **Configure server** in
the app to select another URL. On a physical device, use the Python server's
private-network IP address.
