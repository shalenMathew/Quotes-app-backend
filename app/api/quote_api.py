import logging

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.exceptions import (
    DatabaseSaveError,
    GeminiGenerationError,
    InvalidAIResponseError,
    NoValidQuotesError,
)
from app.core.security import verify_admin_key
from app.database.database import SessionLocal
from app.providers.gemini_provider import GeminiProvider
from app.repositories.quote_repository import QuoteRepository
from app.schemas.quote_schema import GeneratedQuotesResponse, QuoteResponse
from app.services.ai_quote_service import AIQuoteService
from app.services.quote_service import QuoteService
from app.validator.quote_validator import QuoteValidator

logger = logging.getLogger(__name__)

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

    return service.get_random_quotes(15)


@router.get("/today", response_model=list[QuoteResponse])
def get_today_quote(db: Session = Depends(get_db)):
    repository = QuoteRepository(db)
    service = QuoteService(repository)

    return service.get_random_quotes(1)


@router.post("/generate", response_model=GeneratedQuotesResponse)
def generate_quotes(
    count: int = Query(default=1, ge=1, le=50),
    db: Session = Depends(get_db),
    _: None = Depends(verify_admin_key)
):
    try:
        provider = GeminiProvider()
        validator = QuoteValidator()
        repository = QuoteRepository(db)

        service = AIQuoteService(
            provider=provider,
            validator=validator,
            repository=repository
        )

        quotes = service.generate_and_save_quotes(count)

        return {
            "generated": len(quotes),
            "quotes": quotes
        }
    except GeminiGenerationError as exc:
        logger.exception("Generate endpoint failed: Gemini generation error.")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(exc)
        ) from exc
    except InvalidAIResponseError as exc:
        logger.exception("Generate endpoint failed: invalid AI response.")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(exc)
        ) from exc
    except NoValidQuotesError as exc:
        logger.warning("Generate endpoint completed with no valid quotes: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc)
        ) from exc
    except DatabaseSaveError as exc:
        logger.exception("Generate endpoint failed: database save error.")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc)
        ) from exc