from datetime import date
import re
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, field_validator, model_validator

from app.exceptions.owner_exceptions import OwnerValidationError
from app.utils.date_validator import DateValidator
from app.utils.enums.driver_license_category import DriverLicenseCategory


_NAME_PATTERN = re.compile(r"^(?=.{1,255}$)[A-Za-z]+(?: [A-Za-z]+)*$")


class OwnerResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    email: str | None


class OwnerCreate(BaseModel):
    name: str
    birthdate: date
    year_of_driver_license: int
    driver_license_cat: DriverLicenseCategory | None = None
    email: EmailStr | None = None

    @field_validator("name")
    @classmethod
    def validate_name(cls, name: str) -> str:
        if not _NAME_PATTERN.fullmatch(name):
            raise OwnerValidationError(
                "Owner name must contain only letters and single spaces "
                "and must be at most 255 characters"
            )

        return name

    @field_validator("email")
    @classmethod
    def normalize_email(cls, email: EmailStr | None) -> str | None:
        if email is None:
            return None

        return str(email).strip().lower()

    @field_validator("driver_license_cat")
    @classmethod
    def normalize_driver_license_category(
        cls,
        category: DriverLicenseCategory | None,
    ) -> DriverLicenseCategory | None:
        if category == DriverLicenseCategory.NONE:
            return None

        return category

    @model_validator(mode="after")
    def validate_dates(self) -> "OwnerCreate":
        current_year = date.today().year

        DateValidator.ensure_date_not_in_future(
            self.birthdate,
            OwnerValidationError("Birthdate cannot be in the future"),
        )
        DateValidator.ensure_date_year_at_least(
            self.birthdate,
            DateValidator.MIN_YEAR,
            OwnerValidationError(
                "Birthdate year must be greater than or equal to 1900"
            ),
        )
        DateValidator.ensure_year_between(
            self.year_of_driver_license,
            DateValidator.MIN_YEAR,
            current_year,
            OwnerValidationError(
                f"Year of driver license must be between 1900 and {current_year}"
            ),
        )
        DateValidator.ensure_not_before_year(
            self.year_of_driver_license,
            self.birthdate.year,
            OwnerValidationError(
                "Year of driver license cannot be before birth year"
            ),
        )

        return self


class OwnerUpdate(BaseModel):
    driver_license_cat: DriverLicenseCategory | None = None
    email: EmailStr | None = None

    @field_validator("email")
    @classmethod
    def normalize_email(cls, email: EmailStr | None) -> str | None:
        if email is None:
            return None

        return str(email).strip().lower()

    @field_validator("driver_license_cat")
    @classmethod
    def normalize_driver_license_category(
        cls,
        category: DriverLicenseCategory | None,
    ) -> DriverLicenseCategory | None:
        if category == DriverLicenseCategory.NONE:
            return None

        return category


class OwnerDetailResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    birthdate: date
    year_of_driver_license: int
    driver_license_cat: DriverLicenseCategory | None
    email: str | None
