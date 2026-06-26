from app.models.quote import Quote
from app.repositories.quote_repository import QuoteRepository


class QuoteService:

    def __init__(self, repository: QuoteRepository):
        self.repository = repository


    def create_quote(self, quote: Quote) -> Quote:
        return self.repository.create_quote(quote)

    def get_all_quotes(self) -> list[Quote]:
        return self.repository.get_all_quotes()

    def get_quote_by_id(self, quote_id: int) -> Quote | None:
        return self.repository.get_quote_by_id(quote_id)

    def get_random_quotes(self, limit: int = 20) -> list[Quote]:
        return self.repository.get_random_quotes(limit)

    def update_quote(self, quote: Quote) -> Quote:
        return self.repository.update_quote(quote)

    def delete_quote(self, quote: Quote) -> None:
        self.repository.delete_quote(quote)

    def count_quotes(self) -> int:
        return self.repository.count_quotes()


