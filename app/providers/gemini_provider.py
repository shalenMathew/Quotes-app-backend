from pathlib import Path
import logging
import os

from dotenv import load_dotenv
from google import genai

from app.core.exceptions import GeminiGenerationError, InvalidAIResponseError
from app.providers.ai_provider import AIProvider
from app.schemas.quote_schema import QuoteSchema

load_dotenv(dotenv_path=Path(__file__).resolve().parents[1] / ".env")

logger = logging.getLogger(__name__)


class GeminiProvider(AIProvider):

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise GeminiGenerationError("GEMINI_API_KEY is not configured.")

        self.client = genai.Client(api_key=api_key)

    def generate_quotes(self, count: int) -> list[QuoteSchema]:
        prompt = f"""
You are an expert writer of original motivational and philosophical quotes.

Generate exactly {count} original quotes.

Requirements:

- You may include a mix of:
  - Original quotes created by you.
  - Well-known public quotes from real authors when appropriate.
- If a quote is a real quote, provide the correct author's name.
- If a quote is original, set the author to "Unknown".
- Keep each quote between 8 and 25 words when possible.
- Make every quote meaningful, memorable, and emotionally impactful.
- Avoid repeating the same idea.
- Do not include numbering.
- Do not include markdown.
- Do not include explanations.
- Quotes should not be cliche.
- Return only valid JSON.

Output format:

[
  {{
    "q": "...",
    "a": "Unknown"
  }}
]
"""

        try:
            response = self.client.models.generate_content(
                model="gemini-3.5-flash",
                contents=prompt,
                config={
                    "response_mime_type": "application/json",
                    "response_schema": list[QuoteSchema],
                },
            )
        except Exception as exc:
            logger.exception("Gemini failed while generating %s quotes.", count)
            raise GeminiGenerationError("Gemini failed to generate quotes.") from exc

        parsed_response = response.parsed

        if not isinstance(parsed_response, list) or not parsed_response:
            logger.error("Invalid AI response from Gemini: %r", parsed_response)
            raise InvalidAIResponseError("Gemini returned an invalid or empty response.")

        invalid_items = [item for item in parsed_response if not isinstance(item, QuoteSchema)]

        if invalid_items:
            logger.error("Gemini response contains invalid quote items: %r", invalid_items)
            raise InvalidAIResponseError("Gemini response did not match the quote schema.")

        logger.info("Gemini generated %s quote candidates.", len(parsed_response))
        return parsed_response