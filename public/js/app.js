import { downloadCsv } from './csv.js';
import { initializeTaskManager } from './task-manager.js';

const status = document.getElementById('status');
const refreshButton = document.getElementById('refresh');
const logsContainer = document.getElementById('logs');
const filters = document.querySelector('.filters');
const searchInput = document.getElementById('log-search');
const thresholdDialog = document.getElementById('threshold-dialog');
const thresholdForm = document.getElementById('threshold-form');
const historyStorageKey = 'pulse.telemetry.history';
const thresholdStorageKey = 'pulse.telemetry.thresholds';
const maxHistorySamples = 1000;
const metricOptions = {
  cpuUsage: { label: 'CPU utilization', unit: '%', color: '#66e3d2', max: 100 },
  memoryUsage: { label: 'Memory usage', unit: '%', color: '#ae9bff', max: 100 },
  activeConnections: { label: 'Active connections', unit: '', color: '#82a9ff', max: 5000 },
  errorRate: { label: 'Error rate', unit: '%', color: '#f0ad79', max: 2 },
};
const defaultThresholds = { cpu: 85, memory: 85, errors: 1 };
let historyPoints = [];
let eventHistory = [];
let activeFilter = 'ALL';
let activeMetric = 'cpuUsage';
let activeRange = 60;
let thresholds = { ...defaultThresholds };
let lastMetrics = null;
let requestInProgress = false;

try {
  const savedHistory = JSON.parse(localStorage.getItem(historyStorageKey) || '[]');
  if (Array.isArray(savedHistory)) {
    historyPoints = savedHistory
      .filter(
        (point) =>
          point &&
          Number.isFinite(point.timestamp) &&
          Number.isFinite(point.cpuUsage) &&
          Number.isFinite(point.memoryUsage) &&
          Number.isFinite(point.activeConnections) &&
          Number.isFinite(point.errorRate),
      )
      .slice(-maxHistorySamples);
  }
} catch (error) {
  console.warn('Unable to load saved telemetry history:', error);
}

try {
  const savedThresholds = JSON.parse(localStorage.getItem(thresholdStorageKey) || 'null');
  if (
    savedThresholds &&
    ['cpu', 'memory', 'errors'].every((key) => Number.isFinite(savedThresholds[key]))
  ) {
    thresholds = {
      cpu: Math.min(100, Math.max(1, savedThresholds.cpu)),
      memory: Math.min(100, Math.max(1, savedThresholds.memory)),
      errors: Math.min(100, Math.max(0.01, savedThresholds.errors)),
    };
  }
} catch (error) {
  console.warn('Unable to load saved alert thresholds:', error);
}

function saveHistory() {
  try {
    localStorage.setItem(historyStorageKey, JSON.stringify(historyPoints));
  } catch (error) {
    console.warn('Unable to save telemetry history:', error);
  }
}

