# Car Arbitrage Scanner

Private project.

Copyright © 2026 Tobias Bergmark.
All rights reserved.

This repository and all associated documentation, research data, prompts, designs, source code, scoring logic, and market intelligence are proprietary and confidential.

This tool is a private local-first MVP for evaluating Germany-to-Sweden car arbitrage opportunities.

Current MVP includes:
- manual listing input
- Swedish comparable input
- profit calculation
- deal scoring
- model research profiles
- deal pipeline
- local Docker runtime

Current limitations:
- scraping is not implemented
- AI automation is not implemented
- alerts are not implemented
- browser extension is not implemented

Local run command:

```bash
FRONTEND_PORT=5173 BACKEND_PORT=8010 POSTGRES_PORT=55432 docker compose up --build
```

---

## Project layout

```text
.
├── backend/          # FastAPI API, SQLAlchemy models, services, seed data
├── frontend/         # Next.js App Router dashboard
├── docs/             # Project documentation, prompts, model research
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
FRONTEND_PORT=5173 BACKEND_PORT=8010 POSTGRES_PORT=55432 docker compose up --build
```

Then open:

- Frontend dashboard: http://localhost:5173
- Backend API docs: http://localhost:8010/docs
- Backend health: http://localhost:8010/health

PostgreSQL is exposed at `localhost:55432` with:

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

If the frontend does not load after pulling new changes, first check whether another app is using the port. Otherwise, rebuild the containers:

```bash
docker compose up --build
```

If the backend logs show database or Alembic/schema errors from an older local run, reset the local Postgres volume and start again:

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

## Running tests

Backend unit tests:

```bash
PYTHONPATH=backend python3 -m unittest discover -s backend/tests
```

Frontend validation:

```bash
npm --workspace frontend run lint
npm --workspace frontend run typecheck
npm --workspace frontend run build
```

## Database migrations

Docker Compose runs Alembic migrations before the backend starts. For local backend-only development, run migrations from the backend directory after installing `backend/requirements.txt`:

```bash
cd backend
alembic upgrade head
```

## Development notes

- Docker Compose applies Alembic migrations before the backend starts. The backend inserts idempotent seed data for the five starter models: VW Golf, VW Passat GTE, BMW 320d Touring, Audi A4 Avant, and Volvo V60.
- The frontend reads server-side `API_BASE_URL` first, then `NEXT_PUBLIC_API_BASE_URL`, and defaults to `http://localhost:8000`.
- Profit calculation lives in `backend/app/scoring/profit.py`.
- Deal scoring lives in `backend/app/scoring/engine.py`.
- Unit tests for deterministic scoring live in `backend/tests/test_scoring.py`.

## Seed data

Seed data runs automatically when the backend starts after migrations. It creates mock German listings, Swedish comparables, cost assumptions, deal opportunities, and model research intelligence profiles. To reseed locally, reset the PostgreSQL volume:

```bash
docker compose down -v
FRONTEND_PORT=5173 BACKEND_PORT=8010 POSTGRES_PORT=55432 docker compose up --build
```

## Workflow pages

- `/deals` — deal scanner table with filters
- `/pipeline` — status board (New → Researching → Contacted → Negotiating → Bought → Imported → Listed → Sold → Rejected)
- `/market-research` — seeded analytics for the five starter models
- `/settings` — editable cost assumptions
- `/comparables` — add Swedish comparable listings manually
- `/compare` — side-by-side deal comparison

## Documentation

- `PROJECT_STATUS.md` — current status, completed work, next recommended work
- `docs/project_vision.md` — product vision and value proposition
- `docs/automation_roadmap.md` — phased automation plan (Levels 1–7)
- `docs/scoring_principles.md` — deterministic vs AI-assisted scoring rules
- `docs/pause_resume_checklist.md` — checklist for pausing and resuming development
- `docs/prompts/` — AI co-build prompt pack and prompt templates
- `docs/model_research/` — model-specific research notes
