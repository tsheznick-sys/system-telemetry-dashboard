# Pulse Compute Operations

Pulse is a TypeScript/Express operations dashboard with PostgreSQL-backed,
multi-user task management, audit history, account settings, and simulated
telemetry. It uses Neon-compatible PostgreSQL and Better Auth. Telemetry values
are simulated; this application is not an infrastructure monitoring agent.

## Requirements

- Node.js 20.19+, 22.13+, 23.5+, or 24+
- PostgreSQL 14+ (Neon is supported)
- npm

## Configure and run

1. Copy `.env.example` to `.env`.
2. Set `DATABASE_URL` to the Neon connection string and configure a long,
   unique `BETTER_AUTH_SECRET` (at least 32 characters) and the canonical
   `BETTER_AUTH_URL`.
3. Configure `ADMIN_EMAILS` with comma-separated administrator email addresses.
   In production, also configure SMTP so new accounts can verify their email.
4. Apply migrations, compile, and start:

```bash
npm install
npm run db:migrate
npm run build
npm start
```

For local development, run `npm run db:migrate` once, then `npm run dev`. The
server listens on port 3000 by default; set `PORT` to change it.

### Authentication providers

- Email and password registration is open. Production email/password accounts
  must verify their email address using the configured SMTP service. Password
  reset links use the same mail service and revoke active sessions after a
  reset.
- Google sign-in is enabled when both `GOOGLE_CLIENT_ID` and
  `GOOGLE_CLIENT_SECRET` are set. Register
  `https://YOUR_HOST/api/auth/callback/google` as the provider callback URL.
- Administrators in `ADMIN_EMAILS` can register organization-specific OIDC and
  SAML providers from **SSO providers** in the application. Provider secrets
  are submitted to the app server and stored in PostgreSQL; use HTTPS in
  production and restrict database access accordingly.
- SSO provider registration, update, and deletion endpoints are disabled for
  ordinary auth clients. The application exposes provider registration only
  to the configured administrator allowlist.

## Persistence and retention

Every query for tasks, thresholds, telemetry, events, and audit entries is
scoped to the authenticated user. Task creation, updates, and deletion; settings
changes; password resets; and SSO provider registration create audit entries.
Audit history is append-only through the application and retained until the
associated account is deleted.

Telemetry is sampled every 30 seconds (or on manual refresh), and telemetry
samples plus generated system events are retained for 30 days. The server
performs cleanup daily and at startup. Run `npm run db:cleanup` for a manual
cleanup.

Existing data saved by an earlier browser-local demo is not automatically
imported into an account. It remains in that browser's local storage but is not
used by the database-backed version.

## Health and production deployment

- `GET /api/health/live` reports process liveness.
- `GET /api/health/ready` verifies the database and required migrations.
- Production startup requires `DATABASE_URL`, a 32-character
  `BETTER_AUTH_SECRET`, an HTTPS `BETTER_AUTH_URL`, and SMTP settings.
- Apply `npm run db:migrate` as a deployment migration step before rolling out
  the application. Use a Neon role limited to the application's database and
  maintain independent backups and restore testing.
- Terminate TLS at a trusted reverse proxy, expose only the application port,
  configure OAuth callbacks and SMTP delivery, and set `ADMIN_EMAILS` before
  enabling users. Do not commit `.env` or paste secrets into source control.

The application code enforces secure cookies in production, same-origin API
requests, authentication rate limits, payload limits, parameterized SQL,
per-user data isolation, and production environment checks. A live deployment
still requires the operator-provided database, domain, email, OAuth, backup,
and network configuration to be provisioned and tested.

## Build, test, and format

```bash
npm test
npm run build
npm run format:check
npm audit
```

`npm start` serves compiled output from `dist/` and static files from `public/`.

## Project structure

```text
src/
  app.ts                 Express routes, validation, and user-scoped persistence
  auth.ts                Better Auth email, Google, and SSO configuration
  config.ts              Environment configuration and production checks
  db/
    pool.ts              PostgreSQL connection pool
    migrate.ts           Transactional, advisory-locked SQL migration runner
    retention.ts         Manual 30-day telemetry cleanup
    migrations/          Better Auth and application SQL schemas
  server.ts              Production startup, health checks, and scheduled cleanup
tests/
  server.test.ts         Focused API and persistence tests
public/
  index.html             Dashboard, authentication, and SSO provider forms
  css/dashboard.css      Dashboard and sign-in styling
  js/
    api.js               Same-origin API client
    app.js               Telemetry dashboard and persisted settings
    auth.js              Sign-in, registration, and provider UI
    task-manager.js      Account-backed task workflow
    csv.js               Shared CSV download helpers
```
