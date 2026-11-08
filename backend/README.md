# Shram Saathi Backend

FastAPI + PostgreSQL/PostGIS backend foundation for the Android application.

## Current status

**Foundation scaffold — not production-ready.** This first backend milestone establishes the API service, configuration, database connection, initial marketplace data models and a local PostGIS development environment.

Implemented:
- FastAPI service and OpenAPI docs
- PostgreSQL/PostGIS Docker Compose service
- SQLAlchemy 2 models for users, multi-role accounts, worker/employer profiles, skills, jobs and applications
- Basic service and database health endpoints
- Starter API test

Not implemented yet:
- OTP provider and authentication
- Authorization / role and ownership enforcement
- CRUD endpoints and matching
- Alembic migration history
- Notifications, chat, offers and bookings
- Production secrets, hosting, backups and monitoring

Do not expose this API publicly until authentication, authorization, migrations, validation, rate limiting and security review are complete.

## Run locally

1. Copy `.env.example` to `.env`.
2. Start the database:

```bash
docker compose up -d db
```

3. Create a virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

4. Start the API from the `backend` directory:

```bash
uvicorn app.main:app --reload
```

5. Open:
- API docs: http://127.0.0.1:8000/docs
- Health: http://127.0.0.1:8000/api/v1/health
- Database/PostGIS health: http://127.0.0.1:8000/api/v1/health/database

## Tests

Run from the `backend` directory:

```bash
pytest
```

## Data and privacy principles

- Use UUID identifiers and UTC timestamps.
- Public worker discovery must use approximate location only.
- Never return a worker's exact home coordinates from public APIs.
- Keep wage amount and wage unit together; do not compare unlike wage units.
- Server-side authorization must control every private record and state transition.
