class AppException(Exception):
    status_code: int = 500
    error_code: str = "INTERNAL_ERROR"

    def __init__(self, message:str):
        self.message=message
        super().__init__(message)

class BadRequestError(AppException):
    status_code = 400
    error_code = "BAD_REQUEST"


class UnauthorizedError(AppException):
    status_code = 401
    error_code = "UNAUTHORIZED"


class InternalServerError(AppException):
    status_code = 500
    error_code = "INTERNAL_SERVER_ERROR"
