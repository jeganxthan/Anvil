from fastapi import HTTPException


def internal_server_error(error: Exception):
    raise HTTPException(
        status_code=500,
        detail=str(error)
    )


def bad_request(message: str):
    raise HTTPException(
        status_code=400,
        detail=message
    )


def unauthorized(message: str = "Unauthorized"):
    raise HTTPException(
        status_code=401,
        detail=message
    )