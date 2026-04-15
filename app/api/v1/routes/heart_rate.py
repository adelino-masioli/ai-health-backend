"""Heart rate API routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.dependencies.auth import authenticated
from app.repositories import heart_rate_repository, patient_repository
from app.schemas.heart_rate import HeartRateCreate, HeartRateResponse

router = APIRouter(prefix="/heart-rate", tags=["heart-rate"])


@router.post("", response_model=HeartRateResponse, status_code=201)
def create_heart_rate(
    data: HeartRateCreate,
    _: str = Depends(authenticated),
    db: Session = Depends(get_db),
) -> HeartRateResponse:
    """Create a heart rate record. Validates value in 30-220 bpm."""
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
    model = heart_rate_repository.create_heart_rate(db, data)
    return HeartRateResponse.model_validate(model)
