"""Steps API routes."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.repositories import steps_repository
from app.schemas.steps import StepsCreate, StepsResponse

router = APIRouter(prefix="/steps", tags=["steps"])


@router.post("", response_model=StepsResponse, status_code=201)
def create_steps(
    data: StepsCreate,
    db: Session = Depends(get_db),
) -> StepsResponse:
    """Create a steps record. Validates total in 0-100000."""
    model = steps_repository.create_steps(db, data)
    return StepsResponse.model_validate(model)


@router.get("", response_model=list[StepsResponse])
def list_steps(
    db: Session = Depends(get_db),
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
) -> list[StepsResponse]:
    """List steps records (newest first)."""
    models = steps_repository.list_steps(db, limit=limit, offset=offset)
    return [StepsResponse.model_validate(m) for m in models]
