from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.quote import Quote


class QuoteRepository:

    def __init__(self, db: Session):
        self.db = db

    def create_quote(self, quote: Quote) -> Quote:
        self.db.add(quote)
        self.db.commit()
        self.db.refresh(quote)
        return quote

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

    def update_quote(self, quote: Quote) -> Quote:
        self.db.commit()
        self.db.refresh(quote)
        return quote

    def delete_quote(self, quote: Quote) -> None:
        self.db.delete(quote)
        self.db.commit()

    def count_quotes(self) -> int:
        return self.db.query(Quote).count()