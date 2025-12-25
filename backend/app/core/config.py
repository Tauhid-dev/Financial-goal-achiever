import os
from pydantic import BaseSettings, Field

class Config(BaseSettings):
    # Core configuration – values are read from the environment or .env file
    DATABASE_URL: str = Field(..., env="DATABASE_URL")
    ENV: str = Field("production", env="ENV")
    LOG_LEVEL: str = Field("INFO", env="LOG_LEVEL")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
