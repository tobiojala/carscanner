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

Optional: copy the local environment template if you want to override defaults:

```bash
cp .env.example .env
```

Start the full stack:

```bash
docker compose up --build
```

Then open:

- Frontend dashboard: http://localhost:3000
- Backend API docs: http://localhost:8000/docs
- Backend health: http://localhost:8000/health
- Mock opportunities API: http://localhost:8000/api/opportunities

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


## Database migrations

Docker Compose runs Alembic migrations before the backend starts. For local
backend-only development, run migrations from the backend directory after
installing `backend/requirements.txt`:

```bash
cd backend
alembic upgrade head
```

The initial migration creates `car_listings`, `swedish_comparables`, `deals`,
`model_research`, `cost_assumptions`, and `alerts`.

## Development notes

- Docker Compose applies Alembic migrations before the backend starts. The
  backend inserts idempotent seed data for listings, comparables, deals, model
  research, cost assumptions, alerts, and dashboard mock opportunities.
- The frontend reads server-side `API_BASE_URL` first, then
  `NEXT_PUBLIC_API_BASE_URL`, and defaults to `http://localhost:8000`. Docker
  Compose sets `API_BASE_URL` to the backend service hostname.
- The architecture keeps API routing, settings, persistence, schemas, and
  business logic separated so scraping can be added later without coupling it to
  the dashboard or database bootstrap code.
- Scraping is intentionally out of scope for Phase 2; all dashboard
  opportunities are seeded mock data.
