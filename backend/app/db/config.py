import os
from pydantic_settings import BaseSettings  # Use dummy BaseSettings from project root

class DBConfig:
    """
    Minimal DB configuration for testing.
    Falls back to an in‑memory SQLite URL if DATABASE_URL is not set.
    """
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///:memory:")
