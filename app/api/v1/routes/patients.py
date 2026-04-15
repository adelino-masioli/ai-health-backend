"""Patient API routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.dependencies.auth import authenticated
from app.repositories import patient_repository
from app.schemas.patient import PatientCreate, PatientResponse

router = APIRouter(prefix="/patients", tags=["patients"])


@router.post("", response_model=PatientResponse, status_code=201)
def create_patient(
    data: PatientCreate,
    _: str = Depends(authenticated),
    db: Session = Depends(get_db),
) -> PatientResponse:
    """Create a patient record."""
    existing = patient_repository.get_patient_by_email(db, data.email)
    if existing is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "detail": "Email is already registered",
                "code": "CONFLICT",
                "field": "email",
            },
        )
    try:
        model = patient_repository.create_patient(db, data)
    except IntegrityError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "detail": "Email is already registered",
                "code": "CONFLICT",
                "field": "email",
            },
        ) from exc
    return PatientResponse.model_validate(model)


@router.get("", response_model=list[PatientResponse])
def list_patients(
    _: str = Depends(authenticated),
    db: Session = Depends(get_db),
) -> list[PatientResponse]:
    """List patient records ordered by most recent first."""
    models = patient_repository.list_patients(db)
    return [PatientResponse.model_validate(model) for model in models]


@router.get("/{patient_id}", response_model=PatientResponse)
def get_patient(
    patient_id: str,
    _: str = Depends(authenticated),
    db: Session = Depends(get_db),
) -> PatientResponse:
    """Return a patient by identifier."""
    model = patient_repository.get_patient_by_id(db, patient_id)
    if model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "detail": "Patient not found",
                "code": "NOT_FOUND",
                "field": "patient_id",
            },
        )
    return PatientResponse.model_validate(model)
