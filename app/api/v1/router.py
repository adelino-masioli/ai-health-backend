"""API v1 router aggregating all v1 routes."""

from fastapi import APIRouter

from app.api.v1.routes import heart_rate, steps

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(heart_rate.router)
api_router.include_router(steps.router)
