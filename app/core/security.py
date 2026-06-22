from pathlib import Path
import os
import secrets

from dotenv import load_dotenv
from fastapi import Header, HTTPException, status

load_dotenv(dotenv_path=Path(__file__).resolve().parents[1] / ".env")

ADMIN_API_KEY = os.getenv("ADMIN_API_KEY")


def verify_admin_key(x_admin_key: str | None = Header(default=None)) -> None:
    if not ADMIN_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="ADMIN_API_KEY is not configured."
        )

    if not x_admin_key or not secrets.compare_digest(x_admin_key, ADMIN_API_KEY):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid admin API key."
        )