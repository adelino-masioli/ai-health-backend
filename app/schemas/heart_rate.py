"""Pydantic schemas for heart rate."""

from datetime import datetime

from pydantic import BaseModel, Field


class HeartRateCreate(BaseModel):
    """Request body for creating a heart rate record."""

    value: int = Field(..., ge=30, le=220, description="Heart rate in bpm (30-220)")
    timestamp: datetime


class HeartRateResponse(BaseModel):
    """Response body for a heart rate record."""

    id: int
    value: int
    timestamp: datetime

    model_config = {"from_attributes": True}
