import logging
import time

from fastapi import Request

logger=logging.getLogger(__name__)

async def log_request(request: Request, call_next):
    start_time=time.perf_counter()
    response = await call_next(request)
    response_time=time.perf_counter() - start_time
    logger.info(
        "%s %s %d %.3fs",
        request.method,
        request.url.path,
        response.status_code,
        response_time,
    )
    return response
