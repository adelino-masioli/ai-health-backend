"""Patient SQLAlchemy model."""

from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


class Patient(Base):
    """Patient identity stored in the database."""

    __tablename__ = "patients"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid4()),
    )
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(254), unique=True, nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utc_now)

    heart_rates = relationship("HeartRate", back_populates="patient", cascade="all,delete")
    steps = relationship("Steps", back_populates="patient", cascade="all,delete")
