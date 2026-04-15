"""Database session and engine configuration."""

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import get_database_path, settings
from app.database.base import Base
from app.database.migrations import migrate_sqlite_schema
from app.models import HeartRate, Patient, Steps  # noqa: F401 - register tables with Base.metadata

# SQLite requires check_same_thread=False for FastAPI async usage with sync sessions
connect_args = {}
if settings.database_url.startswith("sqlite"):
    connect_args["check_same_thread"] = False

engine = create_engine(
    settings.database_url,
    connect_args=connect_args,
    echo=settings.environment == "development",
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db() -> None:
    """Create all tables. Call on application startup."""
    get_database_path()  # ensure data directory exists for SQLite
    Base.metadata.create_all(bind=engine)
    migrate_sqlite_schema(engine)


def get_db() -> Generator[Session, None, None]:
    """Dependency that yields a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
