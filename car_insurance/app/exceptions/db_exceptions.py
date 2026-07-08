from fastapi import FastAPI
from fastapi import Request
from sqlalchemy.exc import (
    IntegrityError,
    OperationalError,
    SQLAlchemyError,
    DatabaseError,
    TimeoutError,
)
from starlette.responses import JSONResponse


async def integrity_error_handler(
        request: Request,
        exc: IntegrityError,
) -> JSONResponse:
    return JSONResponse(
        status_code=409,
        content={
            "error_code": "integrity_error",
            "detail": "The request violates a database rule",
        },
    )


async def timeout_error_handler(
        request: Request,
        exc: TimeoutError,
) -> JSONResponse:
    return JSONResponse(
        status_code=504,
        content={
            "error_code": "database_timeout",
            "detail": "The database took too long to respond",
        },
    )


async def operational_error_handler(
        request: Request,
        exc: OperationalError,
) -> JSONResponse:
    return JSONResponse(
        status_code=503,
        content={
            "error_code": "database_connection_error",
            "detail": "The database is currently unavailable",
        },
    )


async def database_error_handler(
        request: Request,
        exc: DatabaseError,
) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content={
            "error_code": "database_error",
            "detail": "The request could not be completed because of a database error",
        },
    )


async def sqlalchemy_error_handler(
        request: Request,
        exc: SQLAlchemyError,
) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content={
            "error_code": "sqlalchemy_error",
            "detail": "The request could not be completed because of a database error",
        },
    )


def register_db_exceptions(app: FastAPI) -> None:
    app.add_exception_handler(IntegrityError, integrity_error_handler)
    app.add_exception_handler(TimeoutError, timeout_error_handler)
    app.add_exception_handler(OperationalError, operational_error_handler)

    app.add_exception_handler(DatabaseError, database_error_handler)
    app.add_exception_handler(SQLAlchemyError, sqlalchemy_error_handler)
