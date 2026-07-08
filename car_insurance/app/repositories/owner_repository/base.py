from typing import Protocol
from uuid import UUID

from app.api.schemas.owner_schemas import OwnerUpdate
from app.api.schemas.pagination_schemas import PaginatedResponse
from app.db.models import Owner
from app.utils.enums.driver_license_category import DriverLicenseCategory


class OwnerRepository(Protocol):
    def get_owners(
        self,
        page: int,
        per_page: int,
        category: list[DriverLicenseCategory] | None = None,
        email: str | None = None,
    ) -> PaginatedResponse: ...

    def create(self, data: Owner) -> Owner: ...

    def get_by_id(self, owner_id: UUID) -> Owner: ...

    def get_by_email(self, email: str) -> Owner: ...

    def update(self, owner: Owner, data: OwnerUpdate) -> Owner: ...

    def delete_owner(self, owner: Owner) -> None: ...
