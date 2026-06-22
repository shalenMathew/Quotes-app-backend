import re

from app.schemas.quote_schema import QuoteSchema


class QuoteValidator:
    MIN_WORDS = 8
    MAX_WORDS = 25
    MAX_CHARACTERS = 200

    MARKDOWN_PATTERNS = (
        r"^#{1,6}\s+",
        r"^[-*+]\s+",
        r"^>\s+",
        r"`",
        r"\*\*",
        r"__",
    )

    JSON_ARTIFACT_PATTERNS = (
        r'"q"\s*:',
        r'"a"\s*:',
        r"^\s*[\[{]",
        r"[\]}]\s*$",
    )

    NUMBERING_PATTERN = re.compile(r"^\s*\d+[.)]\s+")

    def validate_quotes(
        self,
        quotes: list[QuoteSchema]
    ) -> list[QuoteSchema]:
        validated_quotes = []
        seen_quotes = set()

        for quote in quotes:
            clean_quote = QuoteSchema(
                q=self.normalize_text(quote.q),
                a=self.normalize_text(quote.a)
            )

            if not self._is_valid_quote(clean_quote):
                continue

            dedupe_key = self.get_dedupe_key(clean_quote.q)

            if dedupe_key in seen_quotes:
                continue

            seen_quotes.add(dedupe_key)
            validated_quotes.append(clean_quote)

        return validated_quotes

    def get_dedupe_key(self, quote_text: str) -> str:
        return self.normalize_text(quote_text).lower()

    def normalize_text(self, value: str) -> str:
        return " ".join(value.strip().split())

    def _is_valid_quote(self, quote: QuoteSchema) -> bool:
        if not quote.q:
            return False

        if not quote.a:
            return False

        if len(quote.q) > self.MAX_CHARACTERS:
            return False

        word_count = len(quote.q.split())

        if word_count < self.MIN_WORDS or word_count > self.MAX_WORDS:
            return False

        if self._has_markdown(quote.q):
            return False

        if self._has_numbering(quote.q):
            return False

        if self._has_json_artifacts(quote.q):
            return False

        return True

    def _has_markdown(self, value: str) -> bool:
        return any(
            re.search(pattern, value)
            for pattern in self.MARKDOWN_PATTERNS
        )

    def _has_numbering(self, value: str) -> bool:
        return self.NUMBERING_PATTERN.search(value) is not None

    def _has_json_artifacts(self, value: str) -> bool:
        return any(
            re.search(pattern, value)
            for pattern in self.JSON_ARTIFACT_PATTERNS
        )