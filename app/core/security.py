"""Authentication helpers for API key security."""

from __future__ import annotations

from typing import Optional

from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader

from app.core.config import settings

API_KEY_HEADER_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_HEADER_NAME, auto_error=False)


def require_api_key(api_key: Optional[str] = Security(api_key_header)) -> str:
    """Validates X-API-Key header against configured key set."""
    if api_key and api_key in settings.parsed_api_keys:
        return api_key
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={
            "detail": "Invalid or missing API key",
            "code": "UNAUTHORIZED",
            "field": API_KEY_HEADER_NAME,
        },
    )
