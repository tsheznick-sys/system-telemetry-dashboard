import 'dart:async';
import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

void main() {
  runApp(const TelemetryApp());
}

enum TelemetryMode { live, simulated }

extension TelemetryModeLabel on TelemetryMode {
  String get label => this == TelemetryMode.live ? 'Live host' : 'Simulated';
  String get queryValue => this == TelemetryMode.live ? 'live' : 'simulated';
}

class TelemetrySnapshot {
  const TelemetrySnapshot({
    required this.timestamp,
    required this.mode,
    required this.hostname,
    required this.platform,
    required this.cpuPercent,
    required this.memoryPercent,
    required this.memoryUsedBytes,
    required this.memoryTotalBytes,
    required this.diskPercent,
    required this.diskUsedBytes,
    required this.diskTotalBytes,
    required this.networkSentBytesPerSec,
    required this.networkRecvBytesPerSec,
    required this.activeConnections,
    required this.processCount,
    required this.uptimeSeconds,
    required this.errorRatePercent,
    required this.alerts,
    required this.events,
  });

  final DateTime timestamp;
  final String mode;
  final String hostname;
  final String platform;
  final double cpuPercent;
  final double memoryPercent;
  final int memoryUsedBytes;
  final int memoryTotalBytes;
  final double diskPercent;
  final int diskUsedBytes;
  final int diskTotalBytes;
  final double networkSentBytesPerSec;
  final double networkRecvBytesPerSec;
  final int? activeConnections;
  final int processCount;
  final double uptimeSeconds;
  final double? errorRatePercent;
  final List<String> alerts;
  final List<String> events;

  factory TelemetrySnapshot.fromJson(Map<String, dynamic> json) {
    final host = json['host'] as Map<String, dynamic>? ?? const {};
    return TelemetrySnapshot(
      timestamp: DateTime.parse(json['timestamp'] as String),
      mode: json['mode'] as String,
      hostname: host['hostname'] as String? ?? 'Unknown host',
      platform: host['platform'] as String? ?? 'Unknown platform',
      cpuPercent: (json['cpu_percent'] as num).toDouble(),
      memoryPercent: (json['memory_percent'] as num).toDouble(),
      memoryUsedBytes: (json['memory_used_bytes'] as num).toInt(),
      memoryTotalBytes: (json['memory_total_bytes'] as num).toInt(),
      diskPercent: (json['disk_percent'] as num).toDouble(),
      diskUsedBytes: (json['disk_used_bytes'] as num).toInt(),
      diskTotalBytes: (json['disk_total_bytes'] as num).toInt(),
      networkSentBytesPerSec:
          (json['network_sent_bytes_per_sec'] as num).toDouble(),
      networkRecvBytesPerSec:
          (json['network_recv_bytes_per_sec'] as num).toDouble(),
      activeConnections: (json['active_connections'] as num?)?.toInt(),
      processCount: (json['process_count'] as num).toInt(),
      uptimeSeconds: (json['uptime_seconds'] as num).toDouble(),
      errorRatePercent: (json['error_rate_percent'] as num?)?.toDouble(),
      alerts: (json['alerts'] as List<dynamic>? ?? const []).cast<String>(),
      events: (json['events'] as List<dynamic>? ?? const []).cast<String>(),
    );
  }
}

class TelemetryApi {
  const TelemetryApi(this.baseUrl);

  final String baseUrl;

  Future<Map<String, dynamic>> _get(
    String endpoint, [
    Map<String, String> query = const {},
  ]) async {
    final root = baseUrl.trim().replaceFirst(RegExp(r'/+$'), '');
    final uri = Uri.parse('$root/gradio_api/api/v1/$endpoint')
        .replace(queryParameters: query);
    final response = await http.get(uri).timeout(const Duration(seconds: 8));
    if (response.statusCode < 200 || response.statusCode >= 300) {
      throw TelemetryApiException(
        'Server returned HTTP ${response.statusCode}: ${response.body}',
      );
    }
    final decoded = jsonDecode(response.body);
    if (decoded is! Map<String, dynamic>) {
      throw const TelemetryApiException('The server returned an invalid response.');
    }
    return decoded;
  }

