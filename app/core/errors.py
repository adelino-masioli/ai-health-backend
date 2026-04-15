"""Global exception handlers and standardized API errors."""

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


def _format_validation_error(exc: RequestValidationError) -> dict:
    errors = []
    for item in exc.errors():
        loc = item.get("loc", [])
        field = ".".join(str(x) for x in loc if x not in {"body", "query", "path"})
        errors.append(
            {
                "field": field or "unknown",
                "message": item.get("msg", "Invalid value"),
            }
        )
    return {
        "detail": "Validation failed",
        "code": "VALIDATION_ERROR",
        "errors": errors,
    }


def register_exception_handlers(app: FastAPI) -> None:
    """Registers exception handlers for standardized API error responses."""

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(  # type: ignore[override]
        request: Request,
        exc: RequestValidationError,
    ) -> JSONResponse:
        return JSONResponse(status_code=422, content=_format_validation_error(exc))

    @app.exception_handler(HTTPException)
    async def http_exception_handler(  # type: ignore[override]
        request: Request,
        exc: HTTPException,
    ) -> JSONResponse:
        if isinstance(exc.detail, dict):
            return JSONResponse(status_code=exc.status_code, content=exc.detail)
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": str(exc.detail), "code": "HTTP_ERROR", "field": None},
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(  # type: ignore[override]
        request: Request,
        exc: Exception,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error", "code": "INTERNAL_ERROR", "field": None},
        )
