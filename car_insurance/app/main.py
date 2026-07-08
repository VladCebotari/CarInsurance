from fastapi import FastAPI

from app.api.routers.cars import cars_router
from app.api.routers.licenses import licenses_router
from app.api.routers.owners import owners_router
from app.exceptions.register_handlers import register_custom_exception_handlers
from app.middleware.pagination import PaginationMiddleware
from app.utils.logging import configure_logging

app = FastAPI(
    title="Insurance API",
    version="1.0.0",
)
configure_logging()
app.add_middleware(PaginationMiddleware)

app.include_router(licenses_router)
app.include_router(owners_router)
app.include_router(cars_router)
register_custom_exception_handlers(app)
