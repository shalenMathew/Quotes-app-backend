from sqlalchemy import Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database.database import Base


class Quote(Base):
    __tablename__ = "quotes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    q: Mapped[str] = mapped_column(Text, nullable=False)

    a: Mapped[str] = mapped_column(Text, nullable=False)