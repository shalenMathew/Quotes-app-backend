from app.providers.ai_provider import AIProvider
from app.validators.quote_validator import QuoteValidator


class AIQuoteService:

    def __init__(
        self,
        provider: AIProvider,
        validator: QuoteValidator
    ):
        self.provider = provider
        self.validator = validator

    def generate_quotes(self, count: int):

        generated_quotes = self.provider.generate_quotes(count)

        validated_quotes = self.validator.validate_quotes(generated_quotes)

        return validated_quotes