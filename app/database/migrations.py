"""Lightweight SQLite schema migrations for local development."""

from __future__ import annotations

from sqlalchemy import inspect, text
from sqlalchemy.engine import Engine


def _has_column(engine: Engine, table_name: str, column_name: str) -> bool:
    inspector = inspect(engine)
    columns = inspector.get_columns(table_name)
    return any(column["name"] == column_name for column in columns)


def migrate_sqlite_schema(engine: Engine) -> None:
    """Apply additive SQLite migrations needed for existing local databases."""
    if engine.dialect.name != "sqlite":
        return

    with engine.begin() as connection:
        if _has_column(engine, "heart_rate", "patient_id") is False:
            connection.execute(text("ALTER TABLE heart_rate ADD COLUMN patient_id VARCHAR(36)"))
        if _has_column(engine, "heart_rate", "created_at") is False:
            connection.execute(text("ALTER TABLE heart_rate ADD COLUMN created_at DATETIME"))

        if _has_column(engine, "steps", "patient_id") is False:
            connection.execute(text("ALTER TABLE steps ADD COLUMN patient_id VARCHAR(36)"))
        if _has_column(engine, "steps", "created_at") is False:
            connection.execute(text("ALTER TABLE steps ADD COLUMN created_at DATETIME"))
