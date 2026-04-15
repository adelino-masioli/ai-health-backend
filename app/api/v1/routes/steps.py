"""Steps API routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.dependencies.auth import authenticated
from app.repositories import heart_rate_repository
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


@router.get("/{patient_id}", response_model=list[StepsResponse], status_code=200)
def list_steps(
    patient_id: str,
    _: str = Depends(authenticated),
    db: Session = Depends(get_db),
) -> list[StepsResponse]:
    """List steps records for a patient in the default analysis window."""
    patient = patient_repository.get_patient_by_id(db, patient_id)
    if patient is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "detail": "Patient not found",
                "code": "NOT_FOUND",
                "field": "patient_id",
            },
        )
    model_list = steps_repository.list_steps_by_patient(
        db,
        patient_id=patient_id,
        start_time=heart_rate_repository.window_start(24 * 30),
    )
    return [StepsResponse.model_validate(model) for model in model_list]
