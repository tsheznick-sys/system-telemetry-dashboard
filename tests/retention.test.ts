import assert from 'node:assert/strict';
import { test } from 'node:test';
import type { Pool } from 'pg';
import { cleanupExpiredData } from '../src/db/retention.js';

test('retention cleanup deletes only telemetry and system events older than 30 days', async () => {
  let executedSql = '';
  const database = {
    async query(sql: string) {
      executedSql = sql;
      return { rows: [{ samples: '12', events: '7' }], rowCount: 1 };
    },
  };
  const result = await cleanupExpiredData(database as unknown as Pick<Pool, 'query'>);

  assert.deepEqual(result, { samples: 12, events: 7 });
  assert.equal((executedSql.match(/interval '30 days'/g) ?? []).length, 2);
  assert.match(executedSql, /DELETE FROM telemetry_samples/);
  assert.match(executedSql, /DELETE FROM system_events/);
  assert.doesNotMatch(executedSql, /DELETE FROM audit_events/);
});
