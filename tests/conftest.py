from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.config import settings
from app.database.base import Base
from app.database.session import get_db
from app.main import app
from app.models import HeartRate, Patient, Steps  # noqa: F401


@pytest.fixture(scope="session")
def test_engine():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def db_session(test_engine) -> Generator[Session, None, None]:
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    session = TestingSessionLocal()
    try:
        session.execute(HeartRate.__table__.delete())
        session.execute(Steps.__table__.delete())
        session.execute(Patient.__table__.delete())
        session.commit()
        yield session
    finally:
        session.close()


@pytest.fixture()
def client(db_session: Session) -> Generator[TestClient, None, None]:
    def override_get_db() -> Generator[Session, None, None]:
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture()
def api_headers() -> dict[str, str]:
    key = next(iter(settings.parsed_api_keys))
    return {"X-API-Key": key}
