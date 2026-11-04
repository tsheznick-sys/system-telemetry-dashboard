import { Pool } from 'pg';
import { config } from '../config.js';

const max = Number(process.env.DATABASE_POOL_SIZE ?? 10);
if (!Number.isInteger(max) || max < 1 || max > 100) {
  throw new Error('DATABASE_POOL_SIZE must be an integer between 1 and 100.');
}

let connectionString: string | undefined;
let useTls = config.isProduction;
if (config.databaseUrl) {
  const connectionUrl = new URL(config.databaseUrl);
  const sslMode = connectionUrl.searchParams.get('sslmode')?.toLowerCase();
  if (config.isProduction && sslMode === 'disable') {
    throw new Error('TLS cannot be disabled for the production database connection.');
  }
  useTls ||= Boolean(sslMode && sslMode !== 'disable');
  connectionUrl.searchParams.delete('sslmode');
  connectionString = connectionUrl.toString();
}

export const pool = new Pool({
  connectionString,
  max,
  idleTimeoutMillis: 30_000,
  connectionTimeoutMillis: 5_000,
  ssl: useTls ? { rejectUnauthorized: true } : undefined,
});

pool.on('error', (error) => {
  console.error('Unexpected idle PostgreSQL client error:', error.message);
});
