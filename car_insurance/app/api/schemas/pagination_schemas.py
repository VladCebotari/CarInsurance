from typing import Generic, TypeVar

from pydantic import AnyHttpUrl, BaseModel, Field

M = TypeVar("M")


class PaginatedResponse(BaseModel, Generic[M]):
    """Standard paginated response wrapper."""

    count: int = Field(description="Number of total items")
    items: list[M] = Field(description="List of items returned in a paginated response")
    next_page: AnyHttpUrl | None = Field(
        None,
        description="url of the next page if it exists",
    )
    previous_page: AnyHttpUrl | None = Field(
        None,
        description="url of the previous page if it exists",
    )
