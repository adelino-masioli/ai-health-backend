"""Analysis API routes."""

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.dependencies.auth import authenticated
from app.repositories import heart_rate_repository, patient_repository, steps_repository
from app.schemas.analysis import AnalysisResponse
from app.services.analysis_service import analyze_vitals

router = APIRouter(prefix="/analysis", tags=["analysis"])


@router.get("/{patient_id}", response_model=AnalysisResponse, status_code=200)
def get_patient_analysis(
    patient_id: str = Path(..., description="Patient UUID identifier."),
    window_hours: int = Query(24, ge=1, le=720),
    _: str = Depends(authenticated),
    db: Session = Depends(get_db),
) -> AnalysisResponse:
    """Analyzes patient health records in the configured time window."""
    patient = patient_repository.get_patient_by_id(db, patient_id)
    if patient is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"detail": "Patient not found", "code": "NOT_FOUND", "field": "patient_id"},
        )

    start = heart_rate_repository.window_start(window_hours)
    heart_rates = heart_rate_repository.list_heart_rates_by_patient(
        db, patient_id=patient_id, start_time=start
    )
    steps = steps_repository.list_steps_by_patient(db, patient_id=patient_id, start_time=start)
    alerts = analyze_vitals(heart_rates, steps)
    return AnalysisResponse(
        patient_id=patient_id,
        generated_at=datetime.now(timezone.utc),
        window_hours=window_hours,
        alerts=alerts,
    )
