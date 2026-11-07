import { betterAuth } from 'better-auth';
import { fromNodeHeaders } from 'better-auth/node';
import { sso } from '@better-auth/sso';
import nodemailer from 'nodemailer';
import { config } from './config.js';
import { pool } from './db/pool.js';
const demoUser = { id: 'demo-user', name: 'Local Operator', email: 'demo@local' };
let auth;
let resolveSession;
if (config.dashboardMode) {
    auth = {
        api: {
            getSession: async () => ({ user: demoUser }),
            registerSSOProvider: async () => ({}),
        },
    };
    resolveSession = async () => ({ user: demoUser });
}
else {
    const hasSmtp = Boolean(config.smtpHost && config.smtpUser && config.smtpPassword && config.smtpFrom);
    const mailer = hasSmtp
        ? nodemailer.createTransport({
            host: config.smtpHost,
            port: config.smtpPort,
            secure: config.smtpPort === 465,
            auth: { user: config.smtpUser, pass: config.smtpPassword },
        })
        : null;
    const socialProviders = config.googleClientId && config.googleClientSecret
        ? {
            google: {
                clientId: config.googleClientId,
                clientSecret: config.googleClientSecret,
            },
        }
        : {};
    auth = betterAuth({
        appName: 'Pulse Compute Operations',
        baseURL: config.baseUrl,
        secret: config.authSecret,
        database: pool,
        trustedOrigins: [config.baseUrl],
        emailAndPassword: {
            enabled: true,
            requireEmailVerification: config.isProduction,
            revokeSessionsOnPasswordReset: true,
            async sendResetPassword({ user, url }) {
                if (!mailer || !config.smtpFrom) {
                    throw new Error('Password reset email is not configured.');
                }
                void mailer
                    .sendMail({
                    from: config.smtpFrom,
                    to: user.email,
                    subject: 'Reset your Pulse password',
                    text: `Reset your password using this secure link: ${url}`,
                })
                    .catch((error) => {
                    console.error('Password reset email delivery failed:', error instanceof Error ? error.message : 'Unknown error');
                });
            },
            async onPasswordReset({ user }) {
                try {
                    await pool.query(`INSERT INTO audit_events (user_id, action, resource_type, resource_id)
           VALUES ($1, 'auth.password_reset', 'account', $1)`, [user.id]);
                }
                catch (error) {
                    console.error('Password reset completed but audit recording failed:', error instanceof Error ? error.name : 'Unknown error');
                }
            },
        },
        emailVerification: {
            sendOnSignUp: config.isProduction,
            autoSignInAfterVerification: true,
            async sendVerificationEmail({ user, url }) {
                if (!mailer || !config.smtpFrom) {
                    throw new Error('Email verification is not configured.');
                }
                await mailer.sendMail({
                    from: config.smtpFrom,
                    to: user.email,
                    subject: 'Verify your Pulse account',
                    text: `Verify your email address: ${url}`,
                });
            },
        },
        socialProviders,
        plugins: [
            sso({
                modelName: 'sso_provider',
                providersLimit: (user) => (config.adminEmails.has(user.email.toLowerCase()) ? 10 : 0),
            }),
        ],
        advanced: {
            useSecureCookies: config.isProduction,
            crossSubDomainCookies: { enabled: false },
        },
        disabledPaths: ['/sso/register', '/sso/update-provider', '/sso/delete-provider'],
    });
    resolveSession = (headers) => auth.api.getSession({ headers: fromNodeHeaders(headers) });
}
export { auth, resolveSession };
