import assert from 'node:assert/strict';
import { test } from 'node:test';
import request from 'supertest';
import app from '../src/server.js';

test('GET /api/telemetry returns the expected telemetry structure and ranges', async () => {
  const response = await request(app).get('/api/telemetry');

  assert.equal(response.status, 200);
  assert.ok(Number.isFinite(Date.parse(response.body.timestamp)));
  assert.deepEqual(Object.keys(response.body.metrics).sort(), [
    'activeConnections',
    'cpuUsage',
    'errorRate',
    'memoryUsage',
  ]);
  assert.ok(response.body.metrics.cpuUsage >= 10 && response.body.metrics.cpuUsage <= 95);
  assert.ok(response.body.metrics.memoryUsage >= 30 && response.body.metrics.memoryUsage <= 85);
  assert.ok(
    response.body.metrics.activeConnections >= 1200 &&
      response.body.metrics.activeConnections <= 4500,
  );
  assert.ok(response.body.metrics.errorRate >= 0 && response.body.metrics.errorRate <= 1.5);
  assert.equal(typeof response.body.activeNode, 'string');
  assert.equal(response.body.recentLogs.length, 5);
  assert.deepEqual(Object.keys(response.body.recentLogs[0]).sort(), [
    'id',
    'level',
    'message',
    'time',
  ]);
  assert.match(response.body.recentLogs[0].level, /^(INFO|WARN|SUCCESS|DEBUG)$/);
  assert.equal(typeof response.body.recentLogs[0].message, 'string');
  assert.equal(typeof response.body.recentLogs[0].time, 'string');
});
