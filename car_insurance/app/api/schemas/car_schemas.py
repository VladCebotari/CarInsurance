import re
from datetime import date
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
from app.api.schemas.owner_schemas import OwnerResponse

_PROVIDER_PATTERN = re.compile(r"^[A-Za-z0-9]+( [A-Za-z0-9]+)*$")

class CarListSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: UUID
    vin: str
    make: Optional[str]
    model: Optional[str]
    yearOfManufacture: int = Field(..., alias="year_of_manufacture")
    power: int
    cc: int
    category: Optional[str]
    owner: OwnerResponse

class PolicyCreateSchema(BaseModel):
    provider: str
    startDate: date = Field(..., alias="startDate")
    endDate: date = Field(..., alias="endDate")
    paid_amount: float

    @field_validator("provider")
    @classmethod
    def validate_provider(cls, v: str) -> str:
        if not (1 <= len(v) <= 100):
            raise ValueError("provider length must be between 1 and 100")
        if not _PROVIDER_PATTERN.fullmatch(v):
            raise ValueError("Provider must contain only letters and numbers and separated only by one space")
        return v

    @field_validator("startDate", "endDate")
    @classmethod
    def validate_years(cls, v: date) -> date:
        if not (1900 <= v.year <= 2100):
            raise ValueError("Year must be between 1900 and 2100")
        return v

    @field_validator("paid_amount")
    @classmethod
    def validate_amount(cls, v: float) -> float:
        if not (0 < v <= 1000000):
            raise ValueError("paidAmount must be between 0 and 1,000,000")
        return v

    @model_validator(mode="after")
    def validate_chronology(self) -> "PolicyCreateSchema":
        if self.endDate < self.startDate:
            raise ValueError("endDate must be greater than or equal to startDate")
        return self

class PolicyResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: UUID
    carId: UUID = Field(..., alias="car_id")
    provider: str
    startDate: date = Field(..., alias="start_date")
    endDate: date = Field(..., alias="end_date")
    paid_amount: float
    status: str = "ACTIVE"