from app.providers.gemini_provider import GeminiProvider
from app.services.ai_quote_service import AIQuoteService

provider = GeminiProvider()

service = AIQuoteService(provider)

print(service.generate_quotes(10))