"""Repository for heart rate records."""

from datetime import datetime, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.heart_rate import HeartRate
from app.schemas.heart_rate import HeartRateCreate


def create_heart_rate(db: Session, data: HeartRateCreate) -> HeartRate:
    """Persist a heart rate record and return it."""
    model = HeartRate(
        patient_id=str(data.patient_id),
        value=data.value,
        timestamp=data.timestamp,
    )
    db.add(model)
    db.commit()
    db.refresh(model)
    return model


def list_heart_rates_by_patient(
    db: Session,
    patient_id: str,
    start_time: datetime,
) -> list[HeartRate]:
    """List heart rate records for a patient in a time window."""
    stmt = (
        select(HeartRate)
        .where(HeartRate.patient_id == patient_id)
        .where(HeartRate.timestamp >= start_time)
        .order_by(HeartRate.timestamp.desc())
    )
    return list(db.execute(stmt).scalars().all())


def window_start(window_hours: int) -> datetime:
    """Returns UTC start datetime for analysis window."""
    return datetime.now(timezone.utc) - timedelta(hours=window_hours)
