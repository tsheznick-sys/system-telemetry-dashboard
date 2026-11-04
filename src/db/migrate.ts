import { readdir, readFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { pool } from './pool.js';

const directory = path.join(path.dirname(fileURLToPath(import.meta.url)), 'migrations');
const migrations = (await readdir(directory))
  .filter((name) => /^\d+_[a-z0-9_-]+\.sql$/i.test(name))
  .sort();
const client = await pool.connect();

try {
  for (const name of migrations) {
    const sql = await readFile(path.join(directory, name), 'utf8');
    await client.query('BEGIN');
    try {
      await client.query('SELECT pg_advisory_xact_lock(718374652)');
      await client.query(`CREATE TABLE IF NOT EXISTS app_migrations (
        name text PRIMARY KEY,
        applied_at timestamptz NOT NULL DEFAULT now()
      )`);
      const existing = await client.query('SELECT 1 FROM app_migrations WHERE name = $1', [name]);
      if (existing.rowCount) {
        await client.query('COMMIT');
        console.log(`Application migration ${name} is already applied.`);
        continue;
      }
      await client.query(sql);
      await client.query('INSERT INTO app_migrations (name) VALUES ($1)', [name]);
      await client.query('COMMIT');
      console.log(`Applied application migration ${name}.`);
    } catch (error) {
      await client.query('ROLLBACK');
      throw error;
    }
  }
} catch (error) {
  console.error('Application database migration failed:', error);
  process.exitCode = 1;
} finally {
  client.release();
  await pool.end();
}
