from app.providers.gemini_provider import GeminiProvider
from app.services.ai_quote_service import AIQuoteService
from app.validator.quote_validator import QuoteValidator

provider = GeminiProvider()
validator = QuoteValidator()
service = AIQuoteService(provider, validator)

print(service.generate_quotes(10))