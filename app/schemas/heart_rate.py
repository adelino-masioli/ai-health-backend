"""Pydantic schemas for heart rate."""

from datetime import datetime, timezone
from uuid import UUID

from pydantic import BaseModel, Field, field_validator


class HeartRateCreate(BaseModel):
    """Request body for creating a heart rate record."""

    patient_id: UUID = Field(
        ...,
        description="Patient UUID identifier.",
        examples=["6f05243f-57c5-4e74-8545-3318db77845d"],
    )
    value: int = Field(..., ge=30, le=220, description="Heart rate in bpm (30-220).", examples=[72])
    timestamp: datetime = Field(
        ...,
        description="Measurement timestamp in UTC (ISO 8601).",
        examples=["2026-01-30T10:15:00Z"],
    )

    @field_validator("timestamp", mode="after")
    @classmethod
    def normalize_timestamp_to_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc)


class HeartRateResponse(BaseModel):
    """Response body for a heart rate record."""

    id: int
    patient_id: str
    value: int
    timestamp: datetime
    created_at: datetime

    model_config = {"from_attributes": True}
