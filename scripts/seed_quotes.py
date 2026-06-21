import json

from app.database.database import SessionLocal
from app.models.quote import Quote
from app.services.quote_service import QuoteService
from app.repositories.quote_repository import QuoteRepository


def seed_quotes():

    db = SessionLocal()

    repository = QuoteRepository(db)
    service = QuoteService(repository)

    with open("data/quotes.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    quotes = data["quotes"]

    inserted = 0

    for item in quotes:

        quote = Quote(
            q=item["quote"],
            a=item["author"]
        )

        service.create_quote(quote)
        inserted += 1

    db.close()

    print(f"Inserted {inserted} quotes successfully!")


if __name__ == "__main__":
    seed_quotes()