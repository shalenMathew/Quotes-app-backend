import logging

from app.core.exceptions import NoValidQuotesError
from app.models.quote import Quote
from app.providers.ai_provider import AIProvider
from app.repositories.quote_repository import QuoteRepository
from app.validator.quote_validator import QuoteValidator

logger = logging.getLogger(__name__)


class AIQuoteService:

    def __init__(
        self,
        provider: AIProvider,
        validator: QuoteValidator,
        repository: QuoteRepository
    ):
        self.provider = provider
        self.validator = validator
        self.repository = repository

    def generate_and_save_quotes(self, count: int) -> list[Quote]:
        generated_quotes = self.provider.generate_quotes(count)
        validated_quotes = self.validator.validate_quotes(generated_quotes)

        if not validated_quotes:
            logger.warning("No generated quotes passed validation. requested=%s generated=%s", count, len(generated_quotes))
            raise NoValidQuotesError("No generated quotes passed validation.")

        saved_quotes = []
        skipped_existing = 0

        for quote in validated_quotes:
            if self.repository.quote_exists_by_text(quote.q):
                skipped_existing += 1
                logger.info("Skipping existing quote: %s", quote.q)
                continue

            db_quote = Quote(
                q=quote.q,
                a=quote.a
            )

            saved_quote = self.repository.create_quote(db_quote)
            saved_quotes.append(saved_quote)

        logger.info(
            "AI quote pipeline completed. requested=%s generated=%s valid=%s saved=%s skipped_existing=%s",
            count,
            len(generated_quotes),
            len(validated_quotes),
            len(saved_quotes),
            skipped_existing
        )

        return saved_quotes