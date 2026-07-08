"""Pagination middleware storing request objects in context."""

from __future__ import annotations

from contextvars import ContextVar

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

request_object: ContextVar[Request | None] = ContextVar("request", default=None)


class PaginationMiddleware(BaseHTTPMiddleware):  # pylint: disable=too-few-public-methods
    """Attach the current request to a context variable."""

    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint,
    ) -> Response:
        """Store request in context for downstream pagination helpers."""
        token = request_object.set(request)
        try:
            response = await call_next(request)
        finally:
            request_object.reset(token)
        return response
