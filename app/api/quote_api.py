from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.repositories.quote_repository import QuoteRepository
from app.schemas.quote_schema import QuoteResponse
from app.services.quote_service import QuoteService

router = APIRouter(
    prefix="/api",
    tags=["Quotes"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/quotes", response_model=list[QuoteResponse])
def get_quotes(db: Session = Depends(get_db)):
    repository = QuoteRepository(db)
    service = QuoteService(repository)

    return service.get_random_quotes(50)


@router.get("/today", response_model=list[QuoteResponse])
def get_today_quote(db: Session = Depends(get_db)):
    repository = QuoteRepository(db)
    service = QuoteService(repository)

    return service.get_random_quotes(1)