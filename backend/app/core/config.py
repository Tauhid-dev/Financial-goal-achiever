import os

class Config:
    """
    Minimal core configuration for testing.
    Uses environment variables when available, otherwise defaults.
    """
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///:memory:")
    ENV: str = os.getenv("ENV", "production")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    JWT_SECRET: str = os.getenv("JWT_SECRET", "test-secret")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
