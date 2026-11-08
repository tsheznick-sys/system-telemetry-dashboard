# System Telemetry Dashboard

A local Express and TypeScript app that serves a dark-mode dashboard and mock
system telemetry. All telemetry is generated locally with Faker; the frontend
does not rely on a remote CSS framework or telemetry API.

## Requirements

- Node.js 18 or newer
- npm

## Setup and run

```bash
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000). Set `PORT` in your
environment or a local `.env` file to use a different port.

## Build and test

```bash
npm test
npm run build
npm start
```

`npm start` serves the compiled backend from `dist/`; the `public/` directory
is served from the project root.