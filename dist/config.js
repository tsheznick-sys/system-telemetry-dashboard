import 'dotenv/config';
import { randomBytes } from 'node:crypto';
const isProduction = process.env.NODE_ENV === 'production';
function requiredProductionValue(name, value) {
    if (isProduction && !value) {
        throw new Error(`${name} must be configured in production.`);
    }
    return value ?? '';
}
export const config = {
    isProduction,
    dashboardMode: process.env.DEMO_MODE === 'true' ||
        process.env.DASHBOARD_ONLY === 'true' ||
        (!process.env.DATABASE_URL && !isProduction),
    port: Number(process.env.PORT ?? 3000),
    databaseUrl: requiredProductionValue('DATABASE_URL', process.env.DATABASE_URL),
    authSecret: requiredProductionValue('BETTER_AUTH_SECRET', process.env.BETTER_AUTH_SECRET) ||
        randomBytes(32).toString('base64url'),
    baseUrl: process.env.BETTER_AUTH_URL ?? `http://localhost:${process.env.PORT ?? 3000}`,
    adminEmails: new Set((process.env.ADMIN_EMAILS ?? '')
        .split(',')
        .map((email) => email.trim().toLowerCase())
        .filter(Boolean)),
    googleClientId: process.env.GOOGLE_CLIENT_ID,
    googleClientSecret: process.env.GOOGLE_CLIENT_SECRET,
    smtpHost: process.env.SMTP_HOST,
    smtpPort: Number(process.env.SMTP_PORT ?? 587),
    smtpUser: process.env.SMTP_USER,
    smtpPassword: process.env.SMTP_PASSWORD,
    smtpFrom: process.env.SMTP_FROM,
};
let parsedBaseUrl;
try {
    parsedBaseUrl = new URL(config.baseUrl);
}
catch {
    throw new Error('BETTER_AUTH_URL must be an absolute URL.');
}
if (!['http:', 'https:'].includes(parsedBaseUrl.protocol) ||
    parsedBaseUrl.pathname !== '/' ||
    parsedBaseUrl.search ||
    parsedBaseUrl.hash ||
    parsedBaseUrl.username ||
    parsedBaseUrl.password) {
    throw new Error('BETTER_AUTH_URL must be an HTTP(S) origin without a path or query.');
}
if (process.env.BETTER_AUTH_SECRET && process.env.BETTER_AUTH_SECRET.length < 32) {
    throw new Error('BETTER_AUTH_SECRET must contain at least 32 characters.');
}
if (Boolean(config.googleClientId) !== Boolean(config.googleClientSecret)) {
    throw new Error('Google OAuth requires both GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET.');
}
const smtpValues = [config.smtpHost, config.smtpUser, config.smtpPassword, config.smtpFrom];
if (smtpValues.some(Boolean) && !smtpValues.every(Boolean)) {
    throw new Error('SMTP_HOST, SMTP_USER, SMTP_PASSWORD, and SMTP_FROM must be configured together.');
}
if (config.databaseUrl && !/^postgres(?:ql)?:\/\//i.test(config.databaseUrl)) {
    throw new Error('DATABASE_URL must use the postgres:// or postgresql:// scheme.');
}
if (config.isProduction) {
    if (!process.env.BETTER_AUTH_URL || parsedBaseUrl.protocol !== 'https:') {
        throw new Error('BETTER_AUTH_URL must be the canonical HTTPS origin in production.');
    }
    if (!config.databaseUrl)
        throw new Error('DATABASE_URL must be configured in production.');
    if (!process.env.BETTER_AUTH_SECRET) {
        throw new Error('BETTER_AUTH_SECRET must be configured in production.');
    }
    if (!config.smtpHost || !config.smtpUser || !config.smtpPassword || !config.smtpFrom) {
        throw new Error('SMTP_HOST, SMTP_USER, SMTP_PASSWORD, and SMTP_FROM are required in production.');
    }
}
if (!Number.isInteger(config.port) || config.port < 1 || config.port > 65535) {
    throw new Error('PORT must be an integer between 1 and 65535.');
}
if (!Number.isInteger(config.smtpPort) || config.smtpPort < 1 || config.smtpPort > 65535) {
    throw new Error('SMTP_PORT must be an integer between 1 and 65535.');
}