  Future<TelemetrySnapshot> metrics(TelemetryMode mode) async {
    final result = await _get('metrics', {'mode': mode.queryValue});
    return TelemetrySnapshot.fromJson(result);
  }

  Future<List<TelemetrySnapshot>> history(TelemetryMode mode) async {
    final root = baseUrl.trim().replaceFirst(RegExp(r'/+$'), '');
    final uri = Uri.parse('$root/gradio_api/api/v1/history').replace(
      queryParameters: {'mode': mode.queryValue, 'limit': '120'},
    );
    final response = await http.get(uri).timeout(const Duration(seconds: 8));
    if (response.statusCode < 200 || response.statusCode >= 300) {
      throw TelemetryApiException(
        'Server returned HTTP ${response.statusCode}: ${response.body}',
      );
    }
    final decoded = jsonDecode(response.body);
    if (decoded is! List<dynamic>) {
      throw const TelemetryApiException('The server returned invalid history.');
    }
    return decoded
        .map(
          (item) => TelemetrySnapshot.fromJson(item as Map<String, dynamic>),
        )
        .toList();
  }
}

class TelemetryApiException implements Exception {
  const TelemetryApiException(this.message);

  final String message;

  @override
  String toString() => message;
}

class TelemetryApp extends StatelessWidget {
  const TelemetryApp({super.key});

  @override
  Widget build(BuildContext context) {
    const seed = Color(0xFF12C8C0);
    const surface = Color(0xFF0B1119);
    const panel = Color(0xFF111927);
    const panelHigh = Color(0xFF17222F);
    final scheme = ColorScheme.fromSeed(
      seedColor: seed,
      brightness: Brightness.dark,
    ).copyWith(
      surface: surface,
      surfaceContainerLowest: const Color(0xFF080D14),
      surfaceContainerLow: panel,
      surfaceContainer: panel,
      surfaceContainerHigh: panelHigh,
      surfaceContainerHighest: const Color(0xFF1E2B3D),
      onSurface: const Color(0xFFE6EDF6),
      onSurfaceVariant: const Color(0xFF8B9BB0),
      outlineVariant: const Color(0x22FFFFFF),
    );
    return MaterialApp(
      title: 'System Telemetry',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorScheme: scheme,
        scaffoldBackgroundColor: surface,
        useMaterial3: true,
        textTheme: const TextTheme().apply(
          bodyColor: const Color(0xFFE6EDF6),
          displayColor: const Color(0xFFF2F7FD),
        ),
        appBarTheme: const AppBarTheme(
          backgroundColor: Color(0xFF0B1119),
          foregroundColor: Color(0xFFF2F7FD),
          elevation: 0,
          scrolledUnderElevation: 0,
          centerTitle: false,
        ),
        filledButtonTheme: FilledButtonThemeData(
          style: FilledButton.styleFrom(
            backgroundColor: seed,
            foregroundColor: const Color(0xFF05131C),
            textStyle: const TextStyle(fontWeight: FontWeight.w700),
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(12),
            ),
          ),
        ),
        inputDecorationTheme: InputDecorationTheme(
          filled: true,
          fillColor: panelHigh,
          border: OutlineInputBorder(
            borderRadius: BorderRadius.circular(12),
            borderSide: const BorderSide(color: Color(0x14FFFFFF)),
          ),
          focusedBorder: OutlineInputBorder(
            borderRadius: BorderRadius.circular(12),
            borderSide: const BorderSide(color: seed, width: 1.6),
          ),
        ),
        dividerTheme: const DividerThemeData(
          color: Color(0x14FFFFFF),
          thickness: 1,
        ),
      ),
      home: const TelemetryHomePage(),
    );
  }
}

class TelemetryHomePage extends StatefulWidget {
  const TelemetryHomePage({super.key});

  @override
  State<TelemetryHomePage> createState() => _TelemetryHomePageState();
}

