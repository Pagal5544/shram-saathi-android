# Shram Saathi Backend

Free-first backend foundation for the Shram Saathi Android app.

**Development branch:** `backend/foundation`  
**Current milestone:** Documentation and implementation roadmap  
**Status:** Foundation scaffold only — not production-ready.

The project will use free and open-source software wherever practical. Paid third-party services will not be introduced during the initial development unless a feature cannot be implemented safely without them.

## 1. Free-first technology stack

| Area | Selected technology | Cost approach |
|---|---|---|
| Backend language | Python | Free / open source |
| API framework | FastAPI | Free / open source |
| Data validation | Pydantic | Free / open source |
| ORM | SQLAlchemy 2 | Free / open source |
| Database | PostgreSQL | Free / open source |
| Geospatial queries | PostGIS + GeoAlchemy2 | Free / open source |
| Schema migrations | Alembic | Free / open source |
| API documentation | OpenAPI / Swagger UI | Included with FastAPI |
| Automated tests | pytest + httpx | Free / open source |
| Local development | Docker Compose | Free tooling |
| Source control | Git + GitHub | Free tier |
| CI checks | GitHub Actions | Use free included quota |
| Android networking | Retrofit + OkHttp | Free / open source |
| Android local cache | Room + DataStore | Free / open source |
| Push notifications | Firebase Cloud Messaging | No-cost service; usage/terms apply |
| Map data | OpenStreetMap | Open data; choose a compliant tile/geocoding provider |

### Cost boundary

"Free" here means no software licence or initial development fee. It does **not** mean unlimited free production hosting, SMS, storage, map tiles, backups, bandwidth or operations.

For the first development milestones:
- Run API and PostgreSQL/PostGIS locally.
- Use sample/test accounts and local test data.
- Do not purchase a cloud server, paid database, SMS bundle or maps subscription.
- Do not add a payment gateway or subscription billing.
- Keep provider-specific integrations behind interfaces so a provider can be selected later without rewriting core business logic.

## 2. Features planned for the free core

These are product capabilities intended to remain usable without a paid subscription.

### Worker
- Create and edit worker profile.
- Add skills, experience and wage expectations.
- Set work availability and preferred work type.
- Discover relevant jobs.
- Apply to jobs and withdraw an application.
- Negotiate job terms.
- Confirm or cancel a booking according to booking rules.
- Basic chat and notifications.
- Receive ratings after a completed booking.
- Report or block abusive accounts.

### Employer / contractor
- Create and edit employer profile.
- Create, edit, pause and close job posts.
- Discover workers using basic filters.
- Review applications and invite workers.
- Negotiate wages and work terms.
- Confirm or cancel bookings according to booking rules.
- Basic chat and notifications.
- Rate workers after a completed booking.
- Report or block abusive accounts.

### Shared platform capabilities
- One account may hold both Worker and Hiring roles.
- Role and ownership checks on every protected operation.
- Basic job/worker search and recommendation matching.
- Approximate-location discovery.
- Ratings, reports and account privacy controls.
- Hindi and English ready API responses and validation messages where practical.

**Important:** A feature listed here is planned, not necessarily implemented. See the milestone status below.

## 3. Paid services deliberately deferred

Do not integrate or purchase these in the initial build:

| Service / capability | Initial decision | Later trigger |
|---|---|---|
| Production API hosting | Defer | Before public launch |
| Managed production database | Defer | Before public launch |
| SMS OTP provider | Defer provider choice | When real phone verification is ready |
| Paid domain name | Defer | Before public API launch |
| Paid object/file storage | Defer | When production uploads are required |
| Paid maps/geocoding APIs | Avoid initially | Only if open-data/provider limits require it |
| Payment gateway | Out of initial scope | After legal, compliance and business review |
| Paid analytics / monitoring | Defer | When production scale requires it |
| Premium subscriptions / paid listings | Out of initial scope | Only after free marketplace is stable |

Firebase Cloud Messaging may be used for push delivery without a paid messaging licence, but it does not provide SMS OTP. SMS verification is a separate service and may incur charges.

## 4. Implementation roadmap

Work in this order. Do not mark a milestone complete until code, tests and documentation are committed.

1. **Foundation and documentation**
   - Confirm project structure and environment configuration.
   - Validate FastAPI startup and database connectivity.
   - Keep secrets out of Git.
2. **Database reliability**
   - Add Alembic migrations.
   - Validate SQLAlchemy models and relationships.
   - Add indexes and constraints.
