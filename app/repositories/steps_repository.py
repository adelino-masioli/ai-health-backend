"""Repository for steps records."""

from datetime import date

from sqlalchemy.orm import Session

from app.models.steps import Steps
from app.schemas.steps import StepsCreate


def create_steps(db: Session, data: StepsCreate) -> Steps:
    """Persist a steps record and return it."""
    model = Steps(total=data.total, date=data.date)
    db.add(model)
    db.commit()
    db.refresh(model)
    return model


def list_steps(
    db: Session,
    limit: int = 100,
    offset: int = 0,
) -> list[Steps]:
    """List steps records ordered by date descending."""
    return (
        db.query(Steps)
        .order_by(Steps.date.desc())
        .limit(limit)
        .offset(offset)
        .all()
    )
