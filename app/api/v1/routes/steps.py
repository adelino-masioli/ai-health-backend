"""Steps API routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.dependencies.auth import authenticated
from app.repositories import patient_repository, steps_repository
from app.schemas.steps import StepsCreate, StepsResponse

router = APIRouter(prefix="/steps", tags=["steps"])


@router.post("", response_model=StepsResponse, status_code=201)
def create_steps(
    data: StepsCreate,
    _: str = Depends(authenticated),
    db: Session = Depends(get_db),
) -> StepsResponse:
    """Create a steps record. Validates total in 0-100000."""
    patient = patient_repository.get_patient_by_id(db, str(data.patient_id))
    if patient is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "detail": "Patient not found",
                "code": "NOT_FOUND",
                "field": "patient_id",
            },
        )
    model = steps_repository.create_steps(db, data)
    return StepsResponse.model_validate(model)
