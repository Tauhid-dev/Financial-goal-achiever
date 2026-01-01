import os
from pydantic import Field
from pydantic_settings import BaseSettings

class DBConfig(BaseSettings):
    # DATABASE_URL is required; placeholder values are in .env.example
    DATABASE_URL: str = Field(..., env="DATABASE_URL")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"
