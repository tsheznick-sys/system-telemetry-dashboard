# System Telemetry Dashboard

A local Express and TypeScript app that serves a dark-mode dashboard and mock
system telemetry. All telemetry is generated locally with Faker; the frontend
does not rely on a remote CSS framework or telemetry API.

## Requirements

- Node.js 20.19+, 22.13+, 23.5+, or 24+
- npm

## Setup and run

```bash
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000). Set `PORT` in your
environment or a local `.env` file to use a different port.

## Dashboard features

- Switchable CPU, memory, connection, and error-rate history charts with 1-, 5-,
  and 15-minute views.
- Locally persisted metric samples and configurable alert thresholds.
- Searchable, level-filtered recent events, with CSV export for telemetry and
  events.
- Compute-operations overview with live mock cluster telemetry and system
  health indicators.
- Task cockpit with a kanban workflow, priorities, workstreams, due dates,
  search, editing, completion, deletion, and CSV export.

Telemetry and task data are local demo data. Saved samples, thresholds, and
tasks stay in the browser's local storage and are not sent to a remote service.

## Build and test

```bash
npm test
npm run build
npm run format:check
npm start
```

`npm start` serves the compiled backend from `dist/`; the `public/` directory
is served from the project root regardless of the current working directory.

## Project structure

```text
src/
  server.ts          Express app and telemetry endpoint
tests/
  server.test.ts     Telemetry API tests
public/
  index.html         Dashboard structure
  css/
    dashboard.css    Dashboard styling
  js/
    app.js           Dashboard navigation and telemetry
    task-manager.js  Local task workflow and board rendering
    csv.js           Shared CSV download helpers
```

`npm run format` applies the configured Prettier style; `npm run format:check`
checks it without modifying files.
