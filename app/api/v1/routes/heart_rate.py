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


@router.get("/{patient_id}", response_model=list[HeartRateResponse], status_code=200)
def list_heart_rates(
    patient_id: str,
    _: str = Depends(authenticated),
    db: Session = Depends(get_db),
) -> list[HeartRateResponse]:
    """List heart rate records for a patient in the default analysis window."""
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
    model_list = heart_rate_repository.list_heart_rates_by_patient(
        db,
        patient_id=patient_id,
        start_time=heart_rate_repository.window_start(24 * 30),
    )
    return [HeartRateResponse.model_validate(model) for model in model_list]
