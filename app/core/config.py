"""Application configuration from environment."""

import os
from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment."""

    database_url: str = "sqlite:///./data/health.db"
    environment: str = "development"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


def get_database_path() -> Path:
    """Resolve database file path for SQLite URL like sqlite:///./data/health.db."""
    url = Settings().database_url
    if url.startswith("sqlite:///"):
        path_str = url.replace("sqlite:///", "").lstrip("/")
        path = Path(path_str)
        path.parent.mkdir(parents=True, exist_ok=True)
        return path
    raise ValueError("Only SQLite database_url is supported (sqlite:///path/to/file.db)")


settings = Settings()
