"""Simple in-memory rate limiting middleware."""

from collections import defaultdict, deque
from time import time

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Simple fixed-window limiter keyed by API key + path."""

    def __init__(self, app, limit: int, window_seconds: int) -> None:  # type: ignore[no-untyped-def]
        super().__init__(app)
        self.limit = limit
        self.window_seconds = window_seconds
        self.requests: dict[str, deque[float]] = defaultdict(deque)

    async def dispatch(self, request: Request, call_next):  # type: ignore[no-untyped-def]
        if request.url.path in {"/", "/health", "/docs", "/openapi.json", "/redoc"}:
            return await call_next(request)

        api_key = request.headers.get("X-API-Key", "anonymous")
        key = f"{api_key}:{request.url.path}"
        now = time()
        queue = self.requests[key]

        while queue and now - queue[0] > self.window_seconds:
            queue.popleft()

        if len(queue) >= self.limit:
            return JSONResponse(
                status_code=429,
                content={
                    "detail": "Rate limit exceeded",
                    "code": "RATE_LIMIT_EXCEEDED",
                    "field": None,
                },
            )

        queue.append(now)
        return await call_next(request)
