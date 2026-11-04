import 'dotenv/config';
import express from 'express';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { faker } from '@faker-js/faker';

const app = express();
const projectRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');

app.use(express.json());
app.use(express.static(path.join(projectRoot, 'public')));

app.get('/api/telemetry', (_req, res) => {
  const telemetryData = {
    timestamp: new Date().toISOString(),
    metrics: {
      cpuUsage: faker.number.float({ min: 10, max: 95, fractionDigits: 1 }),
      memoryUsage: faker.number.float({ min: 30, max: 85, fractionDigits: 1 }),
      activeConnections: faker.number.int({ min: 1200, max: 4500 }),
      errorRate: faker.number.float({ min: 0, max: 1.5, fractionDigits: 2 }),
    },
    activeNode: faker.system.networkInterface(),
    recentLogs: Array.from({ length: 5 }, () => ({
      id: faker.string.uuid(),
      level: faker.helpers.arrayElement(['INFO', 'WARN', 'SUCCESS', 'DEBUG']),
      message: faker.hacker.phrase(),
      time: faker.date.recent().toLocaleTimeString(),
    })),
  };

  res.json(telemetryData);
});

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const port = Number(process.env.PORT ?? 3000);
  app.listen(port, () => {
    console.log(`Cloud Telemetry Engine running on port ${port}`);
  });
}

export default app;
