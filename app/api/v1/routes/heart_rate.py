"""Heart rate API routes."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.repositories import heart_rate_repository
from app.schemas.heart_rate import HeartRateCreate, HeartRateResponse

router = APIRouter(prefix="/heart-rate", tags=["heart-rate"])


@router.post("", response_model=HeartRateResponse, status_code=201)
def create_heart_rate(
    data: HeartRateCreate,
    db: Session = Depends(get_db),
) -> HeartRateResponse:
    """Create a heart rate record. Validates value in 30-220 bpm."""
    model = heart_rate_repository.create_heart_rate(db, data)
    return HeartRateResponse.model_validate(model)


@router.get("", response_model=list[HeartRateResponse])
def list_heart_rates(
    db: Session = Depends(get_db),
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
) -> list[HeartRateResponse]:
    """List heart rate records (newest first)."""
    models = heart_rate_repository.list_heart_rates(db, limit=limit, offset=offset)
    return [HeartRateResponse.model_validate(m) for m in models]
