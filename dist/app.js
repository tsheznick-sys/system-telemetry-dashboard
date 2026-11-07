import { randomUUID } from 'node:crypto';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import express from 'express';
import { rateLimit } from 'express-rate-limit';
import helmet from 'helmet';
import { faker } from '@faker-js/faker';
import { config } from './config.js';
const taskPriorities = new Set(['low', 'normal', 'high', 'urgent']);
const taskStatuses = new Set(['todo', 'in-progress', 'done']);
const defaultThresholds = { cpu: 85, memory: 85, errors: 1 };
const projectRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
function isTaskPriority(value) {
    return typeof value === 'string' && taskPriorities.has(value);
}
function isTaskStatus(value) {
    return typeof value === 'string' && taskStatuses.has(value);
}
function parseLimit(value, fallback, maximum) {
    if (typeof value !== 'string' || !/^\d+$/.test(value))
        return fallback;
    return Math.min(maximum, Math.max(1, Number(value)));
}
function isRecord(value) {
    return typeof value === 'object' && value !== null && !Array.isArray(value);
}
function isCalendarDate(value) {
    const timestamp = Date.parse(`${value}T00:00:00.000Z`);
    return Number.isFinite(timestamp) && new Date(timestamp).toISOString().slice(0, 10) === value;
}
function parseTask(body) {
    if (!isRecord(body))
        return null;
    const { title, description, priority, status, category, dueDate } = body;
    const hasDueDate = dueDate !== undefined && dueDate !== null && dueDate !== '';
    const validDate = !hasDueDate ||
        (typeof dueDate === 'string' && /^\d{4}-\d{2}-\d{2}$/.test(dueDate) && isCalendarDate(dueDate));
    if (typeof title !== 'string' ||
        title.trim().length === 0 ||
        title.trim().length > 100 ||
        (description !== undefined && (typeof description !== 'string' || description.length > 500)) ||
        !isTaskPriority(priority) ||
        !isTaskStatus(status) ||
        (category !== undefined && (typeof category !== 'string' || category.length > 32)) ||
        !validDate) {
        return null;
    }
    return {
        title: title.trim(),
        description: typeof description === 'string' ? description.trim() : '',
        priority,
        status,
        category: typeof category === 'string' ? category.trim() : '',
        dueDate: typeof dueDate === 'string' && dueDate ? dueDate : null,
    };
}
function parseThresholds(body) {
    if (!isRecord(body))
        return null;
    const { cpu, memory, errors } = body;
    if (typeof cpu !== 'number' ||
        !Number.isFinite(cpu) ||
        cpu < 1 ||
        cpu > 100 ||
        typeof memory !== 'number' ||
        !Number.isFinite(memory) ||
        memory < 1 ||
        memory > 100 ||
        typeof errors !== 'number' ||
        !Number.isFinite(errors) ||
        errors < 0.01 ||
        errors > 100) {
        return null;
    }
    return { cpu, memory, errors };
}
async function inTransaction(pool, action) {
    const client = await pool.connect();
    try {
        await client.query('BEGIN');
        const result = await action(client);
        await client.query('COMMIT');
        return result;
    }
    catch (error) {
        try {
            await client.query('ROLLBACK');
        }
        catch (rollbackError) {
            console.error('Database transaction rollback failed:', rollbackError);
        }
        throw error;
    }
    finally {
        client.release();
    }
}
function audit(client, userId, action, resourceType, resourceId, details = {}) {
    return client.query(`INSERT INTO audit_events (user_id, action, resource_type, resource_id, details)
     VALUES ($1, $2, $3, $4, $5)`, [userId, action, resourceType, resourceId, JSON.stringify(details)]);
}
export function createApp(dependencies) {
    const { pool, resolveSession } = dependencies;
    const app = express();
    const dashboardMode = Boolean(dependencies.dashboardMode);
    const demoUser = dependencies.demoUser ?? { id: 'demo-user', email: 'demo@local', name: 'Local Operator' };
    const demoSnapshot = {
        tasks: [
            {
                id: 'demo-task-1',
                title: 'Inspect cluster services',
                description: 'Confirm upstream dependencies and queue health for the current work window.',
                priority: 'high',
                status: 'in-progress',
                category: 'platform',
                dueDate: new Date(Date.now() + 86400000).toISOString().slice(0, 10),
            },
        ],
        settings: { ...defaultThresholds },
        history: [],
        events: [
            {
                id: 'demo-event-1',
                level: 'INFO',
                message: 'Dashboard-only mode initialized.',
                time: new Date().toLocaleTimeString(),
            },
        ],
        audit: [
            {
                id: 1,
                action: 'workspace.initialized',
                resourceType: 'dashboard',
                resourceId: null,
                occurredAt: new Date().toISOString(),
                details: { mode: 'demo' },
            },
        ],
    };
    const telemetryFactory = dependencies.telemetryFactory ??
        (() => ({
            timestamp: new Date().toISOString(),
            metrics: {
                cpuUsage: faker.number.float({ min: 10, max: 95, fractionDigits: 1 }),
                memoryUsage: faker.number.float({ min: 30, max: 85, fractionDigits: 1 }),
                activeConnections: faker.number.int({ min: 1200, max: 4500 }),
                errorRate: faker.number.float({ min: 0, max: 1.5, fractionDigits: 2 }),
            },
            activeNode: faker.system.networkInterface(),
            recentLogs: Array.from({ length: 5 }, () => ({
                id: randomUUID(),
                level: faker.helpers.arrayElement(['INFO', 'WARN', 'SUCCESS', 'DEBUG']),
                message: faker.hacker.phrase(),
                time: new Date().toLocaleTimeString(),
            })),
        }));
    app.disable('x-powered-by');
    app.set('trust proxy', config.isProduction ? 1 : false);
    app.use(helmet({
        contentSecurityPolicy: {
            directives: {
                defaultSrc: ["'self'"],
                scriptSrc: ["'self'"],
                styleSrc: ["'self'", "'unsafe-inline'"],
                imgSrc: ["'self'", 'data:'],
                connectSrc: ["'self'"],
                objectSrc: ["'none'"],
                frameAncestors: ["'none'"],
                upgradeInsecureRequests: config.isProduction ? [] : null,
            },
        },
        crossOriginEmbedderPolicy: false,
    }));
    app.use(express.json({ limit: '32kb' }));
    app.use(express.static(path.join(projectRoot, 'public'), { index: 'index.html' }));
    app.get('/api/health/live', (_req, res) => res.json({ status: 'ok' }));
    app.get('/api/health/ready', async (_req, res) => {
        if (dashboardMode) {
            res.json({ status: 'ready', mode: 'dashboard-demo' });
            return;
        }
        try {
            const { rows } = await pool.query(`SELECT to_regclass('"user"') AS auth_users, to_regclass('tasks') AS tasks`);
            if (!rows[0].auth_users || !rows[0].tasks) {
                res.status(503).json({ error: 'Database migrations have not been applied.' });
                return;
            }
            res.json({ status: 'ready' });
        }
        catch (error) {
            console.error('Readiness database check failed:', error);
            res.status(503).json({ error: 'Database is unavailable.' });
        }
    });
    app.get('/api/auth-options', (_req, res) => {
        res.json({
            googleEnabled: Boolean(config.googleClientId && config.googleClientSecret),
            passwordResetEnabled: Boolean(config.smtpHost && config.smtpUser && config.smtpPassword && config.smtpFrom),
        });
    });
    app.get('/api/auth/get-session', (_req, res) => {
        if (dashboardMode) {
            res.json({ user: demoUser });
            return;
        }
        res.status(401).json({ error: 'No active session.' });
    });
    if (dependencies.authHandler) {
        app.all('/api/auth/*', rateLimit({
            windowMs: 15 * 60 * 1000,
            limit: 50,
            standardHeaders: true,
            legacyHeaders: false,
        }), dependencies.authHandler);
    }
    const requireUser = async (req, res, next) => {
        if (dashboardMode) {
            res.locals.user = demoUser;
            next();
            return;
        }
        try {
            const session = await resolveSession(req.headers);
            if (!session) {
                res.status(401).json({ error: 'Sign in to continue.' });
                return;
            }
            res.locals.user = session.user;
            next();
        }
        catch (error) {
            console.error('Session lookup failed:', error);
            res.status(503).json({ error: 'Authentication service is unavailable.' });
        }
    };
    const sameOrigin = (req, res, next) => {
        const requestHeaders = [req.get('origin'), req.get('referer')].filter(Boolean);
        if (!requestHeaders.length) {
            next();
            return;
        }
        try {
            const appOrigin = new URL(config.baseUrl).origin;
            for (const requestHeader of requestHeaders) {
                if (new URL(requestHeader).origin !== appOrigin) {
                    res.status(403).json({ error: 'Cross-origin request rejected.' });
                    return;
                }
            }
        }
        catch {
            res.status(403).json({ error: 'Invalid request origin.' });
            return;
        }
        next();
    };
    const protectedApi = express.Router();
    protectedApi.use(requireUser, sameOrigin);
    protectedApi.get('/profile', (_req, res) => {
        const user = res.locals.user;
        res.json({
            id: user.id,
            name: user.name,
            email: user.email,
            isAdmin: config.adminEmails.has(user.email.toLowerCase()),
        });
    });
    protectedApi.get('/telemetry', async (_req, res) => {
        const user = res.locals.user;
        if (dashboardMode) {
            const telemetry = telemetryFactory();
            demoSnapshot.history.push({
                timestamp: Date.parse(telemetry.timestamp),
                cpuUsage: telemetry.metrics.cpuUsage,
                memoryUsage: telemetry.metrics.memoryUsage,
                activeConnections: telemetry.metrics.activeConnections,
                errorRate: telemetry.metrics.errorRate,
                activeNode: telemetry.activeNode,
            });
            demoSnapshot.history = demoSnapshot.history.slice(-1000);
            telemetry.recentLogs.forEach((log) => {
                demoSnapshot.events.unshift({
                    id: log.id,
                    level: log.level,
                    message: log.message,
                    time: log.time,
                });
            });
            demoSnapshot.events = demoSnapshot.events.slice(0, 50);
            demoSnapshot.audit.unshift({
                id: Date.now(),
                action: 'telemetry.refresh',
                resourceType: 'telemetry',
                resourceId: null,
                occurredAt: new Date().toISOString(),
                details: { userId: user.id },
            });
            res.json(telemetry);
            return;
        }
        try {
            const telemetry = telemetryFactory();
            await inTransaction(pool, async (client) => {
                await client.query(`INSERT INTO telemetry_samples
           (user_id, recorded_at, cpu_usage, memory_usage, active_connections, error_rate, active_node)
           VALUES ($1, $2, $3, $4, $5, $6, $7)`, [
                    user.id,
                    telemetry.timestamp,
                    telemetry.metrics.cpuUsage,
                    telemetry.metrics.memoryUsage,
                    telemetry.metrics.activeConnections,
                    telemetry.metrics.errorRate,
                    telemetry.activeNode,
                ]);
                for (const log of telemetry.recentLogs) {
                    await client.query(`INSERT INTO system_events (id, user_id, level, message, occurred_at)
             VALUES ($1, $2, $3, $4, $5)`, [log.id, user.id, log.level, log.message, telemetry.timestamp]);
                }
            });
            res.json(telemetry);
        }
        catch (error) {
            console.error('Unable to persist telemetry sample:', error);
            res.status(503).json({ error: 'Telemetry could not be stored.' });
        }
    });
    protectedApi.get('/telemetry/history', async (req, res) => {
        if (dashboardMode) {
            const limit = parseLimit(req.query.limit, 1000, 1000);
            res.json(demoSnapshot.history.slice(-limit));
            return;
        }
        const user = res.locals.user;
        const limit = parseLimit(req.query.limit, 1000, 1000);
        try {
            const result = await pool.query(`SELECT recorded_at, cpu_usage, memory_usage, active_connections, error_rate, active_node
         FROM telemetry_samples WHERE user_id = $1
         ORDER BY recorded_at DESC LIMIT $2`, [user.id, limit]);
            res.json(result.rows.reverse().map((row) => ({
                timestamp: Date.parse(row.recorded_at),
                cpuUsage: row.cpu_usage,
                memoryUsage: row.memory_usage,
                activeConnections: row.active_connections,
                errorRate: row.error_rate,
                activeNode: row.active_node,
            })));
        }
        catch (error) {
            console.error('Unable to read telemetry history:', error);
            res.status(503).json({ error: 'Telemetry history is unavailable.' });
        }
    });
    protectedApi.get('/events', async (req, res) => {
        if (dashboardMode) {
            const limit = parseLimit(req.query.limit, 50, 200);
            res.json(demoSnapshot.events.slice(0, limit));
            return;
        }
        const user = res.locals.user;
        const limit = parseLimit(req.query.limit, 50, 200);
        try {
            const result = await pool.query(`SELECT id, level, message, occurred_at
         FROM system_events WHERE user_id = $1
         ORDER BY occurred_at DESC LIMIT $2`, [user.id, limit]);
            res.json(result.rows.map((row) => ({
                id: row.id,
                level: row.level,
                message: row.message,
                time: new Date(row.occurred_at).toLocaleTimeString(),
            })));
        }
        catch (error) {
            console.error('Unable to read system events:', error);
            res.status(503).json({ error: 'System events are unavailable.' });
        }
    });
    protectedApi.get('/tasks', async (_req, res) => {
        if (dashboardMode) {
            res.json(demoSnapshot.tasks);
            return;
        }
        const user = res.locals.user;
        try {
            const result = await pool.query(`SELECT id, title, description, priority, status, category,
                to_char(due_date, 'YYYY-MM-DD') AS "dueDate"
         FROM tasks WHERE user_id = $1 ORDER BY updated_at DESC`, [user.id]);
            res.json(result.rows);
        }
        catch (error) {
            console.error('Unable to read tasks:', error);
            res.status(503).json({ error: 'Tasks are unavailable.' });
        }
    });
    protectedApi.post('/tasks', async (req, res) => {
        const task = parseTask(req.body);
        if (!task) {
            res.status(400).json({ error: 'Invalid task. Check the title, status, priority, and date.' });
            return;
        }
        if (dashboardMode) {
            const created = {
                id: randomUUID(),
                ...task,
            };
            demoSnapshot.tasks.unshift(created);
            demoSnapshot.audit.unshift({
                id: Date.now(),
                action: 'task.created',
                resourceType: 'task',
                resourceId: created.id,
                occurredAt: new Date().toISOString(),
                details: { title: task.title, status: task.status },
            });
            res.status(201).json(created);
            return;
        }
        const user = res.locals.user;
        const id = randomUUID();
        try {
            const created = await inTransaction(pool, async (client) => {
                const result = await client.query(`INSERT INTO tasks (id, user_id, title, description, priority, status, category, due_date)
           VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
           RETURNING id, title, description, priority, status, category,
                     to_char(due_date, 'YYYY-MM-DD') AS "dueDate"`, [
                    id,
                    user.id,
                    task.title,
                    task.description,
                    task.priority,
                    task.status,
                    task.category,
                    task.dueDate,
                ]);
                await audit(client, user.id, 'task.created', 'task', id, { title: task.title });
                return result.rows[0];
            });
            res.status(201).json(created);
        }
        catch (error) {
            console.error('Unable to create task:', error);
            res.status(503).json({ error: 'Task could not be created.' });
        }
    });
    protectedApi.patch('/tasks/:id', async (req, res) => {
        const task = parseTask(req.body);
        if (!task || !/^[\w-]{1,80}$/.test(req.params.id)) {
            res.status(400).json({ error: 'Invalid task update.' });
            return;
        }
        if (dashboardMode) {
            const index = demoSnapshot.tasks.findIndex((entry) => entry.id === req.params.id);
            if (index === -1) {
                res.status(404).json({ error: 'Task not found.' });
                return;
            }
            const updated = { ...demoSnapshot.tasks[index], ...task };
            demoSnapshot.tasks[index] = updated;
            demoSnapshot.audit.unshift({
                id: Date.now(),
                action: 'task.updated',
                resourceType: 'task',
                resourceId: req.params.id,
                occurredAt: new Date().toISOString(),
                details: { title: task.title, status: task.status },
            });
            res.json(updated);
            return;
        }
        const user = res.locals.user;
        try {
            const updated = await inTransaction(pool, async (client) => {
                const result = await client.query(`UPDATE tasks SET title = $3, description = $4, priority = $5, status = $6,
             category = $7, due_date = $8, updated_at = now()
           WHERE id = $1 AND user_id = $2
           RETURNING id, title, description, priority, status, category,
                     to_char(due_date, 'YYYY-MM-DD') AS "dueDate"`, [
                    req.params.id,
                    user.id,
                    task.title,
                    task.description,
                    task.priority,
                    task.status,
                    task.category,
                    task.dueDate,
                ]);
                if (result.rowCount) {
                    await audit(client, user.id, 'task.updated', 'task', req.params.id, {
                        title: task.title,
                        status: task.status,
                    });
                }
                return result.rows[0];
            });
            if (!updated) {
                res.status(404).json({ error: 'Task not found.' });
                return;
            }
            res.json(updated);
        }
        catch (error) {
            console.error('Unable to update task:', error);
            res.status(503).json({ error: 'Task could not be updated.' });
        }
    });
    protectedApi.delete('/tasks/:id', async (req, res) => {
        if (!/^[\w-]{1,80}$/.test(req.params.id)) {
            res.status(400).json({ error: 'Invalid task ID.' });
            return;
        }
        if (dashboardMode) {
            const initialLength = demoSnapshot.tasks.length;
            demoSnapshot.tasks = demoSnapshot.tasks.filter((entry) => entry.id !== req.params.id);
            if (demoSnapshot.tasks.length === initialLength) {
                res.status(404).json({ error: 'Task not found.' });
                return;
            }
            demoSnapshot.audit.unshift({
                id: Date.now(),
                action: 'task.deleted',
                resourceType: 'task',
                resourceId: req.params.id,
                occurredAt: new Date().toISOString(),
                details: { removed: true },
            });
            res.status(204).end();
            return;
        }
        const user = res.locals.user;
        try {
            const removed = await inTransaction(pool, async (client) => {
                const result = await client.query('DELETE FROM tasks WHERE id = $1 AND user_id = $2 RETURNING title', [req.params.id, user.id]);
                if (result.rowCount) {
                    await audit(client, user.id, 'task.deleted', 'task', req.params.id, {
                        title: result.rows[0].title,
                    });
                }
                return result.rowCount;
            });
            if (!removed) {
                res.status(404).json({ error: 'Task not found.' });
                return;
            }
            res.status(204).end();
        }
        catch (error) {
            console.error('Unable to delete task:', error);
            res.status(503).json({ error: 'Task could not be deleted.' });
        }
    });
    protectedApi.get('/settings', async (_req, res) => {
        if (dashboardMode) {
            res.json(demoSnapshot.settings);
            return;
        }
        const user = res.locals.user;
        try {
            const result = await pool.query('SELECT thresholds FROM user_settings WHERE user_id = $1', [
                user.id,
            ]);
            res.json(result.rows[0]?.thresholds ?? defaultThresholds);
        }
        catch (error) {
            console.error('Unable to read settings:', error);
            res.status(503).json({ error: 'Settings are unavailable.' });
        }
    });
    protectedApi.put('/settings', async (req, res) => {
        const thresholds = parseThresholds(req.body);
        if (!thresholds) {
            res.status(400).json({ error: 'Invalid alert thresholds.' });
            return;
        }
        if (dashboardMode) {
            demoSnapshot.settings = thresholds;
            demoSnapshot.audit.unshift({
                id: Date.now(),
                action: 'settings.updated',
                resourceType: 'settings',
                resourceId: demoUser.id,
                occurredAt: new Date().toISOString(),
                details: thresholds,
            });
            res.json(thresholds);
            return;
        }
        const user = res.locals.user;
        try {
            await inTransaction(pool, async (client) => {
                await client.query(`INSERT INTO user_settings (user_id, thresholds, updated_at)
           VALUES ($1, $2, now())
           ON CONFLICT (user_id) DO UPDATE SET thresholds = EXCLUDED.thresholds, updated_at = now()`, [user.id, JSON.stringify(thresholds)]);
                await audit(client, user.id, 'settings.updated', 'settings', user.id, thresholds);
            });
            res.json(thresholds);
        }
        catch (error) {
            console.error('Unable to update settings:', error);
            res.status(503).json({ error: 'Settings could not be saved.' });
        }
    });
    protectedApi.get('/audit', async (req, res) => {
        if (dashboardMode) {
            const limit = parseLimit(req.query.limit, 50, 100);
            res.json(demoSnapshot.audit.slice(0, limit));
            return;
        }
        const user = res.locals.user;
        const limit = parseLimit(req.query.limit, 50, 100);
        try {
            const result = await pool.query(`SELECT id, action, resource_type AS "resourceType", resource_id AS "resourceId",
                details, occurred_at AS "occurredAt"
         FROM audit_events WHERE user_id = $1 ORDER BY occurred_at DESC LIMIT $2`, [user.id, limit]);
            res.json(result.rows);
        }
        catch (error) {
            console.error('Unable to read audit history:', error);
            res.status(503).json({ error: 'Audit history is unavailable.' });
        }
    });
    protectedApi.post('/admin/sso/providers', async (req, res) => {
        const user = res.locals.user;
        if (!config.adminEmails.has(user.email.toLowerCase())) {
            res.status(403).json({ error: 'Administrator access is required.' });
            return;
        }
        if (!dependencies.registerSsoProvider) {
            res.status(503).json({ error: 'SSO provider management is unavailable.' });
            return;
        }
        const body = req.body;
        if (!isRecord(body) ||
            typeof body.providerId !== 'string' ||
            !/^[a-zA-Z0-9_-]{2,64}$/.test(body.providerId) ||
            typeof body.domain !== 'string' ||
            !/^(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$/.test(body.domain) ||
            typeof body.issuer !== 'string' ||
            body.issuer.length > 2048) {
            res.status(400).json({ error: 'Invalid SSO provider configuration.' });
            return;
        }
        let providerInput;
        if (body.type === 'oidc') {
            if (!isRecord(body.oidcConfig) ||
                typeof body.oidcConfig.clientId !== 'string' ||
                typeof body.oidcConfig.clientSecret !== 'string' ||
                typeof body.oidcConfig.discoveryEndpoint !== 'string' ||
                !body.oidcConfig.discoveryEndpoint.startsWith('https://')) {
                res
                    .status(400)
                    .json({ error: 'OIDC requires a client ID, secret, and HTTPS discovery URL.' });
                return;
            }
            providerInput = {
                providerId: body.providerId,
                issuer: body.issuer,
                domain: body.domain.toLowerCase(),
                type: 'oidc',
                oidcConfig: {
                    clientId: body.oidcConfig.clientId,
                    clientSecret: body.oidcConfig.clientSecret,
                    discoveryEndpoint: body.oidcConfig.discoveryEndpoint,
                    scopes: ['openid', 'email', 'profile'],
                    pkce: true,
                },
            };
        }
        else if (body.type === 'saml') {
            if (!isRecord(body.samlConfig) ||
                typeof body.samlConfig.entryPoint !== 'string' ||
                !body.samlConfig.entryPoint.startsWith('https://') ||
                typeof body.samlConfig.cert !== 'string' ||
                body.samlConfig.cert.length > 16384) {
                res
                    .status(400)
                    .json({ error: 'SAML requires an HTTPS entry point and signing certificate.' });
                return;
            }
            providerInput = {
                providerId: body.providerId,
                issuer: body.issuer,
                domain: body.domain.toLowerCase(),
                type: 'saml',
                samlConfig: {
                    entryPoint: body.samlConfig.entryPoint,
                    cert: body.samlConfig.cert,
                    audience: typeof body.samlConfig.audience === 'string' ? body.samlConfig.audience : undefined,
                    wantAssertionsSigned: true,
                },
            };
        }
        else {
            res.status(400).json({ error: 'SSO type must be oidc or saml.' });
            return;
        }
        const providerId = body.providerId;
        const providerType = body.type;
        const providerDomain = body.domain.toLowerCase();
        let providerRegistered = false;
        try {
            const registration = await dependencies.registerSsoProvider(providerInput, req.headers);
            providerRegistered = true;
            await inTransaction(pool, (client) => audit(client, user.id, 'sso.provider.registered', 'sso_provider', providerId, {
                type: providerType,
                domain: providerDomain,
            }));
            res.status(201).json({
                providerId,
                type: providerType,
                domain: providerDomain,
                callbackUrl: providerType === 'oidc'
                    ? `${config.baseUrl}/api/auth/sso/callback/${encodeURIComponent(providerId)}`
                    : undefined,
                metadataUrl: providerType === 'saml'
                    ? isRecord(registration) && typeof registration.spMetadataUrl === 'string'
                        ? registration.spMetadataUrl
                        : `${config.baseUrl}/api/auth/sso/saml2/sp/metadata?providerId=${encodeURIComponent(providerId)}`
                    : undefined,
            });
        }
        catch (error) {
            console.error('Unable to register SSO provider:', error instanceof Error ? error.name : 'Unknown error');
            res.status(providerRegistered ? 503 : 400).json({
                error: providerRegistered
                    ? 'The provider was registered, but its audit record could not be saved.'
                    : 'SSO provider could not be registered.',
            });
        }
    });
    app.use('/api', rateLimit({ windowMs: 60 * 1000, limit: 120, standardHeaders: true, legacyHeaders: false }), protectedApi);
    const notFound = (_req, res) => {
        res.status(404).json({ error: 'Not found.' });
    };
    const errorHandler = (error, _req, res, _next) => {
        console.error('Unhandled request error:', error);
        const statusCode = isRecord(error) ? error.status : undefined;
        const status = typeof statusCode === 'number' && statusCode >= 400 && statusCode < 500 ? statusCode : 500;
        res.status(status).json({
            error: status === 413
                ? 'Request body is too large.'
                : status === 400
                    ? 'Invalid request.'
                    : 'An unexpected server error occurred.',
        });
    };
    app.use(notFound, errorHandler);
    return app;
}
