from typing import Protocol
from uuid import UUID

from app.api.schemas.pagination_schemas import PaginatedResponse
from app.db.models import Car
from app.utils.enums.car_category import CarCategory


class CarRepository(Protocol):
    def get_cars(
        self,
        page: int,
        per_page: int,
        make: str | None = None,
        model: str | None = None,
        category: CarCategory | None = None,
        owner_id: UUID | None = None,
    ) -> PaginatedResponse: ...

    def get_car_by_id(self, car_id: UUID) -> Car: ...

    def create_car(self, request: Car) -> Car: ...

    def get_by_vin(self, vin: str) -> Car | None: ...

    def delete_car(self, car: Car) -> None: ...
