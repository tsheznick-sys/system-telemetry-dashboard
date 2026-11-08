import 'dotenv/config';
import express from 'express';
import path from 'path';
import { faker } from '@faker-js/faker';

const app = express();

app.use(express.json());
app.use(express.static(path.join(process.cwd(), 'public')));

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

if (require.main === module) {
  const port = Number(process.env.PORT ?? 3000);
  app.listen(port, () => {
    console.log(`Cloud Telemetry Engine running on port ${port}`);
  });
}

export default app;
