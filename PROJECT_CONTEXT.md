# Project Context

Last updated: 2026-06-22

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
- Includes a Gemini AI provider for generating quote candidates.
- Includes an AI quote service that validates generated quotes and saves accepted quotes to Supabase.
- Includes a quote validator that enforces quote quality, 8-25 word length, max 200 characters, cleanup, markdown/artifact rejection, and batch duplicate filtering.
- Checks Supabase for existing quote text before inserting AI-generated quotes.
- Protects `POST /api/generate` with an admin API key.

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
|   +-- .env.example
|   +-- main.py
|   +-- api/
|   |   +-- quote_api.py
|   +-- core/
|   |   +-- __init__.py
|   |   +-- security.py
|   +-- database/
|   |   +-- database.py
|   +-- models/
|   |   +-- quote.py
|   +-- providers/
|   |   +-- ai_provider.py
|   |   +-- gemini_provider.py
|   |   +-- test_gemini.py
|   +-- repositories/
|   |   +-- quote_repository.py
|   +-- scheduler/
|   +-- schemas/
|   |   +-- quote_schema.py
|   +-- services/
|   |   +-- ai_quote_service.py
|   |   +-- quote_service.py
|   +-- utils/
|   +-- validator/
|   |   +-- __init__.py
|   |   +-- quote_validator.py
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
- `app/schemas/quote_schema.py` contains shared quote schemas: `QuoteSchema` for generated quote shape and `QuoteResponse` for API responses.
- `app/api/quote_api.py` defines the public quote endpoints and protected AI generation endpoint.
- `app/providers/ai_provider.py` defines the AI provider interface.
- `app/providers/gemini_provider.py` implements Gemini quote generation.
- `app/services/ai_quote_service.py` coordinates AI generation, validation, database duplicate checks, and saving accepted quotes.
- `app/validator/quote_validator.py` cleans generated quotes, enforces 8-25 words/max 200 characters, rejects markdown/numbering/JSON artifacts, removes empty values, and removes duplicates within the generated batch.
- `scripts/seed_quotes.py` imports seed data from `data/quotes.json`.
- `test_connection.py` is used for database connection testing.
- `app/.env` should contain local environment variables such as `DATABASE_URL`, `GEMINI_API_KEY`, and `ADMIN_API_KEY`; do not commit real secrets.
- `app/.env.example` documents required environment variables with safe placeholder values.
- `venv/` and `__pycache__/` are generated/local files and should not be committed.
- Empty directories such as `core/`, `scheduler/`, `utils/`, `docs/`, and `tests/` are scaffolding for planned work.
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
google-genai==2.9.0
```


## Architecture Decisions

- FastAPI chosen over Ktor.
- Supabase chosen as PostgreSQL provider.
- SQLAlchemy ORM.
- Repository → Service → API architecture.
- Response format matches ZenQuotes.
- Database is append-only (Version 1).
- AI pipeline can generate quote candidates through Gemini.
- Batch-level duplicate filtering is implemented in `QuoteValidator`; existing database duplicate checks are handled before inserting generated quotes.
- Initial deployment target: Render.
- Supabase remains the managed PostgreSQL database.
- Android app consumes the backend through a configurable Base URL.
- Future AI pipeline will be triggered externally (planned) rather than relying on a continuously running scheduler inside the web service.



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
- `POST /api/generate?count={n}`
  - Protected by `X-Admin-Key`.
  - Generates AI quote candidates through Gemini.
  - Validates and filters generated quotes.
  - Skips quotes already present in Supabase.
  - Saves accepted quotes to the `quotes` table.

Both endpoints match the ZenQuotes API response format.

#### Data

- Initial quote dataset imported into PostgreSQL.
- Backend successfully serves quotes from the database.

---

## Not Implemented Yet


### AI Pipeline

- Production-ready error handling for Gemini failures.
- Parsing/normalization hardening for AI responses.
- Better reporting for generated/saved/skipped quote counts.

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

0.4.5

## Current Phase

Phase 4 – AI Quote Pipeline

## Current Milestone

## Milestone 4.5 Status

Milestone 4.5 – Generate, Validate, Deduplicate, And Store AI Quotes ✅ INITIAL VERSION COMPLETED

Tasks Completed
✅ Created the AI provider abstraction.
✅ Implemented the Gemini provider.
✅ Added Gemini SDK dependency (`google-genai`).
✅ Configured Gemini API access through `.env`.
✅ Created `QuoteSchema` for AI-generated quote shape.
✅ Updated `QuoteResponse` to inherit from `QuoteSchema`.
✅ Created `AIQuoteService` to coordinate quote generation and validation.
✅ Created `QuoteValidator`.
✅ Added validation for empty quote text.
✅ Added validation for empty author text.
✅ Added normalization for extra whitespace.
✅ Added batch-level duplicate filtering by quote text.
✅ Added database duplicate checks before saving AI-generated quotes.
✅ Added automatic insertion of accepted generated quotes into Supabase.
✅ Exposed the AI pipeline through `POST /api/generate`.
✅ Protected `POST /api/generate` with `X-Admin-Key` and `ADMIN_API_KEY`.
✅ Added `.env.example` with required environment variable placeholders.
✅ Updated the Gemini test script to use provider + validator + service.

#### Outcome

The backend can now generate quote candidates through Gemini, validate them, reject malformed or duplicate content, skip quotes already present in Supabase, and save accepted quotes into the PostgreSQL `quotes` table.

The AI generation endpoint is protected with an admin API key so public users can read quotes without being able to spend Gemini quota or write to the database.

---

## Upcoming Milestones

### Phase 4 – AI Quote Pipeline

Milestone 4.6
- Add production-ready error handling for Gemini failures and invalid AI responses.

Milestone 4.7
- Improve `/api/generate` response with generated/saved/skipped counts and skip reasons.

---

### Phase 5 – Automated Quote Generation

Milestone 5.1
- Configure scheduled quote generation.

Milestone 5.2
- Trigger AI generation automatically.

Milestone 5.3
- Continuously grow the quote database.

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
- ✅ Backend deployed to Render.
- ✅ Public HTTPS endpoint available.
- ✅ Android application migrated from ZenQuotes to the custom backend.
- ✅ End-to-end communication verified:
  Android → Render → FastAPI → Supabase.

### Phase 4

- ✅ Gemini provider implemented.
- ✅ AI provider abstraction added.
- ✅ AI quote service added.
- ✅ `QuoteSchema` created for generated quote shape.
- ✅ `QuoteResponse` now inherits from `QuoteSchema`.
- ✅ Quote validator added for generated quote cleanup and batch deduplication.
- ✅ Quote length validation added: 8-25 words, max 200 characters.
- ✅ Markdown, numbering, JSON artifact, and wrapper rejection added.
- ✅ Database duplicate checks added before AI quote insertion.
- ✅ Validated AI quotes are saved into Supabase.
- ✅ Protected `POST /api/generate` with `ADMIN_API_KEY` / `X-Admin-Key`.













