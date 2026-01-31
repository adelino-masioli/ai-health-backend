"""Pydantic schemas for steps."""

from datetime import date

from pydantic import BaseModel, Field


class StepsCreate(BaseModel):
    """Request body for creating a steps record."""

    total: int = Field(..., ge=0, le=100_000, description="Total steps (0-100000)")
    date: date


class StepsResponse(BaseModel):
    """Response body for a steps record."""

    id: int
    total: int
    date: date

    model_config = {"from_attributes": True}
