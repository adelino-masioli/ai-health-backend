"""Authentication helper routes."""

from fastapi import APIRouter, Depends

from app.dependencies.auth import authenticated

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/check")
def check_authentication(_: str = Depends(authenticated)) -> dict[str, bool]:
    """Validate API key credentials without touching business data."""
    return {"authenticated": True}