class _TelemetryHomePageState extends State<TelemetryHomePage> {
  static const _urlPreferenceKey = 'telemetry_server_url';
  static const _defaultUrl = 'http://127.0.0.1:7860';

  String _serverUrl = _defaultUrl;
  TelemetryMode _mode = TelemetryMode.live;
  TelemetrySnapshot? _current;
  List<TelemetrySnapshot> _history = const [];
  String? _error;
  bool _loading = true;
  bool _refreshing = false;
  Timer? _timer;

  @override
  void initState() {
    super.initState();
    _timer = Timer.periodic(const Duration(seconds: 5), (_) => _refresh());
    unawaited(_loadPreferences());
  }

  @override
  void dispose() {
    _timer?.cancel();
    super.dispose();
  }

  Future<void> _loadPreferences() async {
    final preferences = await SharedPreferences.getInstance();
    final savedUrl = preferences.getString(_urlPreferenceKey);
    if (!mounted) return;
    if (savedUrl != null && savedUrl.isNotEmpty) {
      setState(() => _serverUrl = savedUrl);
    }
    await _refresh();
  }

  Future<void> _refresh() async {
    if (_refreshing) return;
    _refreshing = true;
    final requestMode = _mode;
    final requestUrl = _serverUrl;
    if (_current == null && mounted) setState(() => _loading = true);
    try {
      final api = TelemetryApi(requestUrl);
      final sample = await api.metrics(requestMode);
      final history = await api.history(requestMode);
      if (!mounted || requestMode != _mode || requestUrl != _serverUrl) return;
      setState(() {
        _current = sample;
        _history = history;
        _error = null;
        _loading = false;
      });
    } catch (error) {
      if (!mounted || requestMode != _mode || requestUrl != _serverUrl) return;
      setState(() {
        _error = error.toString();
        _loading = false;
      });
    } finally {
      _refreshing = false;
      if (mounted && (requestMode != _mode || requestUrl != _serverUrl)) {
        unawaited(_refresh());
      }
    }
  }

  Future<void> _changeMode(TelemetryMode? value) async {
    if (value == null || value == _mode) return;
    setState(() {
      _mode = value;
      _current = null;
      _history = const [];
      _loading = true;
    });
    await _refresh();
  }

