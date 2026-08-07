class AppException(Exception):
    def __init__(
        self,
        status_code: int,
        error_code: str,
        message: str,
    ) -> None:
        self.status_code = status_code
        self.error_code = error_code
        self.message = message
        super().__init__(message)


class BadRequestError(AppException):
    def __init__(self, message: str) -> None:
        super().__init__(
            status_code=400,
            error_code="BAD_REQUEST",
            message=message,
        )


class UnauthorizedError(AppException):
    def __init__(self, message: str = "Unauthorized") -> None:
        super().__init__(
            status_code=401,
            error_code="UNAUTHORIZED",
            message=message,
        )


class InternalServerError(AppException):
    def __init__(
        self,
        message: str = "Internal server error",
    ) -> None:
        super().__init__(
            status_code=500,
            error_code="INTERNAL_SERVER_ERROR",
            message=message,
        )


class DomainException(Exception):
    """Base class for all business/domain exceptions."""
    pass


class InvalidConversationTitle(DomainException):
    def __init__(self, message: str = "Conversation title cannot be empty."):
        super().__init__(message)
        
class ConversationNotFound(DomainException):
    pass

class InvalidEnum(DomainException):
    pass

class MessageNotFound(DomainException):
    pass

class PromptNotFound(DomainException):
    pass