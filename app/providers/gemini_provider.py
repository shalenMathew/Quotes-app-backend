from pathlib import Path
import os

from dotenv import load_dotenv
from google import genai

from app.providers.ai_provider import AIProvider
from app.schemas.quote_schema import QuoteSchema

load_dotenv(dotenv_path=Path(__file__).resolve().parents[1] / ".env")


class GeminiProvider(AIProvider):

    def __init__(self):
        self.client = genai.Client(
            api_key=os.getenv("GEMINI_API_KEY")
        )

    def generate_quotes(self, count: int):
        prompt = f"""
You are an expert writer of original motivational and philosophical quotes.

Generate exactly {count} original quotes.

Requirements:

- You may include a mix of:
  - Original quotes created by you.
  - Well-known public quotes from real authors when appropriate.
- If a quote is a real quote, provide the correct author's name.
- If a quote is original, set the author to "Unknown".
- Keep each quote between 8 and 20 words when possible.
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

        response = self.client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "response_schema": list[QuoteSchema],
            },
        )

        return response.parsed