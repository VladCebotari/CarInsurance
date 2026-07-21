from datetime import date
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field


class PolicyResponseSchema(BaseModel):
    id: UUID
    car_id: UUID = Field(..., alias="carId")
    provider: str | None = None
    start_date: date = Field(..., alias="startDate")
    end_date: date = Field(..., alias="endDate")
    paid_amount: float
    status: str

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)