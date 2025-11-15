from fastapi import HTTPException, status

from app.models import Error, ErrorCode, ErrorResponse


class NotFoundException(HTTPException):
    def __init__(self, message: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorResponse(
                error=Error(
                    code=ErrorCode.NOT_FOUND,
                    message=message,
                )
            ).model_dump(),
        )


class ConflictException(HTTPException):
    def __init__(
        self, code: ErrorCode, message: str, status_code: int = status.HTTP_409_CONFLICT
    ):
        super().__init__(
            status_code=status_code,
            detail=ErrorResponse(
                error=Error(
                    code=code,
                    message=message,
                )
            ).model_dump(),
        )
