from fastapi import FastAPI

from app.api.quote_api import router as quote_router

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