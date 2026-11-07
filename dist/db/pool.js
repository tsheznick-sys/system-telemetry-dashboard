import { Pool } from 'pg';
import { config } from '../config.js';
const max = Number(process.env.DATABASE_POOL_SIZE ?? 10);
if (!Number.isInteger(max) || max < 1 || max > 100) {
    throw new Error('DATABASE_POOL_SIZE must be an integer between 1 and 100.');
}
const pool = config.dashboardMode
    ? {
        async query() {
            return { rows: [], rowCount: 0 };
        },
        async connect() {
            return {
                async query() {
                    return { rows: [], rowCount: 0 };
                },
                release() { },
            };
        },
        async end() { },
    }
    : (() => {
        let connectionString;
        let useTls = config.isProduction;
        if (config.databaseUrl) {
            const connectionUrl = new URL(config.databaseUrl);
            const sslMode = connectionUrl.searchParams.get('sslmode')?.toLowerCase();
            if (config.isProduction && sslMode === 'disable') {
                throw new Error('TLS cannot be disabled for the production database connection.');
            }
            useTls || (useTls = Boolean(sslMode && sslMode !== 'disable'));
            connectionUrl.searchParams.delete('sslmode');
            connectionString = connectionUrl.toString();
        }
        const postgresPool = new Pool({
            connectionString,
            max,
            idleTimeoutMillis: 30000,
            connectionTimeoutMillis: 5000,
            ssl: useTls ? { rejectUnauthorized: true } : undefined,
        });
        postgresPool.on('error', (error) => {
            console.error('Unexpected idle PostgreSQL client error:', error.message);
        });
        return postgresPool;
    })();
export { pool };
