import 'dotenv/config';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { fromNodeHeaders, toNodeHandler } from 'better-auth/node';
import { auth, resolveSession } from './auth.js';
import { createApp } from './app.js';
import { config } from './config.js';
import { pool } from './db/pool.js';
import { cleanupExpiredData } from './db/retention.js';

const app = createApp({
  pool,
  resolveSession,
  authHandler: toNodeHandler(auth),
  registerSsoProvider: (body, headers) =>
    auth.api.registerSSOProvider({ body, headers: fromNodeHeaders(headers) }),
});

async function startServer() {
  const { rows } = await pool.query(
    `SELECT to_regclass('"user"') AS auth_users, to_regclass('tasks') AS tasks`,
  );
  if (!rows[0].auth_users || !rows[0].tasks) {
    throw new Error('Database migrations are missing. Run npm run db:migrate before starting.');
  }
  const server = app.listen(config.port, () => {
    console.log(`Pulse Compute Operations listening on port ${config.port}.`);
  });
  const cleanup = async () => {
    try {
      const { samples, events } = await cleanupExpiredData(pool);
      if (samples || events) {
        console.info(`30-day retention removed ${samples} telemetry samples and ${events} events.`);
      }
    } catch (error) {
      console.error('30-day retention cleanup failed:', error);
    }
  };
  const retentionTimer = setInterval(cleanup, 24 * 60 * 60 * 1000);
  retentionTimer.unref();
  await cleanup();

  const shutdown = () => {
    clearInterval(retentionTimer);
    server.close(() => {
      void pool.end();
    });
  };
  process.once('SIGINT', shutdown);
  process.once('SIGTERM', shutdown);
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  startServer().catch(async (error: unknown) => {
    console.error('Unable to start Pulse Compute Operations:', error);
    await pool.end();
    process.exitCode = 1;
  });
}

export default app;
