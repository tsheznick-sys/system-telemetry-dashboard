import request from 'supertest';
import app from './server';

describe('GET /api/telemetry', () => {
  it('returns a timestamp, metrics, active node, and recent logs', async () => {
    const response = await request(app).get('/api/telemetry');

    expect(response.status).toBe(200);
    expect(Number.isNaN(Date.parse(response.body.timestamp))).toBe(false);
    expect(response.body.metrics).toEqual({
      cpuUsage: expect.any(Number),
      memoryUsage: expect.any(Number),
      activeConnections: expect.any(Number),
      errorRate: expect.any(Number),
    });
    expect(response.body.metrics.cpuUsage).toBeGreaterThanOrEqual(10);
    expect(response.body.metrics.cpuUsage).toBeLessThanOrEqual(95);
    expect(response.body.metrics.memoryUsage).toBeGreaterThanOrEqual(30);
    expect(response.body.metrics.memoryUsage).toBeLessThanOrEqual(85);
    expect(response.body.metrics.activeConnections).toBeGreaterThanOrEqual(1200);
    expect(response.body.metrics.activeConnections).toBeLessThanOrEqual(4500);
    expect(response.body.metrics.errorRate).toBeGreaterThanOrEqual(0);
    expect(response.body.metrics.errorRate).toBeLessThanOrEqual(1.5);
    expect(response.body.activeNode).toEqual(expect.any(String));
    expect(response.body.recentLogs).toHaveLength(5);
    expect(response.body.recentLogs[0]).toEqual({
      id: expect.any(String),
      level: expect.stringMatching(/^(INFO|WARN|SUCCESS|DEBUG)$/),
      message: expect.any(String),
      time: expect.any(String),
    });
  });
});
