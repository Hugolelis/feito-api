import logging
import time

from fastapi import Request, Response
from starlette.middleware.base import RequestResponseEndpoint

logger = logging.getLogger("feito.access")


async def log_requests(request: Request, call_next: RequestResponseEndpoint) -> Response:
    start = time.perf_counter()
    response = await call_next(request)
    ms = (time.perf_counter() - start) * 1000
    status = response.status_code
    level = logging.ERROR if status >= 500 else logging.WARNING if status >= 400 else logging.INFO
    logger.log(level, "%s %s %s %.1fms", request.method, request.url.path, status, ms)
    return response