function renderChart() {
  const metric = metricOptions[activeMetric];
  const now = Date.now();
  const rangeStart = now - activeRange * 1000;
  const samples = historyPoints.filter((point) => point.timestamp >= rangeStart);
  const line = document.getElementById('chart-line');
  const area = document.getElementById('chart-area');
  const point = document.getElementById('chart-last-point');
  const chart = document.getElementById('history-chart');
  const chartColor = metric.color;
  chart.style.setProperty('--chart-color', chartColor);
  chart.setAttribute('aria-label', `${metric.label} over the last ${activeRange / 60} minute(s)`);
  document.getElementById('chart-unit').textContent = metric.unit;
  document.getElementById('chart-max').textContent = metric.max.toLocaleString();
  document.getElementById('chart-min').textContent = '0';
  document.getElementById('chart-start').textContent = new Date(rangeStart).toLocaleTimeString([], {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
  });
  document.getElementById('chart-end').textContent = new Date(now).toLocaleTimeString([], {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
  });

  const latest = samples[samples.length - 1];
  if (!latest) {
    document.getElementById('chart-current').textContent = '—';
    document.getElementById('chart-samples').textContent = 'No samples in this range';
    line.setAttribute('d', '');
    area.setAttribute('d', '');
    point.setAttribute('visibility', 'hidden');
    return;
  }

  const value = latest[activeMetric];
  const scaleMax = Math.max(metric.max, Math.ceil(value * 1.15));
  const left = 48;
  const right = 790;
  const top = 20;
  const bottom = 146;
  const coordinates = samples.map((sample) => ({
    x:
      left +
      Math.max(0, Math.min(1, (sample.timestamp - rangeStart) / (activeRange * 1000))) *
        (right - left),
    y: bottom - (sample[activeMetric] / scaleMax) * (bottom - top),
  }));
  const linePath = coordinates
    .map(
      (coordinate, index) =>
        `${index === 0 ? 'M' : 'L'}${coordinate.x.toFixed(2)} ${coordinate.y.toFixed(2)}`,
    )
    .join(' ');
  const first = coordinates[0];
  const last = coordinates[coordinates.length - 1];
  line.setAttribute('d', linePath);
  area.setAttribute(
    'd',
    `${linePath} L${last.x.toFixed(2)} ${bottom} L${first.x.toFixed(2)} ${bottom} Z`,
  );
  point.setAttribute('cx', last.x.toFixed(2));
  point.setAttribute('cy', last.y.toFixed(2));
  point.setAttribute('visibility', 'visible');
  document.getElementById('chart-max').textContent = scaleMax.toLocaleString();
  document.getElementById('chart-current').textContent = new Intl.NumberFormat(undefined, {
    maximumFractionDigits:
      activeMetric === 'errorRate' || activeMetric === 'cpuUsage' || activeMetric === 'memoryUsage'
        ? 2
        : 0,
  }).format(value);
  document.getElementById('chart-samples').textContent =
    `${samples.length} sample${samples.length === 1 ? '' : 's'}`;
}

function renderLogs() {
  const query = searchInput.value.trim().toLocaleLowerCase();
  const visibleLogs = eventHistory.filter((log) => {
    const matchesLevel = activeFilter === 'ALL' || log.level === activeFilter;
    const matchesSearch =
      !query || `${log.level} ${log.message} ${log.id}`.toLocaleLowerCase().includes(query);
    return matchesLevel && matchesSearch;
  });

  if (visibleLogs.length === 0) {
    const empty = document.createElement('div');
    empty.className = 'empty-state';
    empty.textContent = eventHistory.length
      ? 'No events match your search and filters.'
      : 'Waiting for system events…';
    logsContainer.replaceChildren(empty);
    return;
  }

  logsContainer.replaceChildren(
    ...visibleLogs.map((log) => {
      const row = document.createElement('div');
      row.className = 'log';

      const time = document.createElement('time');
      time.className = 'log-time';
      time.textContent = log.time;

      const level = document.createElement('span');
      level.className = 'log-level';
      level.dataset.level = log.level;
      level.textContent = log.level;

      const message = document.createElement('span');
      message.className = 'log-message';
      message.textContent = log.message;

      const id = document.createElement('span');
      id.className = 'log-id';
      id.textContent = log.id.slice(0, 6);
      id.title = log.id;

      row.append(time, level, message, id);
      return row;
    }),
  );
}

