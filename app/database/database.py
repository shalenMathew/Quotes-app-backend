from dotenv import load_dotenv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# Load .env
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL is None:
    raise ValueError("DATABASE_URL is not configured.")

# Create Engine
engine = create_engine(DATABASE_URL)

# Session Factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base Class
class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy models.
    """
    pass

# Import models AFTER Base is created
from app.models.quote import Quote

# Create tables
Base.metadata.create_all(bind=engine)