import assert from 'node:assert/strict';
import { test } from 'node:test';
import request from 'supertest';
import type { Pool } from 'pg';
import { createApp } from '../src/app.js';

function createTestApp(onRegisterSso?: () => Promise<unknown>) {
  const queries: Array<{ sql: string; values?: unknown[] }> = [];
  const client = {
    async query(sql: string, values?: unknown[]) {
      queries.push({ sql, values });
      if (sql.includes('INSERT INTO tasks')) {
        return {
          rows: [
            {
              id: 'task-1',
              title: 'Review compute capacity',
              description: '',
              priority: 'high',
              status: 'todo',
              category: '',
              dueDate: null,
            },
          ],
          rowCount: 1,
        };
      }
      return { rows: [], rowCount: 1 };
    },
    release() {},
  };
  const pool = {
    async query(sql: string, values?: unknown[]) {
      queries.push({ sql, values });
      if (sql.includes('to_regclass')) {
        return { rows: [{ auth_users: 'user', tasks: 'tasks' }], rowCount: 1 };
      }
      return { rows: [], rowCount: 1 };
    },
    async connect() {
      return client;
    },
  };
  const app = createApp({
    pool: pool as unknown as Pool,
    resolveSession: async (headers) => {
      const userId = headers['x-test-user'];
      return typeof userId === 'string'
        ? { user: { id: userId, email: `${userId}@example.com`, name: 'Test Operator' } }
        : null;
    },
    registerSsoProvider: onRegisterSso ? async () => onRegisterSso() : undefined,
    telemetryFactory: () => ({
      timestamp: '2025-01-01T00:00:00.000Z',
      metrics: { cpuUsage: 45.2, memoryUsage: 60.5, activeConnections: 2500, errorRate: 0.1 },
      activeNode: 'node-test',
      recentLogs: [{ id: 'log-1', level: 'INFO', message: 'Test event', time: '12:00:00 AM' }],
    }),
  });
  return { app, queries };
}

test('GET /api/health/live returns a liveness response without requiring a database', async () => {
  const { app } = createTestApp();
  const response = await request(app).get('/api/health/live');
  assert.equal(response.status, 200);
  assert.deepEqual(response.body, { status: 'ok' });
});

test('GET / serves the authenticated dashboard without third-party scripts', async () => {
  const { app } = createTestApp();
  const response = await request(app).get('/');
  assert.equal(response.status, 200);
  assert.match(response.text, /id="auth-screen"/);
  assert.match(response.text, /id="task-dialog"/);
  assert.doesNotMatch(response.text, /cdn\.tailwindcss\.com/);
});

test('GET /api/health/ready verifies the migrated database schema', async () => {
  const { app } = createTestApp();
  const response = await request(app).get('/api/health/ready');
  assert.equal(response.status, 200);
  assert.deepEqual(response.body, { status: 'ready' });
});

test('account data endpoints reject requests without an authenticated session', async () => {
  const { app, queries } = createTestApp();
  const response = await request(app).get('/api/tasks');
  assert.equal(response.status, 401);
  assert.deepEqual(response.body, { error: 'Sign in to continue.' });
  assert.equal(queries.length, 0);
});

test('task reads are scoped to the authenticated user', async () => {
  const { app, queries } = createTestApp();
  const response = await request(app).get('/api/tasks').set('x-test-user', 'user-42');
  assert.equal(response.status, 200);
  const taskQuery = queries.find((query) => query.sql.includes('FROM tasks'));
  assert.equal(taskQuery?.values?.[0], 'user-42');
});

test('mutations reject cross-origin requests and unprivileged SSO administration', async () => {
  let ssoRegistrationCount = 0;
  const { app } = createTestApp(async () => {
    ssoRegistrationCount++;
    return {};
  });
  const originResponse = await request(app)
    .put('/api/settings')
    .set('x-test-user', 'user-42')
    .set('Origin', 'https://other.example')
    .send({ cpu: 80, memory: 80, errors: 1 });
  assert.equal(originResponse.status, 403);

  const ssoResponse = await request(app)
    .post('/api/admin/sso/providers')
    .set('x-test-user', 'user-42')
    .send({});
  assert.equal(ssoResponse.status, 403);
  assert.equal(ssoRegistrationCount, 0);
});

test('GET /api/telemetry persists user-scoped samples and system events', async () => {
  const { app, queries } = createTestApp();
  const response = await request(app).get('/api/telemetry').set('x-test-user', 'user-42');

  assert.equal(response.status, 200);
  assert.ok(Number.isFinite(Date.parse(response.body.timestamp)));
  assert.deepEqual(response.body.metrics, {
    cpuUsage: 45.2,
    memoryUsage: 60.5,
    activeConnections: 2500,
    errorRate: 0.1,
  });
  assert.equal(response.body.recentLogs.length, 1);
  assert.ok(queries.some((query) => query.sql.includes('INSERT INTO telemetry_samples')));
  assert.ok(queries.some((query) => query.sql.includes('INSERT INTO system_events')));
  assert.ok(queries.some((query) => query.values?.includes('user-42')));
});

test('task creation validates input and writes audit records under the current user', async () => {
  const { app, queries } = createTestApp();
  const invalid = await request(app).post('/api/tasks').set('x-test-user', 'user-42').send({
    title: 'Broken due date',
    description: '',
    priority: 'normal',
    status: 'todo',
    dueDate: '2025-02-31',
  });
  assert.equal(invalid.status, 400);

  const created = await request(app).post('/api/tasks').set('x-test-user', 'user-42').send({
    title: 'Review compute capacity',
    description: '',
    priority: 'high',
    status: 'todo',
    category: '',
    dueDate: '',
  });
  assert.equal(created.status, 201);
  assert.equal(created.body.id, 'task-1');
  assert.ok(queries.some((query) => query.sql.includes('INSERT INTO audit_events')));
  const taskInsert = queries.find((query) => query.sql.includes('INSERT INTO tasks'));
  assert.equal(taskInsert?.values?.[1], 'user-42');
});