function renderAlerts(metrics) {
  const triggered = [
    metrics.cpuUsage >= thresholds.cpu && `CPU ${metrics.cpuUsage}%`,
    metrics.memoryUsage >= thresholds.memory && `Memory ${metrics.memoryUsage}%`,
    metrics.errorRate >= thresholds.errors && `Errors ${metrics.errorRate}%`,
  ].filter(Boolean);

  document
    .querySelector('.metric-card.cpu')
    .classList.toggle('is-alert', metrics.cpuUsage >= thresholds.cpu);
  document
    .querySelector('.metric-card.memory')
    .classList.toggle('is-alert', metrics.memoryUsage >= thresholds.memory);
  document
    .querySelector('.metric-card.errors')
    .classList.toggle('is-alert', metrics.errorRate >= thresholds.errors);
  document.getElementById('service-health').textContent = triggered.length
    ? 'Attention needed'
    : 'Operational';
  document.getElementById('service-health').classList.toggle('good', triggered.length === 0);

  if (status.dataset.state === 'error') return;
  status.dataset.state = triggered.length ? 'warning' : 'live';
  status.querySelector('.status-label').textContent = triggered.length
    ? `Threshold reached: ${triggered.join(', ')}`
    : 'All systems operational';
  document.getElementById('status-detail').textContent = triggered.length
    ? 'Review configured alert limits'
    : 'Receiving live telemetry';
}

function updateMetric(id, value, barId, fillPercentage, footId, description) {
  document.getElementById(id).textContent = value;
  document.getElementById(barId).style.width = `${Math.max(0, Math.min(100, fillPercentage))}%`;
  document.getElementById(footId).textContent = description;
}

async function fetchTelemetry() {
  if (requestInProgress) return;
  requestInProgress = true;
  refreshButton.disabled = true;
  refreshButton.classList.add('is-loading');

  const startedAt = performance.now();
  try {
    const response = await fetch('/api/telemetry');
    if (!response.ok) {
      throw new Error(`Telemetry request failed: ${response.status}`);
    }

    const data = await response.json();
    const { cpuUsage, memoryUsage, activeConnections, errorRate } = data.metrics;
    lastMetrics = { cpuUsage, memoryUsage, activeConnections, errorRate };
    updateMetric('cpu', cpuUsage, 'cpu-bar', cpuUsage, 'cpu-foot', 'Current load');
    updateMetric('memory', memoryUsage, 'memory-bar', memoryUsage, 'memory-foot', 'In use');
    updateMetric(
      'connections',
      new Intl.NumberFormat().format(activeConnections),
      'connections-bar',
      activeConnections / 45,
      'connections-foot',
      'Concurrent now',
    );
    updateMetric(
      'errors',
      errorRate,
      'errors-bar',
      (errorRate / 1.5) * 100,
      'errors-foot',
      errorRate >= thresholds.errors ? 'Threshold reached' : 'Within threshold',
    );

    const sample = {
      timestamp: Date.parse(data.timestamp),
      cpuUsage,
      memoryUsage,
      activeConnections,
      errorRate,
      activeNode: data.activeNode,
    };
    if (Number.isFinite(sample.timestamp)) {
      historyPoints.push(sample);
      historyPoints = historyPoints.slice(-maxHistorySamples);
      saveHistory();
      renderChart();
    }
    document.getElementById('active-node').textContent = data.activeNode;
    document.getElementById('node-detail').textContent = data.activeNode;
    document.getElementById('updated-at').textContent = new Date(data.timestamp).toLocaleTimeString(
      [],
      {
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
      },
    );
    document.getElementById('response-time').textContent =
      `${Math.round(performance.now() - startedAt)} ms`;
    status.dataset.state = 'live';
    renderAlerts(lastMetrics);
    eventHistory = [
      ...new Map([...data.recentLogs, ...eventHistory].map((log) => [log.id, log])).values(),
    ].slice(0, 50);
    renderLogs();
  } catch (error) {
    console.error('Telemetry polling error:', error);
    status.dataset.state = 'error';
    status.querySelector('.status-label').textContent = 'Connection interrupted';
    document.getElementById('status-detail').textContent = 'Unable to reach telemetry service';
    document.getElementById('service-health').textContent = 'Unavailable';
    document.getElementById('service-health').classList.remove('good');
  } finally {
    requestInProgress = false;
    refreshButton.disabled = false;
    refreshButton.classList.remove('is-loading');
  }
}

