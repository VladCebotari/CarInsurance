from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.exceptions.db_exceptions import register_db_exceptions
from app.utils.custom_exception import AppException


async def custom_exception_handler(
        request: Request,
        exc: AppException,
) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error_code": exc.error_code,
            "detail": exc.message,
        },
    )


async def request_validation_exception_handler(
        request: Request,
        exc: RequestValidationError,
) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={
            "error_code": "request_validation_error",
            "detail": _format_validation_errors(exc),
        },
    )


async def http_exception_handler(
        request: Request,
        exc: HTTPException,
) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error_code": "http_error",
            "detail": str(exc.detail),
        },
    )


async def internal_exception_handler(
        request: Request,
        exc: Exception,
) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content={
            "error_code": "internal_error",
            "detail": "Internal server error",
        },
    )


def _format_validation_errors(exc: RequestValidationError) -> str:
    formatted_errors = []

    for error in exc.errors():
        formatted_errors.append(_format_validation_error(error))

    if not formatted_errors:
        return "Please check the request and try again."

    return "; ".join(formatted_errors)


def _format_validation_error(error: dict) -> str:
    field = _format_validation_location(error.get("loc", []))
    error_type = error.get("type", "")
    context = error.get("ctx", {})

    if error_type == "missing":
        message = "is required"
    elif error_type == "greater_than":
        message = f"must be greater than {context.get('gt')}"
    elif error_type == "greater_than_equal":
        message = f"must be greater than or equal to {context.get('ge')}"
    elif error_type == "less_than":
        message = f"must be less than {context.get('lt')}"
    elif error_type == "less_than_equal":
        message = f"must be less than or equal to {context.get('le')}"
    elif error_type == "string_too_long":
        message = f"must be at most {context.get('max_length')} characters"
    elif error_type == "string_too_short":
        message = f"must be at least {context.get('min_length')} characters"
    elif error_type in ("int_parsing", "int_type"):
        message = "must be a whole number"
    elif error_type in ("float_parsing", "float_type"):
        message = "must be a number"
    elif error_type in ("uuid_parsing", "uuid_type"):
        message = "must be a valid UUID"
    elif error_type in ("date_from_datetime_parsing", "date_parsing", "date_type"):
        message = "must be a valid date"
    elif error_type == "enum":
        message = f"must be one of: {context.get('expected')}"
    else:
        message = "has an invalid value"

    if field:
        return f"The {field} field {message}"

    return f"The request {message}"


def _format_validation_location(location: list) -> str:
    field_parts = [
        str(part).replace("_", " ")
        for part in location
        if part not in ("body", "query", "path")
    ]

    return " ".join(field_parts)


def register_custom_exception_handlers(app: FastAPI) -> None:
    register_db_exceptions(app)
    app.add_exception_handler(AppException, custom_exception_handler)
    app.add_exception_handler(
        RequestValidationError,
        request_validation_exception_handler,
    )
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(Exception, internal_exception_handler)