  Future<void> _configureServer() async {
    final controller = TextEditingController(text: _serverUrl);
    final formKey = GlobalKey<FormState>();
    final url = await showDialog<String>(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Connect to telemetry server'),
        content: Form(
          key: formKey,
          child: TextFormField(
            controller: controller,
            autofocus: true,
            keyboardType: TextInputType.url,
            decoration: const InputDecoration(
              labelText: 'Server URL',
              hintText: 'http://192.168.1.20:7860',
              prefixIcon: Icon(Icons.link),
            ),
            validator: (value) {
              final uri = Uri.tryParse(value?.trim() ?? '');
              if (uri == null ||
                  !uri.hasAuthority ||
                  !{'http', 'https'}.contains(uri.scheme)) {
                return 'Enter a complete http:// or https:// server URL.';
              }
              return null;
            },
            onFieldSubmitted: (_) {
              if (formKey.currentState?.validate() ?? false) {
                Navigator.pop(context, controller.text.trim());
              }
            },
          ),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('Cancel'),
          ),
          FilledButton(
            onPressed: () {
              if (formKey.currentState?.validate() ?? false) {
                Navigator.pop(context, controller.text.trim());
              }
            },
            child: const Text('Save and connect'),
          ),
        ],
      ),
    );
    controller.dispose();
    if (url == null || !mounted) return;
    final preferences = await SharedPreferences.getInstance();
    await preferences.setString(_urlPreferenceKey, url);
    setState(() {
      _serverUrl = url;
      _current = null;
      _history = const [];
      _loading = true;
    });
    await _refresh();
  }

  @override
  Widget build(BuildContext context) {
    final sample = _current;
    return Scaffold(
      appBar: AppBar(
        titleSpacing: 20,
        title: const Row(
          children: [
            Icon(Icons.monitor_heart_outlined, color: Color(0xFF12C8C0)),
            SizedBox(width: 10),
            Text('TELEMETRY', style: TextStyle(letterSpacing: 2)),
            SizedBox(width: 8),
            Text('4.0', style: TextStyle(color: Color(0xFF12C8C0))),
          ],
        ),
        actions: [
          IconButton(
            tooltip: 'Configure server',
            onPressed: _configureServer,
            icon: const Icon(Icons.settings_outlined),
          ),
          IconButton(
            tooltip: 'Refresh now',
            onPressed: _refresh,
            icon: const Icon(Icons.refresh),
          ),
          const SizedBox(width: 8),
        ],
      ),
      body: SafeArea(
        top: false,
        child: RefreshIndicator(
          onRefresh: _refresh,
          child: ListView(
            padding: const EdgeInsets.fromLTRB(20, 12, 20, 32),
            children: [
              _buildHeader(sample),
              const SizedBox(height: 20),
              if (_loading && sample == null)
                const SizedBox(
                  height: 260,
                  child: Center(child: CircularProgressIndicator()),
                )
              else if (_error != null && sample == null)
                _buildConnectionError()
              else if (sample != null) ...[
                if (_error != null) _buildStaleWarning(),
                _buildMetricGrid(sample),
                const SizedBox(height: 24),
                _buildTrendSection(),
                const SizedBox(height: 24),
                _buildAlerts(sample),
                const SizedBox(height: 24),
                _buildEvents(sample),
              ]
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildHeader(TelemetrySnapshot? sample) {
    final subtitle = sample == null
        ? _serverUrl
        : '${sample.hostname}  ·  ${sample.platform}';
    return LayoutBuilder(
      builder: (context, constraints) {
        final compact = constraints.maxWidth < 540;
        return Card(
          child: Padding(
            padding: const EdgeInsets.all(20),
            child: Wrap(
              alignment: WrapAlignment.spaceBetween,
              crossAxisAlignment: WrapCrossAlignment.center,
              runSpacing: 16,
              spacing: 16,
              children: [
                SizedBox(
                  width: compact ? constraints.maxWidth - 40 : 320,
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        'SYSTEM OVERVIEW',
                        style: Theme.of(context).textTheme.labelMedium?.copyWith(
                              color: const Color(0xFF12C8C0),
                              letterSpacing: 1.5,
                            ),
                      ),
                      const SizedBox(height: 6),
                      Text(
                        sample?.hostname ?? 'Host telemetry',
                        style: Theme.of(context).textTheme.headlineSmall,
                        overflow: TextOverflow.ellipsis,
                      ),
                      const SizedBox(height: 4),
                      Text(
                        subtitle,
                        style: Theme.of(context).textTheme.bodySmall?.copyWith(
                              color: Colors.white60,
                            ),
                        maxLines: 2,
                        overflow: TextOverflow.ellipsis,
                      ),
                    ],
                  ),
                ),
                Wrap(
                  spacing: 10,
                  runSpacing: 10,
                  crossAxisAlignment: WrapCrossAlignment.center,
                  children: [
                    DropdownButton<TelemetryMode>(
                      value: _mode,
                      underline: const SizedBox.shrink(),
                      onChanged: _changeMode,
                      items: TelemetryMode.values
                          .map(
                            (mode) => DropdownMenuItem(
                              value: mode,
                              child: Text(mode.label),
                            ),
                          )
                          .toList(),
                    ),
                    _statusPill(
                      sample == null
                          ? 'CONNECTING'
                          : _error == null
                              ? 'CONNECTED'
                              : 'STALE DATA',
                      sample != null && _error == null,
                    ),
                  ],
                ),
              ],
            ),
          ),
        );
      },
    );
  }

  Widget _statusPill(String label, bool healthy) {
    final color = healthy ? const Color(0xFF53D7A5) : const Color(0xFFFFB45C);
    return DecoratedBox(
      decoration: BoxDecoration(
        color: color.withOpacity(0.12),
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: color.withOpacity(0.35)),
      ),
      child: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
        child: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(Icons.circle, size: 8, color: color),
            const SizedBox(width: 8),
            Text(
              label,
              style: TextStyle(
                color: color,
                fontSize: 11,
                fontWeight: FontWeight.w700,
                letterSpacing: 0.7,
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildMetricGrid(TelemetrySnapshot sample) {
    final width = MediaQuery.sizeOf(context).width;
    final columns = width >= 1100 ? 4 : width >= 650 ? 2 : 1;
    final metrics = [
      _MetricData(
        'CPU usage',
        sample.cpuPercent,
        '%',
        Icons.memory,
        const Color(0xFF46C7F5),
        'Processor load',
      ),
      _MetricData(
        'Memory',
        sample.memoryPercent,
        '%',
        Icons.storage,
        const Color(0xFFAF8CFF),
        '${_formatBytes(sample.memoryUsedBytes)} / ${_formatBytes(sample.memoryTotalBytes)}',
      ),
      _MetricData(
        'Disk usage',
        sample.diskPercent,
        '%',
        Icons.disc_full_outlined,
        const Color(0xFFFFB45C),
        '${_formatBytes(sample.diskUsedBytes)} / ${_formatBytes(sample.diskTotalBytes)}',
      ),
      _MetricData(
        'Active connections',
        sample.activeConnections?.toDouble() ?? 0,
        '',
        Icons.hub_outlined,
        const Color(0xFF53D7A5),
        sample.activeConnections == null ? 'Not available' : 'Established',
        displayValue:
            sample.activeConnections?.toString() ?? 'Unavailable',
      ),
      _MetricData(
        'Network sent',
        sample.networkSentBytesPerSec,
        '/s',
        Icons.north_east,
        const Color(0xFF46C7F5),
        'Current throughput',
        displayValue: '${_formatBytes(sample.networkSentBytesPerSec)}/s',
      ),
      _MetricData(
        'Network received',
        sample.networkRecvBytesPerSec,
        '/s',
        Icons.south_west,
        const Color(0xFF53D7A5),
        'Current throughput',
        displayValue: '${_formatBytes(sample.networkRecvBytesPerSec)}/s',
      ),
      _MetricData(
        'Processes',
        sample.processCount.toDouble(),
        '',
        Icons.account_tree_outlined,
        const Color(0xFFFFB45C),
        'Running on host',
        displayValue: sample.processCount.toString(),
      ),
      _MetricData(
        'Error rate',
        sample.errorRatePercent ?? 0,
        '%',
        Icons.error_outline,
        const Color(0xFFFF7185),
        sample.errorRatePercent == null ? 'Not instrumented on host' : 'Demo metric',
        displayValue: sample.errorRatePercent == null
            ? '—'
            : '${sample.errorRatePercent!.toStringAsFixed(2)}%',
      ),
    ];
    return GridView.builder(
      shrinkWrap: true,
      physics: const NeverScrollableScrollPhysics(),
      itemCount: metrics.length,
      gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
        crossAxisCount: columns,
        mainAxisSpacing: 12,
        crossAxisSpacing: 12,
        mainAxisExtent: 142,
      ),
      itemBuilder: (context, index) => _MetricCard(data: metrics[index]),
    );
  }

  Widget _buildTrendSection() {
    return _SectionCard(
      title: 'Resource trends',
      subtitle: 'Recent CPU, memory, and disk utilization',
      icon: Icons.show_chart,
      child: SizedBox(
        height: 230,
        child: _history.length < 2
            ? const Center(
                child: Text(
                  'Collecting samples — trend lines appear after the next refresh.',
                  textAlign: TextAlign.center,
                ),
              )
            : CustomPaint(
                painter: _TrendPainter(_history),
                child: const SizedBox.expand(),
              ),
      ),
    );
  }

  Widget _buildAlerts(TelemetrySnapshot sample) {
    final hasAlerts = sample.alerts.isNotEmpty;
    final color = hasAlerts ? const Color(0xFFFFB45C) : const Color(0xFF53D7A5);
    return _SectionCard(
      title: 'Health alerts',
      subtitle: hasAlerts
          ? '${sample.alerts.length} threshold${sample.alerts.length == 1 ? '' : 's'} exceeded'
          : 'All monitored thresholds are clear',
      icon: hasAlerts ? Icons.warning_amber_rounded : Icons.verified_outlined,
      accent: color,
      child: hasAlerts
          ? Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: sample.alerts
                  .map((alert) => _EventRow(text: alert, color: color))
                  .toList(),
            )
          : Text(
              'No CPU, memory, or disk threshold alerts.',
              style: TextStyle(color: Colors.white.withOpacity(0.66)),
            ),
    );
  }

  Widget _buildEvents(TelemetrySnapshot sample) {
    return _SectionCard(
      title: 'Event stream',
      subtitle: 'Latest events from this telemetry source',
      icon: Icons.receipt_long_outlined,
      child: Column(
        children: sample.events
            .map(
              (event) => _EventRow(
                text: event,
                color: event.startsWith('ALERT')
                    ? const Color(0xFFFFB45C)
                    : const Color(0xFF8DA0B5),
              ),
            )
            .toList(),
      ),
    );
  }

  Widget _buildConnectionError() {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          children: [
            const Icon(
              Icons.cloud_off_outlined,
              size: 42,
              color: Color(0xFFFF7185),
            ),
            const SizedBox(height: 12),
            Text('Unable to reach the telemetry server',
                style: Theme.of(context).textTheme.titleLarge),
            const SizedBox(height: 8),
            Text(_error ?? 'Check the server URL and try again.'),
            const SizedBox(height: 8),
            Text(
              _serverUrl,
              style: const TextStyle(color: Colors.white60),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 16),
            Wrap(
              spacing: 12,
              children: [
                FilledButton.icon(
                  onPressed: _refresh,
                  icon: const Icon(Icons.refresh),
                  label: const Text('Retry'),
                ),
                OutlinedButton.icon(
                  onPressed: _configureServer,
                  icon: const Icon(Icons.settings_outlined),
                  label: const Text('Configure server'),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildStaleWarning() {
    return Padding(
      padding: const EdgeInsets.only(bottom: 12),
      child: MaterialBanner(
        content: Text('Showing the last successful sample. ${_error!}'),
        leading: const Icon(Icons.cloud_off_outlined),
        actions: [
          TextButton(onPressed: _refresh, child: const Text('RETRY')),
        ],
      ),
    );
  }
}

class _MetricData {
  const _MetricData(
    this.label,
    this.value,
    this.unit,
    this.icon,
    this.color,
    this.caption, {
    this.displayValue,
  });

  final String label;
  final double value;
  final String unit;
  final IconData icon;
  final Color color;
  final String caption;
  final String? displayValue;
}

class _MetricCard extends StatelessWidget {
  const _MetricCard({required this.data});

  final _MetricData data;

  @override
  Widget build(BuildContext context) {
    final value = data.displayValue ?? '${data.value.toStringAsFixed(1)}${data.unit}';
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Row(
              children: [
                Icon(data.icon, color: data.color, size: 19),
                const SizedBox(width: 8),
                Expanded(
                  child: Text(
                    data.label,
                    style: Theme.of(context).textTheme.labelLarge,
                    overflow: TextOverflow.ellipsis,
                  ),
                ),
              ],
            ),
            Text(
              value,
              style: Theme.of(context).textTheme.headlineMedium?.copyWith(
                    fontWeight: FontWeight.w700,
                    color: data.color,
                  ),
              maxLines: 1,
              overflow: TextOverflow.ellipsis,
            ),
            Text(
              data.caption,
              style: Theme.of(context)
                  .textTheme
                  .bodySmall
                  ?.copyWith(color: Colors.white60),
              overflow: TextOverflow.ellipsis,
            ),
          ],
        ),
      ),
    );
  }
}

class _SectionCard extends StatelessWidget {
  const _SectionCard({
    required this.title,
    required this.subtitle,
    required this.icon,
    required this.child,
    this.accent = const Color(0xFF12C8C0),
  });

  final String title;
  final String subtitle;
  final IconData icon;
  final Widget child;
  final Color accent;

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Icon(icon, color: accent),
                const SizedBox(width: 10),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(title, style: Theme.of(context).textTheme.titleMedium),
                      Text(
                        subtitle,
                        style: Theme.of(context)
                            .textTheme
                            .bodySmall
                            ?.copyWith(color: Colors.white60),
                      ),
                    ],
                  ),
                ),
              ],
            ),
            const SizedBox(height: 20),
            child,
          ],
        ),
      ),
    );
  }
}

