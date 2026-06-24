import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.quote_api import router as quote_router
from app.core.logging_config import configure_logging
from app.database.database import init_db

logger = logging.getLogger(__name__)

configure_logging()
init_db()

app = FastAPI(
    title="AI Quotes Platform",
    version="1.0.0"
)


# Add a global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.exception("An unhandled exception occurred: %s", exc)
    return JSONResponse(
        status_code=500,
        content={"message": "Internal Server Error", "detail": str(exc)},
    )


app.include_router(quote_router)


@app.get("/")
def root():
    return {
        "message": "Welcome to the AI Quotes Platform"
    }