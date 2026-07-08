from uuid import UUID

from sqlalchemy import func, or_, select
from sqlalchemy.sql import Select
from sqlalchemy.orm import Session

from app.api.schemas.owner_schemas import OwnerUpdate
from app.db.models import Owner
from app.exceptions.owner_exceptions import OwnerNotFoundError
from app.repositories.owner_repository.base import OwnerRepository
from app.repositories.paginator import PaginationRepositoryMixin
from app.utils.enums.driver_license_category import DriverLicenseCategory


class SqlAlchemyOwnerRepository(PaginationRepositoryMixin, OwnerRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_owners(
        self,
        page: int,
        per_page: int,
        category: list[DriverLicenseCategory] | None = None,
        email: str | None = None,
    ):
        statement = self._apply_filters(
            select(Owner),
            category=category,
            email=email,
        )

        return self.paginate_query(statement, page=page, per_page=per_page)

    def create(self, owner: Owner) -> Owner:
        self.db.add(owner)
        self.db.commit()
        self.db.refresh(owner)

        return owner

    def get_by_id(self, owner_id: UUID) -> Owner:
        statement = select(Owner).where(Owner.id == owner_id)
        owner = self.db.scalar(statement)
        if not owner:
            raise OwnerNotFoundError(owner_id)
        return owner

    def get_by_email(self, email: str) -> Owner:
        statement = select(Owner).where(func.lower(Owner.email) == email.lower())
        return self.db.scalar(statement)

    def update(self, owner: Owner, data: OwnerUpdate) -> Owner:
        update_data = data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(owner, field, value)

        self.db.commit()
        self.db.refresh(owner)

        return owner

    def delete_owner(self, owner: Owner) -> None:
        self.db.delete(owner)
        self.db.commit()

    def _apply_filters(
        self,
        statement: Select,
        category: list[DriverLicenseCategory] | None = None,
        email: str | None = None,
    ) -> Select:
        filters = []

        if category:
            selected_categories = set(category)
            license_categories = [
                item.value
                for item in selected_categories
                if item != DriverLicenseCategory.NONE
            ]

            category_filters = []

            if license_categories:
                category_filters.append(Owner.driver_license_cat.in_(license_categories))

            if DriverLicenseCategory.NONE in selected_categories:
                category_filters.append(Owner.driver_license_cat.is_(None))

            if category_filters:
                filters.append(or_(*category_filters))

        if email:
            filters.append(
                Owner.email.ilike(
                    f"%{self._escape_like(email)}%",
                    escape="\\",
                )
            )

        if not filters:
            return statement

        return statement.where(*filters)

    @staticmethod
    def _escape_like(value: str) -> str:
        return (
            value
            .replace("\\", "\\\\")
            .replace("%", "\\%")
            .replace("_", "\\_")
        )
