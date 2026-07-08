from uuid import UUID

from starlette import status

from app.utils.custom_exception import AppException


class OwnerNotFoundError(AppException):
    def __init__(self, owner_id: UUID):
        super().__init__(
            message=f"Owner with id {owner_id} was not found",
            status_code=status.HTTP_404_NOT_FOUND,
            error_code="owner_not_found",
        )


class OwnerEmailAlreadyExistsError(AppException):
    def __init__(self, email: str):
        super().__init__(
            message=f"Owner with email {email} already exists",
            status_code=status.HTTP_409_CONFLICT,
            error_code="owner_email_already_exists",
        )


class OwnerValidationError(AppException):
    def __init__(self, message: str):
        super().__init__(
            message=message,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            error_code="owner_validation_error",
        )
