# car-arbitrage-scanner

A local-first monorepo for exploring car arbitrage opportunities. The current
scope is a clean application foundation: Next.js frontend, FastAPI backend,
PostgreSQL via Docker Compose, database connectivity, seed data, and a simple
dashboard.

Scraping is intentionally not implemented yet. Phase 2 is driven by
`docs/car_arbitrage_ai_prompt_pack.md`.

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
- Raw German listings API: http://localhost:8000/api/listings

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


## Troubleshooting localhost

If http://localhost:3000 does not load after pulling new Phase 2 changes, rebuild
the containers first:

```bash
docker compose up --build
```

If the backend logs show database or Alembic/schema errors from an older local
run, reset the local Postgres volume and start again:

```bash
docker compose down -v
docker compose up --build
```

Useful checks while the stack is running:

```bash
docker compose ps
docker compose logs frontend
docker compose logs backend
```

The frontend now starts even if the backend is still becoming healthy, so
localhost:3000 should show either the dashboard or a backend connection message.

## Database migrations

Docker Compose runs Alembic migrations before the backend starts. For local
backend-only development, run migrations from the backend directory after
installing `backend/requirements.txt`:

```bash
cd backend
alembic upgrade head
```

The initial migration creates `car_listings`, `swedish_comparables`, `deals`,
`model_research`, `cost_assumptions`, and `alerts` using the prompt pack field
names.

## Development notes

- Docker Compose applies Alembic migrations before the backend starts. The
  backend inserts idempotent seed data for the five starter models: VW Golf, VW
  Passat GTE, BMW 320d Touring, Audi A4 Avant, and Volvo V60.
- The frontend reads server-side `API_BASE_URL` first, then
  `NEXT_PUBLIC_API_BASE_URL`, and defaults to `http://localhost:8000`. Docker
  Compose sets `API_BASE_URL` to the backend service hostname.
- The architecture keeps API routing, settings, persistence, schemas, and
  business logic separated so scraping can be added later without coupling it to
  the dashboard or database bootstrap code.
- Scraping is intentionally out of scope for Phase 2; all dashboard
  opportunities are seeded mock data.

## Phase 2 utilities

- Profit calculation lives in `backend/app/scoring/profit.py`.
- Deal scoring lives in `backend/app/scoring/deal_scoring.py`.
- Unit tests for deterministic scoring live in `backend/tests/test_scoring.py`.
