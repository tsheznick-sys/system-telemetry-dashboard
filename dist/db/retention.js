import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { pool } from './pool.js';
export async function cleanupExpiredData(database = pool) {
    const result = await database.query(`WITH deleted_samples AS (
       DELETE FROM telemetry_samples WHERE recorded_at < now() - interval '30 days'
       RETURNING 1
     ),
     deleted_events AS (
       DELETE FROM system_events WHERE occurred_at < now() - interval '30 days'
       RETURNING 1
     )
     SELECT
       (SELECT count(*) FROM deleted_samples)::bigint AS samples,
       (SELECT count(*) FROM deleted_events)::bigint AS events`);
    const row = result.rows[0] ?? { samples: 0, events: 0 };
    return {
        samples: Number(row.samples ?? 0),
        events: Number(row.events ?? 0),
    };
}
if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
    try {
        const result = await cleanupExpiredData();
        console.log(`Retention cleanup removed ${result.samples} telemetry samples and ${result.events} events.`);
    }
    catch (error) {
        console.error('Retention cleanup failed:', error);
        process.exitCode = 1;
    }
    finally {
        await pool.end();
    }
}
