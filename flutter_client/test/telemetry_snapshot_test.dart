import 'package:flutter_test/flutter_test.dart';
import 'package:telemetry_client/main.dart';

void main() {
  test('parses a telemetry API response', () {
    final snapshot = TelemetrySnapshot.fromJson({
      'timestamp': '2026-11-04T10:00:00+00:00',
      'mode': 'live',
      'host': {'hostname': 'test-host', 'platform': 'Linux', 'processor': 'CPU'},
      'cpu_percent': 42.5,
      'memory_percent': 61,
      'memory_used_bytes': 600,
      'memory_total_bytes': 1000,
      'disk_percent': 51,
      'disk_used_bytes': 510,
      'disk_total_bytes': 1000,
      'network_sent_bytes_per_sec': 200.5,
      'network_recv_bytes_per_sec': 300.5,
      'active_connections': null,
      'process_count': 123,
      'uptime_seconds': 3600,
      'error_rate_percent': null,
      'alerts': ['CPU usage is high.'],
      'events': ['INFO: Host telemetry collected successfully.'],
    });

    expect(snapshot.hostname, 'test-host');
    expect(snapshot.cpuPercent, 42.5);
    expect(snapshot.activeConnections, isNull);
    expect(snapshot.errorRatePercent, isNull);
    expect(snapshot.alerts, hasLength(1));
  });
}
