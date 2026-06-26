# AI Quotes Generator Backend



## Project Overview

This project was created to solve a real problem from my Android Quotes App.

The app originally relied on a third-party quotes API. That was fine in the beginning, but the API later changed significantly and moved important access behind a paywall. That made me realize that even relying on a third-party service for something as simple as quotes can become costly and risky over time.

So I created this backend as a free alternative that I control.

Instead of depending on a paid quotes provider, this project stores quotes in my own Supabase PostgreSQL database and uses Gemini AI to generate new quote content. A scheduled GitHub Actions workflow trigerrs the AI to create new quotes everyday. Generated quotes are validated, cleaned, checked for duplicates, and saved into the database.

The goal is simple: provide a no-cost quotes API for my app, without depending on a paid third-party quote service.


Completed core flow:

```text
Android app / API client
-> FastAPI backend
-> Supabase PostgreSQL
```

Completed AI flow:

```text
GitHub Actions / admin request
-> protected POST /api/generate
-> Gemini AI quote generation
-> validation and cleanup
-> duplicate checks
-> Supabase insert
-> public quote API
```

## What This Project Does

This is a FastAPI backend for a quotes app. It serves random quotes from Supabase PostgreSQL and can generate new quotes using Gemini.

Current capabilities:

- Serves random quotes through a ZenQuotes-compatible response shape.
- Serves one daily/random quote endpoint.
- Stores quotes in Supabase PostgreSQL using SQLAlchemy.
- Seeds initial quote data from `data/quotes.json`.
- Generates new quote candidates using Gemini.
- Validates AI-generated quotes before saving.
- Rejects invalid AI output, markdown, numbering, JSON artifacts, empty values, and bad lengths.
- Rejects duplicate quotes inside the generated batch.
- Checks Supabase for existing quote text before inserting.
- Saves accepted AI quotes into the `quotes` table.
- Protects AI generation with an admin API key.
- Uses GitHub Actions to wake Render and trigger scheduled AI generation.
- Logs and reports major AI pipeline failures.

## Recreate This Project Locally

Follow these steps to run this backend on a new machine.

### 1. Clone The Repository

```powershell
git clone <your-repo-url>
cd backend
```

### 2. Create And Activate A Virtual Environment

