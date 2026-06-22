from app.schemas.quote_schema import QuoteSchema


class QuoteValidator:

    def validate_quotes(
        self,
        quotes: list[QuoteSchema]
    ) -> list[QuoteSchema]:

        validated_quotes = []
        seen_quotes = set()

        for quote in quotes:

            if not self._is_valid_quote(quote):
                continue

            normalized_quote = quote.q.strip().lower()

            if normalized_quote in seen_quotes:
                continue

            seen_quotes.add(normalized_quote)
            validated_quotes.append(quote)

        return validated_quotes

    def _is_valid_quote(self, quote: QuoteSchema) -> bool:

        if not quote.q.strip():
            return False

        if not quote.a.strip():
            return False

        return True