"""Pydantic schemas for steps."""

from datetime import datetime, timezone
from uuid import UUID

from pydantic import BaseModel, Field, field_validator


class StepsCreate(BaseModel):
    """Request body for creating a steps record."""

    patient_id: UUID = Field(
        ...,
        description="Patient UUID identifier.",
        examples=["6f05243f-57c5-4e74-8545-3318db77845d"],
    )
    total: int = Field(..., ge=0, le=100_000, description="Total steps (0-100000).", examples=[8450])
    date: datetime = Field(
        ...,
        description="Reference datetime for step count in UTC (ISO 8601).",
        examples=["2026-01-30T00:00:00Z"],
    )

    @field_validator("date", mode="after")
    @classmethod
    def normalize_date_to_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc)


class StepsResponse(BaseModel):
    """Response body for a steps record."""

    id: int
    patient_id: str
    total: int
    date: datetime
    created_at: datetime

    model_config = {"from_attributes": True}
