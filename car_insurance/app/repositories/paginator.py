from __future__ import annotations

from math import ceil
from typing import TypeVar

from sqlalchemy import Select, func, select
from sqlalchemy.orm import Session

from app.api.schemas.pagination_schemas import PaginatedResponse
from app.middleware.pagination import request_object

M = TypeVar("M")


class Paginator:
    def __init__(self, session: Session, query: Select, page: int, per_page: int) -> None:
        self.session = session
        self.query = query
        self.page = page
        self.per_page = per_page
        self.offset = (page - 1) * per_page
        self.request = request_object.get()
        self.number_of_pages = 0

    def get_response(self) -> PaginatedResponse[M]:
        count = self._get_total_count()
        items = list(
            self.session.scalars(
                self.query.limit(self.per_page).offset(self.offset)
            ).all()
        )

        return PaginatedResponse(
            count=count,
            next_page=self._get_next_page(),
            previous_page=self._get_previous_page(),
            items=items,
        )

    def _get_next_page(self) -> str | None:
        if self.request is None:
            return None

        if self.page >= self.number_of_pages:
            return None

        return str(
            self.request.url.include_query_params(
                page=self.page + 1,
                per_page=self.per_page,
            )
        )

    def _get_previous_page(self) -> str | None:
        if self.request is None:
            return None

        if self.page <= 1 or self.page > self.number_of_pages + 1:
            return None

        return str(
            self.request.url.include_query_params(
                page=self.page - 1,
                per_page=self.per_page,
            )
        )

    def _get_total_count(self) -> int:
        count = self.session.scalar(select(func.count()).select_from(self.query.subquery()))
        total = int(count or 0)
        self.number_of_pages = self._get_number_of_pages(total)
        return total

    def _get_number_of_pages(self, count: int) -> int:
        if self.per_page <= 0:
            return 0

        return ceil(count / self.per_page)


class PaginationRepositoryMixin:
    db: Session

    def paginate_query(
        self,
        query: Select,
        page: int,
        per_page: int,
    ) -> PaginatedResponse:
        paginator = Paginator(self.db, query, page, per_page)
        return paginator.get_response()
