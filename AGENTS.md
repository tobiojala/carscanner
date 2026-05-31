# AGENTS.md

## Cursor Cloud specific instructions

### Repository branches

`main` currently contains only a placeholder `README.md`. The runnable monorepo (frontend, backend, Docker Compose) lives on **`cursor/car-arbitrage-scanner-4c75`**. Check out that branch before installing dependencies or starting services.

### Services (see root `README.md` for defaults)

| Service | Port (default) | Purpose |
|---------|----------------|---------|
| PostgreSQL (`db`) | 5432 | Persistence; required for API |
| FastAPI (`backend`) | 8000 | REST API, Alembic migrations, seed data |
| Next.js (`frontend`) | 3000 | Dashboard and workflow UI |

Full-stack dev is intended to run via **Docker Compose** (`npm run dev` or `docker compose up --build`). All three containers are required for browser E2E.

### Docker in Cloud Agent VMs

Docker is not preinstalled. If `docker` is missing, install Docker CE and use the `fuse-overlayfs` storage driver (see Cloud Agent setup docs). On this VM, `dockerd` may need to be started manually:

```bash
sudo dockerd > /tmp/dockerd.log 2>&1 &
```

Use `sudo docker compose …` unless your user is in the `docker` group.

### Lint, typecheck, and tests (no Docker required)

From repo root after `npm install`:

- **Frontend lint:** `cd frontend && npm run lint`
- **Frontend types:** `cd frontend && npm run typecheck`
- **Backend scoring tests:** `pip3 install -r backend/requirements.txt pydantic` then `PYTHONPATH=backend python3 -m unittest backend/tests/test_scoring.py -v`

There is no backend linter configured in-repo. No Playwright/Cypress E2E suite.

### Port conflicts

If port 3000 is taken, set `FRONTEND_PORT` (and open that URL). See `README.md` troubleshooting for `docker compose down -v` when schema/seed issues appear after pulls.

### Secrets

Local MVP needs no API keys. Defaults in `.env.example` are sufficient.
