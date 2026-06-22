import logging

from sqlalchemy import func, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.exceptions import DatabaseSaveError
from app.models.quote import Quote

logger = logging.getLogger(__name__)


class QuoteRepository:

    def __init__(self, db: Session):
        self.db = db

    def create_quote(self, quote: Quote) -> Quote:
        try:
            self.db.add(quote)
            self.db.commit()
            self.db.refresh(quote)
            return quote
        except SQLAlchemyError as exc:
            self.db.rollback()
            logger.exception("Database save failed for quote: %s", quote.q)
            raise DatabaseSaveError("Database save failed while storing generated quote.") from exc

    def get_all_quotes(self) -> list[Quote]:
        return self.db.scalars(
            select(Quote)
        ).all()

    def get_quote_by_id(self, quote_id: int) -> Quote | None:
        return self.db.scalar(
            select(Quote).where(Quote.id == quote_id)
        )

    def get_random_quotes(self, limit: int = 50) -> list[Quote]:
        return self.db.scalars(
            select(Quote)
            .order_by(func.random())
            .limit(limit)
        ).all()

    def quote_exists_by_text(self, quote_text: str) -> bool:
        normalized_quote = quote_text.strip().lower()

        existing_quote_id = self.db.scalar(
            select(Quote.id)
            .where(func.lower(func.trim(Quote.q)) == normalized_quote)
            .limit(1)
        )

        return existing_quote_id is not None

    def update_quote(self, quote: Quote) -> Quote:
        self.db.commit()
        self.db.refresh(quote)
        return quote

    def delete_quote(self, quote: Quote) -> None:
        self.db.delete(quote)
        self.db.commit()

    def count_quotes(self) -> int:
        return self.db.query(Quote).count()