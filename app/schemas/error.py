"""Standard API error schemas."""

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class FieldError(BaseModel):
    field: str
    message: str


class ApiError(BaseModel):
    detail: str = Field(..., examples=["Patient not found"])
    code: str = Field(..., examples=["NOT_FOUND"])
    field: Optional[str] = Field(default=None, examples=["patient_id"])


class ApiValidationError(BaseModel):
    detail: str = Field(default="Validation failed")
    code: str = Field(default="VALIDATION_ERROR")
    errors: list[FieldError]
