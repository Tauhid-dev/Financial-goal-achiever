import os
from pydantic import Field
from pydantic_settings import BaseSettings

class Config(BaseSettings):
    # Core configuration – values are read from the environment or .env file
    DATABASE_URL: str = Field(..., env="DATABASE_URL")
    ENV: str = Field("production", env="ENV")
    LOG_LEVEL: str = Field("INFO", env="LOG_LEVEL")
    JWT_SECRET: str = Field(..., env="JWT_SECRET")  # required, no fallback
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(60, env="ACCESS_TOKEN_EXPIRE_MINUTES")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