class _EventRow extends StatelessWidget {
  const _EventRow({required this.text, required this.color});

  final String text;
  final Color color;

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 10),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Padding(
            padding: const EdgeInsets.only(top: 5),
            child: Icon(Icons.circle, size: 7, color: color),
          ),
          const SizedBox(width: 10),
          Expanded(child: Text(text)),
        ],
      ),
    );
  }
}

class _TrendPainter extends CustomPainter {
  _TrendPainter(this.samples);

  final List<TelemetrySnapshot> samples;

  @override
  void paint(Canvas canvas, Size size) {
    const left = 34.0;
    const right = 10.0;
    const top = 14.0;
    const bottom = 24.0;
    final chartWidth = size.width - left - right;
    final chartHeight = size.height - top - bottom;
    final gridPaint = Paint()
      ..color = Colors.white.withOpacity(0.09)
      ..strokeWidth = 1;
    final labelStyle = const TextStyle(color: Colors.white54, fontSize: 10);
    for (var index = 0; index <= 4; index++) {
      final y = top + chartHeight * index / 4;
      canvas.drawLine(Offset(left, y), Offset(size.width - right, y), gridPaint);
      final label = TextPainter(
        text: TextSpan(text: '${100 - index * 25}%', style: labelStyle),
        textDirection: TextDirection.ltr,
      )..layout();
      label.paint(canvas, Offset(0, y - label.height / 2));
    }
    final series = [
      (const Color(0xFF46C7F5), (TelemetrySnapshot sample) => sample.cpuPercent),
      (const Color(0xFFAF8CFF), (TelemetrySnapshot sample) => sample.memoryPercent),
      (const Color(0xFFFFB45C), (TelemetrySnapshot sample) => sample.diskPercent),
    ];
    for (final (color, readValue) in series) {
      final path = Path();
      for (var index = 0; index < samples.length; index++) {
        final x = left + chartWidth * index / (samples.length - 1);
        final normalized = (readValue(samples[index]).clamp(0, 100)) / 100;
        final y = top + chartHeight * (1 - normalized);
        if (index == 0) {
          path.moveTo(x, y);
        } else {
          path.lineTo(x, y);
        }
      }
      canvas.drawPath(
        path,
        Paint()
          ..color = color
          ..style = PaintingStyle.stroke
          ..strokeWidth = 2
          ..strokeCap = StrokeCap.round
          ..strokeJoin = StrokeJoin.round,
      );
    }
    final legend = [
      ('CPU', const Color(0xFF46C7F5)),
      ('Memory', const Color(0xFFAF8CFF)),
      ('Disk', const Color(0xFFFFB45C)),
    ];
    var x = left;
    for (final (label, color) in legend) {
      canvas.drawCircle(
        Offset(x + 4, size.height - 10),
        4,
        Paint()..color = color,
      );
      final text = TextPainter(
        text: TextSpan(text: label, style: labelStyle),
        textDirection: TextDirection.ltr,
      )..layout();
      text.paint(canvas, Offset(x + 12, size.height - 16));
      x += text.width + 34;
    }
  }

  @override
  bool shouldRepaint(covariant _TrendPainter oldDelegate) =>
      oldDelegate.samples != samples;
}

String _formatBytes(num value) {
  var amount = value.toDouble();
  for (final unit in ['B', 'KB', 'MB', 'GB', 'TB']) {
    if (amount < 1024 || unit == 'TB') {
      return '${amount.toStringAsFixed(1)} $unit';
    }
    amount /= 1024;
  }
  return '${amount.toStringAsFixed(1)} TB';
}
