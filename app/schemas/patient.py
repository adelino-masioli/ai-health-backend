"""Pydantic schemas for patient endpoints."""

from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class PatientCreate(BaseModel):
    """Request body for creating a patient."""

    name: str = Field(
        ...,
        min_length=2,
        max_length=120,
        description="Patient full name.",
        examples=["Adelino Masioli"],
    )
    email: EmailStr = Field(
        ...,
        description="Patient email address (must be unique).",
        examples=["adelino@example.com"],
    )


class PatientResponse(BaseModel):
    """Patient response."""

    id: str = Field(..., description="Patient unique identifier (UUID).")
    name: str
    email: EmailStr
    created_at: datetime = Field(
        ..., description="Creation timestamp in UTC (ISO 8601)."
    )

    model_config = {"from_attributes": True}
