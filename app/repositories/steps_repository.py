"""Repository for steps records."""

from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.steps import Steps
from app.schemas.steps import StepsCreate


def create_steps(db: Session, data: StepsCreate) -> Steps:
    """Persist a steps record and return it."""
    model = Steps(
        patient_id=str(data.patient_id),
        total=data.total,
        date=data.date,
    )
    db.add(model)
    db.commit()
    db.refresh(model)
    return model


def list_steps_by_patient(
    db: Session,
    patient_id: str,
    start_time: datetime,
) -> list[Steps]:
    """List steps records for a patient in a time window."""
    stmt = (
        select(Steps)
        .where(Steps.patient_id == patient_id)
        .where(Steps.date >= start_time)
        .order_by(Steps.date.desc())
    )
    return list(db.execute(stmt).scalars().all())
