# car-arbitrage-scanner

A local-first monorepo for exploring car arbitrage opportunities. The current
scope is a clean application foundation: Next.js frontend, FastAPI backend,
PostgreSQL via Docker Compose, database connectivity, seed data, and a simple
dashboard.

Scraping is intentionally not implemented yet.

## Project layout

```text
.
├── backend/          # FastAPI API, SQLAlchemy models, services, seed data
├── frontend/         # Next.js App Router dashboard
├── docker-compose.yml
└── package.json      # Monorepo helper scripts
```

## Run locally

Start the full stack:

```bash
docker compose up --build
```

Then open:

- Frontend dashboard: http://localhost:3000
- Backend API docs: http://localhost:8000/docs
- Backend health: http://localhost:8000/health

PostgreSQL is exposed at `localhost:5432` with:

- Database: `car_arbitrage`
- User: `car_user`
- Password: `car_password`

Stop the stack:

```bash
docker compose down
```

Reset the database volume and reseed on next startup:

```bash
docker compose down -v
```

## Development notes

- The backend creates the current schema on startup and inserts seed listings if
  the database is empty.
- The frontend reads `NEXT_PUBLIC_API_BASE_URL` and defaults to
  `http://localhost:8000`.
- The architecture keeps API routing, settings, persistence, schemas, and
  business logic separated so scraping can be added later without coupling it to
  the dashboard or database bootstrap code.
