import re
from datetime import date
from typing import Literal, Union, Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
from app.api.schemas.owner_schemas import OwnerResponse

_PROVIDER_PATTERN = re.compile(r"^[A-Za-z0-9]+( [A-Za-z0-9]+)*$")
_DESCRIPTION_PATTERN = re.compile(r"^(?!\s*$).+")

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
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    car_id: UUID
    provider: str
    start_date: date
    end_date: date
    paid_amount: float
    status: str

class ValidityResponseSchema(BaseModel):
    carId: UUID
    date: date
    valid: bool

class ClaimCreateSchema(BaseModel):
    claimDate: date = Field(..., alias="claimDate")
    description: str
    amount: float

    @field_validator("claimDate")
    @classmethod
    def validate_claim_date(cls, v: date) -> date:
        if not (date(1900, 1, 1) <= v <= date.today()):
            raise ValueError("claimDate must be between 1900-01-01 and today")
        return v

    @field_validator("description")
    @classmethod
    def validate_description(cls, v: str) -> str:
        if not (1 <= len(v) <= 2000) or not _DESCRIPTION_PATTERN.match(v):
            raise ValueError("description is required, cannot be empty, and must be at most 2000 characters")
        return v

    @field_validator("amount")
    @classmethod
    def validate_amount(cls, v: float) -> float:
        if not (0 < v <= 1000000):
            raise ValueError("amount must be greater than 0 and less than or equal to 1,000,000")
        return v


class CarCreateSchema(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    vin: str = Field(..., max_length=16, pattern=r"^[A-Za-z0-9]+$")
    make: Optional[str] = Field(None, max_length=150, pattern=r"^[A-Za-z0-9]+( [A-Za-z0-9]+)*$")
    model: Optional[str] = Field(None, max_length=150, pattern=r"^[A-Za-z0-9]+( [A-Za-z0-9]+)*$")
    yearOfManufacture: int = Field(..., alias="year_of_manufacture", ge=1900)
    cc: int = Field(..., ge=1, le=10000)
    power: int = Field(..., ge=1, le=500)
    category: Optional[str] = None
    ownerId: UUID = Field(..., alias="owner_id")


class ClaimResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: UUID
    carId: UUID = Field(..., alias="car_id")
    claimDate: date = Field(..., alias="claim_date")
    description: str
    amount: float

class HistoryPolicyItem(BaseModel):
    type: Literal["POLICY"] = "POLICY"
    policyId: UUID
    startDate: date
    endDate: date
    provider: str
    paid_amount: float
    status: str

class HistoryClaimItem(BaseModel):
    type: Literal["CLAIM"] = "CLAIM"
    claimId: UUID
    claimDate: date
    amount: float
    description: str

HistoryItem = Union[HistoryPolicyItem, HistoryClaimItem]