refreshButton.addEventListener('click', fetchTelemetry);
document.getElementById('export-button').addEventListener('click', () => {
  if (historyPoints.length === 0) {
    document.getElementById('status-detail').textContent = 'No telemetry samples to export yet';
    return;
  }
  const headers = [
    'timestamp',
    'cpuUsage',
    'memoryUsage',
    'activeConnections',
    'errorRate',
    'activeNode',
  ];
  const rows = historyPoints.map((sample) => [
    new Date(sample.timestamp).toISOString(),
    sample.cpuUsage,
    sample.memoryUsage,
    sample.activeConnections,
    sample.errorRate,
    sample.activeNode,
  ]);
  downloadCsv([headers, ...rows], 'pulse-telemetry.csv');
});
document.getElementById('export-logs-button').addEventListener('click', () => {
  if (eventHistory.length === 0) return;
  const rows = eventHistory.map((log) => [log.time, log.level, log.message, log.id]);
  downloadCsv([['time', 'level', 'message', 'id'], ...rows], 'pulse-events.csv');
});
document.getElementById('alerts-button').addEventListener('click', () => {
  thresholdForm.elements.cpu.value = thresholds.cpu;
  thresholdForm.elements.memory.value = thresholds.memory;
  thresholdForm.elements.errors.value = thresholds.errors;
  thresholdDialog.showModal();
});
document
  .getElementById('close-thresholds')
  .addEventListener('click', () => thresholdDialog.close());
document
  .getElementById('cancel-thresholds')
  .addEventListener('click', () => thresholdDialog.close());
thresholdForm.addEventListener('submit', (event) => {
  event.preventDefault();
  const nextThresholds = {
    cpu: Number(thresholdForm.elements.cpu.value),
    memory: Number(thresholdForm.elements.memory.value),
    errors: Number(thresholdForm.elements.errors.value),
  };
  if (Object.values(nextThresholds).some((value) => !Number.isFinite(value))) {
    thresholdForm.reportValidity();
    return;
  }
  thresholds = nextThresholds;
  try {
    localStorage.setItem(thresholdStorageKey, JSON.stringify(thresholds));
  } catch (error) {
    console.warn('Unable to save alert thresholds:', error);
  }
  if (lastMetrics) renderAlerts(lastMetrics);
  thresholdDialog.close();
});
document.querySelectorAll('[data-metric]').forEach((button) => {
  button.addEventListener('click', () => {
    activeMetric = button.dataset.metric;
    document.querySelectorAll('[data-metric]').forEach((tab) => {
      tab.setAttribute('aria-pressed', String(tab === button));
    });
    renderChart();
  });
});
document.querySelectorAll('[data-range]').forEach((button) => {
  button.addEventListener('click', () => {
    activeRange = Number(button.dataset.range);
    document.querySelectorAll('[data-range]').forEach((tab) => {
      tab.setAttribute('aria-pressed', String(tab === button));
    });
    renderChart();
  });
});
filters.addEventListener('click', (event) => {
  const button = event.target.closest('[data-filter]');
  if (!button) return;
  activeFilter = button.dataset.filter;
  filters.querySelectorAll('[data-filter]').forEach((filterButton) => {
    filterButton.setAttribute('aria-pressed', String(filterButton === button));
  });
  renderLogs();
});
searchInput.addEventListener('input', renderLogs);

document.querySelectorAll('[data-view]').forEach((button) => {
  button.addEventListener('click', () => {
    const view = button.dataset.view;
    document.getElementById('overview-view').hidden = view !== 'overview';
    document.getElementById('tasks-view').hidden = view !== 'tasks';
    document.querySelectorAll('[data-view]').forEach((navButton) => {
      navButton.setAttribute('aria-current', String(navButton === button));
    });
  });
});

renderChart();
initializeTaskManager();
fetchTelemetry();
window.setInterval(fetchTelemetry, 2500);
