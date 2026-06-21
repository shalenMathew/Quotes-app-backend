# Project Context

Last updated: 2026-06-21

## Purpose

This repository is the backend for an "AI Quotes Platform". It is a FastAPI service that currently serves quote data from a Supabase PostgreSQL database using a layered backend structure.

The app currently:

- Creates a FastAPI app titled `AI Quotes Platform`.
- Connects to PostgreSQL through SQLAlchemy using `DATABASE_URL` from the environment.
- Defines a `Quote` SQLAlchemy model with `id`, `q`, and `a` fields.
- Exposes quote API routes under `/api`.
- Returns 50 random quotes from `GET /api/quotes`.
- Returns 1 random quote from `GET /api/today`.
- Uses repository and service layers for quote retrieval.
- Uses Pydantic response schemas that match the ZenQuotes-style `q` and `a` response format.
- Includes a seed script for importing quote data from `data/quotes.json` into the database.

The current project goal is to replace the ZenQuotes API dependency for the Android app with this custom backend. Future phases plan to add AI quote generation, duplicate detection, scheduled quote generation, and deployment.

## Current Project Structure

```text
backend/
+-- .git/
+-- .gitignore
+-- PROJECT_CONTEXT.md
+-- requirements.txt
+-- test_connection.py
+-- app/
|   +-- __init__.py
|   +-- .env
|   +-- main.py
|   +-- api/
|   |   +-- quote_api.py
|   +-- core/
|   +-- database/
|   |   +-- database.py
|   +-- models/
|   |   +-- quote.py
|   +-- providers/
|   +-- repositories/
|   |   +-- quote_repository.py
|   +-- scheduler/
|   +-- schemas/
|   |   +-- quote_schema.py
|   +-- services/
|   |   +-- quote_service.py
|   +-- utils/
+-- data/
|   +-- quotes.json
+-- docs/
+-- scripts/
|   +-- seed_quotes.py
+-- tests/
+-- venv/
```

Important notes:

- `app/main.py` is the FastAPI entry point and includes the quote API router.
- `app/database/database.py` loads environment variables, creates the SQLAlchemy engine, defines `SessionLocal`, defines `Base`, imports models, and creates tables.
- `app/models/quote.py` defines the `quotes` table model.
- `app/repositories/quote_repository.py` contains database query logic.
- `app/services/quote_service.py` contains quote business/service logic.
- `app/schemas/quote_schema.py` contains Pydantic response schemas.
- `app/api/quote_api.py` defines the public quote endpoints.
- `scripts/seed_quotes.py` imports seed data from `data/quotes.json`.
- `test_connection.py` is used for database connection testing.
- `app/.env` should contain local environment variables such as `DATABASE_URL`; do not commit real secrets.
- `venv/` and `__pycache__/` are generated/local files and should not be committed.
- Empty directories such as `core/`, `providers/`, `scheduler/`, `utils/`, `docs/`, and `tests/` are scaffolding for planned work.
- `.gitignore` is present and ignores Python caches, virtual environments, `.env` files, local databases, logs, build output, IDE files, and OS files.
## Runtime And Dependencies

Dependencies are now tracked in `requirements.txt`.

Key packages:

```text
fastapi==0.138.0
uvicorn==0.49.0
pydantic==2.13.4
starlette==1.3.1
SQLAlchemy==2.0.51
psycopg==3.3.4
psycopg-binary==3.3.4
python-dotenv==1.2.2
```


## Architecture Decisions

- FastAPI chosen over Ktor.
- Supabase chosen as PostgreSQL provider.
- SQLAlchemy ORM.
- Repository → Service → API architecture.
- Response format matches ZenQuotes.
- Database is append-only (Version 1).
- AI pipeline will generate new quotes.
- Duplicate detection will occur before insertion.
- Deployment target: Oracle Cloud (planned).
- Android app should only need a Base URL change.



#### Project Architecture

- FastAPI project initialized.
- Layered project structure established.
- Virtual environment configured.
- Git repository initialized.
- `.gitignore` configured.
- Dependencies managed through `requirements.txt`.

