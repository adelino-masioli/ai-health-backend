"""Repository for heart rate records."""

from datetime import datetime

from sqlalchemy.orm import Session

from app.models.heart_rate import HeartRate
from app.schemas.heart_rate import HeartRateCreate


def create_heart_rate(db: Session, data: HeartRateCreate) -> HeartRate:
    """Persist a heart rate record and return it."""
    model = HeartRate(value=data.value, timestamp=data.timestamp)
    db.add(model)
    db.commit()
    db.refresh(model)
    return model


def list_heart_rates(
    db: Session,
    limit: int = 100,
    offset: int = 0,
) -> list[HeartRate]:
    """List heart rate records ordered by timestamp descending."""
    return (
        db.query(HeartRate)
        .order_by(HeartRate.timestamp.desc())
        .limit(limit)
        .offset(offset)
        .all()
    )
