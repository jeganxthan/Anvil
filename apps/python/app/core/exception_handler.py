import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.exceptions import AppException

logger = logging.getLogger(__name__)


async def app_exception_handler(
    request: Request,
    exc: Exception
):
    if isinstance(exc, AppException):

        if exc.status_code >= 500:
            logger.error(
                "%s %s - %s: %s",
                request.method,
                request.url.path,
                exc.error_code,
                exc.message
            )
        else:
            logger.warning(
                "%s %s - %s: %s",
                request.method,
                request.url.path,
                exc.error_code,
                exc.message
            )

        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "error": {
                    "code": exc.error_code,
                    "message": exc.message
                }
            }
        )

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "Internal server error"
            }
        }
    )



def register_exception_handlers(app: FastAPI):
    app.add_exception_handler(
        AppException,
        app_exception_handler
    )
