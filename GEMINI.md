# Agent Guide: Pathcamp Environment & Workflows

This document contains critical instructions for agents working on this repository to avoid wasting time on environment and execution errors.

## 1. Container Engine
- **ALWAYS use `podman` and `podman-compose`.** 
- Do NOT use `docker` or `docker-compose`.

## 2. Backend Architecture Constraints
- The backend is a FastAPI application managed via `poetry`.
- The production `Dockerfile` uses a two-stage build that results in a **Distroless** image (`gcr.io/distroless/python3-debian12`).
- **CRITICAL:** The running backend container (`pathcamp_backend_1`) DOES NOT have a shell (`/bin/bash`), `pip`, or `poetry` installed.
- **Do not** attempt to run `podman exec pathcamp_backend_1 poetry run ...` or `pytest` inside the running backend container. It will fail with `executable file not found`.

## 3. Running Tests & Alembic Migrations
To run development commands like `pytest` or `alembic`, you must spin up an **ephemeral `python:3.11-slim` container**, mount the backend directory, install poetry, and execute the command.

### Running Tests
Use an ephemeral SQLite database to avoid postgres dependency issues during tests.
```bash
podman run --rm -v $PWD/backend:/app -w /app -e DATABASE_URL="sqlite:///./test.db" python:3.11-slim /bin/bash -c "pip install poetry && poetry config virtualenvs.create false && poetry install --no-root && pytest"
```

### Running Alembic Migrations
Connect the ephemeral container to the `pathcamp_default` network so it can reach the running `db` container.
```bash
podman run --rm -v $PWD/backend:/app -w /app --network pathcamp_default -e DATABASE_URL="postgresql://postgres:password@db:5432/pathcamp" python:3.11-slim /bin/bash -c "pip install poetry && poetry config virtualenvs.create false && poetry install --no-root && alembic revision --autogenerate -m 'Migration name' && alembic upgrade head"
```

## 4. Dealing with Database State
- When modifying SQLAlchemy models, be aware that if the `pathcamp_pgdata` volume already exists from a previous run, SQLAlchemy's `create_all()` will NOT update existing tables (e.g., it won't add new columns).
- If you encounter a `psycopg2.errors.UndefinedColumn` or similar 500 error after a model change, you either need to run an Alembic migration or fully reset the database.
- **To wipe the database volume and reset the stack:**
  ```bash
  podman-compose down -v && podman-compose up -d --build
  ```

## 5. Frontend Development Server
- The frontend is a Vite + React application.
- To run it in the background during manual end-to-end testing:
  ```bash
  cd frontend && npm install && npm run dev
  ```
  The app will be available at `http://localhost:5173/` and proxies `/auth` and `/admin` requests to the backend at `http://localhost:8000/`.