#### Database

- Supabase PostgreSQL project created.
- Environment variables configured.
- SQLAlchemy engine configured.
- SQLAlchemy session factory implemented.
- SQLAlchemy `Base` class created.
- `Quote` model implemented.
- `quotes` table created successfully.
- Database connection verified.

#### Backend Architecture

- Repository layer implemented.
- Service layer implemented.
- Pydantic response schemas implemented.
- REST API router implemented.

#### API

Implemented endpoints:

- `GET /api/quotes`
  - Returns 50 random quotes.
- `GET /api/today`
  - Returns 1 random quote.

Both endpoints match the ZenQuotes API response format.

#### Data

- Initial quote dataset imported into PostgreSQL.
- Backend successfully serves quotes from the database.

---

## Not Implemented Yet

### Android Integration

- Connect Android application to the custom backend.
- Replace ZenQuotes base URL.

### AI Pipeline

- Gemini integration.
- AI quote generation.
- Quote validation.
- Duplicate detection.
- Automatic database insertion.

### Scheduler

- Scheduled quote generation.
- Automatic database updates.

### Deployment

- Production hosting.
- HTTPS configuration.
- Production environment variables.
- Custom domain (optional).


## Add Current Database Plan:

Version 1 will keep the database intentionally simple.

Quotes Table

- id
- q
- a

Additional columns will only be added when there is a real requirement.


## Current Version

0.3.1

## Current Phase

Phase 3

## Current Milestone

### Milestone 3.1 – Seed the Database ✅ COMPLETED

#### Tasks Completed

- ✅ Created a `data/` directory for seed datasets.
- ✅ Added an initial quotes JSON dataset.
- ✅ Created a database seeding script.
- ✅ Imported quotes into the Supabase PostgreSQL database.
- ✅ Verified that quotes were successfully inserted.
- ✅ Confirmed the REST API returns data from the database.

#### Outcome

The backend now contains an initial dataset of quotes and is capable of serving real data instead of empty responses.

---

## Upcoming Milestones

### Milestone 3.2 – Android App Integration

Tasks

- Point the Android application to the new backend.
- Replace the ZenQuotes base URL.
- Verify Retrofit communication.
- Display quotes served from the custom backend.
- Ensure the existing Android code works without modifying the DTOs.

---

### Future Milestones (Planned)

#### Phase 4 – AI Quote Pipeline

- Integrate Google Gemini.
- Generate new quotes automatically.
- Validate AI responses.
- Remove duplicate quotes.
- Store validated quotes in PostgreSQL.

---

#### Phase 5 – Scheduler

- Automatically run the AI pipeline.
- Generate new quotes at scheduled intervals.
- Continuously grow the quote database.

---

#### Phase 6 – Deployment

- Deploy FastAPI backend.
- Configure HTTPS.
- Update Android production base URL.
- Prepare production environment.

---

## Completed

### Phase 1

- ✅ FastAPI installed.
- ✅ Virtual environment configured.
- ✅ Root endpoint created.
- ✅ Swagger/OpenAPI documentation enabled.
- ✅ Git initialized.
- ✅ `.gitignore` configured.
- ✅ `requirements.txt` created.
- ✅ Initial project architecture created.

### Phase 2

- ✅ Connected FastAPI to Supabase PostgreSQL.
- ✅ Configured environment variables.
- ✅ SQLAlchemy engine created.
- ✅ SQLAlchemy session factory created.
- ✅ Created SQLAlchemy Base.
- ✅ Created the `Quote` model.
- ✅ Created the `quotes` table.
- ✅ Implemented the Repository layer.
- ✅ Implemented the Service layer.
- ✅ Created REST API endpoints:
  - `GET /api/quotes`
  - `GET /api/today`
- ✅ Matched the ZenQuotes response format.
- ✅ Created response schemas using Pydantic.

### Phase 3

- ✅ Seed dataset imported.
- ✅ Database populated with quotes.
- ✅ Backend successfully serves quotes from PostgreSQL.






