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

If another app is already using `localhost:3000`, run the frontend on a
different host port, for example:

```bash
FRONTEND_PORT=3001 docker compose up --build
```

Then open http://localhost:3001. You can also move the backend or Postgres host
ports if needed:

```bash
FRONTEND_PORT=3001 BACKEND_PORT=8001 POSTGRES_PORT=5433 docker compose up --build
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

If http://localhost:3000 does not load after pulling new Phase 2 changes, first
check whether another app is using port 3000. If so, use `FRONTEND_PORT=3001`
and open http://localhost:3001. Otherwise, rebuild the containers:

```bash
docker compose up --build
```

If the backend logs show database or Alembic/schema errors from an older local
run, reset the local Postgres volume and start again:

```bash
docker compose down -v
docker compose up --build
```

If a newly added page returns 404, make sure you have pulled the latest branch
and rebuilt the frontend image:

```bash
git pull
docker compose down
FRONTEND_PORT=5173 BACKEND_PORT=8010 POSTGRES_PORT=55432 docker compose up --build
```

Useful checks while the stack is running:

```bash
docker compose ps
docker compose logs frontend
docker compose logs backend
```

On macOS or Linux, this can help identify a port conflict:

```bash
lsof -i :3000
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

## Model research seed modules

Model-specific research profiles can live under `backend/app/seeds/model_research/`.
For example, `audi_a4_avant_b9.py`, `bmw_320d_touring.py`, `vw_golf_variant_mk7.py`, and `vw_passat_gte_variant.py` expose
builder functions that return fresh SQLAlchemy `ModelResearch` objects mapped
from richer research profiles into the current `model_research` table columns.

## Link intake workflow

Use `/link-intake` to paste batches of mobile.de, AutoScout24, Blocket, or Bytbil
links. The app classifies each URL by marketplace and whether it appears to be a
search link or individual listing link. Search links are useful queues; open an
individual listing from the search results before adding a manual deal.

## Workflow pages

The frontend now includes the remaining Phase 2 workflow screens:

- `/deals` - deal scanner table with filters for model, profit, confidence,
  source, seller type, fuel, transmission, and status.
- `/pipeline` - status board for moving deals through New, Researching,
  Contacted, Negotiating, Bought, Imported, Listed in Sweden, Sold, or Rejected.
- `/market-research` - seeded analytics for the five starter models.
- `/settings` - editable cost assumptions used by future manual deal
  calculations.

Supporting APIs include filtered `GET /api/opportunities`,
`PATCH /api/deals/{id}/status`, `GET/PATCH /api/settings`, and
`GET/PATCH /api/model-research`.

## Deal detail workflow

Each opportunity in the dashboard links to `/deals/{id}`. The detail page uses
`GET /api/deals/{id}` to show the foreign listing, deterministic cost breakdown,
score explanation, risk flags, and matching Swedish comparable listings.

## Manual input workflow

The dashboard includes a Phase 2 manual listing form. Submitting it creates a
German listing with `POST /api/listings`, then calculates and stores a scored
deal opportunity with `POST /api/deals/calculate`. Supporting endpoints are now
available for listing CRUD and Swedish comparable input:

- `GET /api/listings`
- `POST /api/listings`
- `GET /api/listings/{id}`
- `PATCH /api/listings/{id}`
- `DELETE /api/listings/{id}`
- `GET /api/comparables`
- `POST /api/comparables`
- `POST /api/deals/calculate`

## Phase 2 utilities

- Profit calculation lives in `backend/app/scoring/profit.py`.
- Deal scoring lives in `backend/app/scoring/deal_scoring.py`.
- Unit tests for deterministic scoring live in `backend/tests/test_scoring.py`.
