from fastapi import FastAPI

from app.api.quote_api import router as quote_router
from app.core.logging_config import configure_logging
from app.database.database import init_db

configure_logging()
init_db()

app = FastAPI(
    title="AI Quotes Platform",
    version="1.0.0"
)

app.include_router(quote_router)


@app.get("/")
def root():
    return {
        "message": "Welcome to the AI Quotes Platform"
    }