3. **Identity and access**
   - Define secure authentication and token lifecycle.
   - Add role-based and record-ownership authorization.
   - Keep real SMS OTP provider selection separate from core auth logic.
4. **Profiles and skills**
   - Worker/employer profile APIs.
   - Skill catalogue, experience and availability APIs.
5. **Jobs and applications**
   - Job CRUD, search, applications and invitations.
   - Validate wage amount/unit and job state transitions.
6. **Location and matching**
   - PostGIS-based distance and basic matching.
   - Return approximate public worker location only.
7. **Negotiation and bookings**
   - Offers, counter-offers, mutual confirmation and cancellation rules.
8. **Communication and trust**
   - Basic chat, FCM push notifications, ratings, reports and blocking.
9. **Production readiness**
   - Security review, rate limits, migrations, backups, monitoring, privacy review and deployment.

## 5. Current implementation status

### Already scaffolded
- FastAPI application entry point.
- Environment-based settings.
- SQLAlchemy database setup.
- Initial models for users, roles, worker/employer profiles, skills, jobs and applications.
- PostgreSQL/PostGIS Docker Compose configuration.
- Health endpoints:
  - `GET /api/v1/health`
  - `GET /api/v1/health/database`
- Starter pytest health test.
- Backend GitHub Actions workflow.

### Not yet implemented / not yet verified
- Complete Alembic migration history.
- Production authentication, OTP and authorization.
- CRUD APIs for marketplace entities.
- Search, matching and geospatial API behavior.
- Offers, bookings, chat and notifications.
- Ratings, reports and blocking APIs.
- Production hosting, secrets, backups and monitoring.
- A verified green backend CI run.

Do not describe this scaffold as a completed backend and do not expose it publicly.

## 6. Run locally

From the repository root, enter the backend directory:

```bash
cd backend
```

Create local environment configuration:

```bash
cp .env.example .env
```

Start PostgreSQL/PostGIS:

```bash
docker compose up -d db
```

Create a virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Start the API:

```bash
uvicorn app.main:app --reload
```

Open:
- API docs: http://127.0.0.1:8000/docs
- Health: http://127.0.0.1:8000/api/v1/health
- Database health: http://127.0.0.1:8000/api/v1/health/database

Run tests:

```bash
pytest
```

## 7. Security and privacy rules

- Never commit `.env`, passwords, API keys, signing keys or production credentials.
- Use UUID identifiers and UTC timestamps.
- Enforce authentication, role permissions and record ownership server-side.
- Never expose a worker's exact home coordinates through public discovery APIs.
- Use approximate location for public worker discovery.
- Validate all user input and enforce safe upload limits.
- Keep wage amount and wage unit together; do not compare unlike units.
- Protect sensitive endpoints with rate limits before public launch.
- Do not deploy until authentication, authorization, migrations and security review are complete.

## 8. Product and repository references

- Android app package: `com.shramsaathi.app`
- Locked Android UI baseline: `release/v0.1.0`
- Backend development branch: `backend/foundation`
- Product blueprint: [../../BLUEPRINT.md](../../BLUEPRINT.md)
- UI/UX specification: [../../docs/UI_UX_DESIGN.md](../../docs/UI_UX_DESIGN.md)


## Implemented public API endpoints

These endpoints are read-only and use the PostgreSQL database:

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/v1/health` | API health |
| GET | `/api/v1/health/database` | PostgreSQL and PostGIS connectivity |
| GET | `/api/v1/skills` | Active skills with category names |
| GET | `/api/v1/jobs` | Open jobs with pagination |
| GET | `/api/v1/jobs?district=Meerut` | Filter open jobs by district |
| GET | `/api/v1/jobs?skill_id=<uuid>` | Filter open jobs by skill |
| GET | `/api/v1/jobs/<job-uuid>` | One open job detail |

The public job response intentionally excludes exact coordinates and private worker information. Write endpoints are not exposed until authentication and authorization are implemented.

## Database migrations

The initial Alembic migration creates the marketplace schema and enables the PostGIS extension.

From the `backend` directory:

```bash
alembic upgrade head
```

Check whether model definitions and migration history are aligned:

```bash
alembic check
```

Create a future migration after changing models:

```bash
alembic revision --autogenerate -m "describe schema change"
```

Rollback the latest migration:

```bash
alembic downgrade -1
```

The backend CI workflow starts a temporary PostGIS database, applies migrations, checks migration/model consistency and runs tests. This is a disposable CI database, not a production database.

## Docker Compose note

The API container connects to the Compose database service using hostname `db`. The local `.env.example` URL is intended for running the API directly on the host; Compose overrides it for the API container.
