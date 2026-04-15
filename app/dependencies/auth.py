"""Auth dependencies for route protection."""

from fastapi import Depends

from app.core.security import require_api_key


def authenticated(api_key: str = Depends(require_api_key)) -> str:
    """Ensures request has a valid API key."""
    return api_key
