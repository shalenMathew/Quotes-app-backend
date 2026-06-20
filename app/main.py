from fastapi import FastAPI

app = FastAPI(
    title="AI Quotes Platform",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "Welcome to the AI Quotes Platform 🚀"
    }