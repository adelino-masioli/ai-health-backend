"""Application configuration from environment."""

from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment."""

    database_url: str = "sqlite:///./data/health.db"
    environment: str = "development"
    api_keys: str = Field(default="dev-api-key")
    cors_origins: str = Field(default="http://localhost:3000,http://localhost:8080")
    rate_limit_requests: int = 60
    rate_limit_window_seconds: int = 60

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @property
    def parsed_api_keys(self) -> set[str]:
        return {x.strip() for x in self.api_keys.split(",") if x.strip()}

    @property
    def parsed_cors_origins(self) -> list[str]:
        return [x.strip() for x in self.cors_origins.split(",") if x.strip()]


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