```powershell
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 4. Create Environment File

Copy the example file:

```powershell
copy app\.env.example app\.env
```

Fill in real values inside `app/.env`:

```env
DATABASE_URL=postgresql+psycopg://USER:PASSWORD@HOST:5432/DATABASE
GEMINI_API_KEY=your-gemini-api-key
ADMIN_API_KEY=your-admin-api-key
```

Notes:

- `DATABASE_URL` should point to a Supabase PostgreSQL database.
- `GEMINI_API_KEY` comes from Google AI Studio / Gemini API.
- `ADMIN_API_KEY` is any long private secret you create yourself.
- Do not commit `app/.env`.

### 5. Run The Backend

```powershell
uvicorn app.main:app --reload
```

Open Swagger docs:

```text
http://127.0.0.1:8000/docs
```

### 6. Seed Initial Quotes (Optinal, but still good)

If you want to import the starter dataset:

```powershell
python -m scripts.seed_quotes
```

This reads from:

```text
data/quotes.json
```

and inserts some inital quotes into Supabase.

### 7. Test Public Endpoints

```text
GET http://127.0.0.1:8000/
GET http://127.0.0.1:8000/api/quotes
GET http://127.0.0.1:8000/api/today
```

### 8. Test AI Generation Endpoint

Use Swagger, Postman, or curl.

Endpoint:

```text
POST http://127.0.0.1:8000/api/generate?count=5
```

Required header:

```text
X-Admin-Key: your-admin-api-key
```

If successful, generated quotes are validated and saved into Supabase.


## Current Project Structure

```text
backend/
+-- .github/
|   +-- workflows/
|   |   +-- generate-quotes.yml
+-- app/
|   +-- __init__.py
|   +-- .env
|   +-- .env.example
|   +-- main.py
|   +-- api/
|   |   +-- quote_api.py
|   +-- core/
|   |   +-- __init__.py
|   |   +-- exceptions.py
|   |   +-- logging_config.py
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
|   +-- schemas/
|   |   +-- quote_schema.py
|   +-- services/
|   |   +-- ai_quote_service.py
|   |   +-- quote_service.py
|   +-- scheduler/
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
+-- .gitignore
+-- PROJECT_CONTEXT.md
+-- requirements.txt
+-- test_connection.py
+-- venv/
```

## Main Files

- `app/main.py`: FastAPI app entry point, logging setup, DB initialization, router registration.
- `app/api/quote_api.py`: API endpoints for reading quotes and protected AI generation.
- `app/database/database.py`: SQLAlchemy engine, session factory, `Base`, and `init_db()`.
- `app/models/quote.py`: `Quote` database model with `id`, `q`, and `a`.
- `app/repositories/quote_repository.py`: database read/write logic and duplicate checks.
- `app/services/quote_service.py`: normal quote read service.
- `app/services/ai_quote_service.py`: AI generation, validation, duplicate filtering, and save orchestration.
- `app/providers/ai_provider.py`: AI provider abstraction.
- `app/providers/gemini_provider.py`: Gemini implementation.
- `app/validator/quote_validator.py`: generated quote validation and cleanup.
- `app/core/security.py`: admin API key verification.
- `app/core/exceptions.py`: custom pipeline exceptions.
- `app/core/logging_config.py`: logging setup.
- `.github/workflows/generate-quotes.yml`: scheduled GitHub Actions quote generation.

## API Endpoints

### `GET /`

Health/welcome endpoint.

### `GET /api/quotes`

Returns 20 random quotes.

Response shape:

```json
[
  {
    "q": "Quote text",
    "a": "Author"
  }
]
```

### `GET /api/today`

Returns 1 random quote.

### `POST /api/generate?count=20`

Protected admin endpoint that generates, validates, deduplicates, and stores AI quotes.

Required header:

```text
X-Admin-Key: your-admin-api-key
```

Response shape:

```json
{
  "generated": 5, // this is list of quotes after validation i.e after removing duplicates etc from raw gemini quotes
  "quotes": [
    {
      "q": "Quote text",
      "a": "Author"
    }
  ]
}
```

## Environment Variables

Required in local `app/.env` and Render environment variables:

```env
DATABASE_URL=postgresql+psycopg://USER:PASSWORD@HOST:5432/DATABASE
GEMINI_API_KEY=your-gemini-api-key
ADMIN_API_KEY=your-admin-api-key
```

Do not commit real `.env` values.

`app/.env.example` contains safe placeholders.

## Local Run

From the project root:

```powershell
venv\Scripts\activate
uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

## Seed Data

Seed initial quotes from `data/quotes.json`:

```powershell
python -m scripts.seed_quotes
```

## GitHub Actions Scheduler

Workflow file:

```text
.github/workflows/generate-quotes.yml
```

Current behavior:

- Runs daily at `02:30 UTC`, which is `08:00 IST`.
- Can also be triggered manually with `workflow_dispatch`.
- Calls Render root endpoint first to wake the service.
- Waits 100 seconds for warmup.
- Calls `POST /api/generate?count=20`.
- Sends `X-Admin-Key` from GitHub Actions secrets.
- Prints HTTP status and response body when generation fails.

Required GitHub Actions secrets:

```text
BACKEND_BASE_URL=https://your-render-service.onrender.com
ADMIN_API_KEY=your-admin-api-key
```

## Validation Rules For AI Quotes

`QuoteValidator` currently enforces:

- quote text is not empty
- author is not empty
- quote has 8 to 25 words
- quote is at most 200 characters
- whitespace is normalized
- markdown-like text is rejected
- numbering like `1. quote` is rejected
- JSON artifacts like `"q":` or wrappers like `{...}` are rejected
- duplicate quote text inside the same generated batch is rejected

`AIQuoteService` also checks the database before insert so existing quote text is skipped.

## Error Handling And Logs

The AI pipeline logs and reports these failure types:

- Gemini generation failed
- Gemini returned an invalid or empty parsed response
- no generated quotes passed validation
- database save failed

API error mapping:

- Gemini failure: `502`
- invalid AI response: `502`
- no valid quotes: `422`
- database save failure: `500`
- missing/wrong admin key: `401`

Logs appear in the local Uvicorn terminal and Render logs.

## Architecture

The backend uses a layered structure:

```text
API route
-> service
-> repository
-> database
```

AI generation uses:

```text
GeminiProvider
-> AIQuoteService
-> QuoteValidator
-> QuoteRepository
-> Supabase PostgreSQL
```





