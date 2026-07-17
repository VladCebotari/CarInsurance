import uuid
from datetime import date
from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from app.api.deps import get_db
from app.db.models import Car
from app.api.schemas.car_schemas import PolicyCreateSchema, PolicyResponseSchema

policies_router = APIRouter(prefix="/api/cars", tags=["Policies"])

@policies_router.post("/{carId}/policies", response_model=PolicyResponseSchema, status_code=status.HTTP_201_CREATED)
def create_insurance_policy(carId: uuid.UUID, payload: PolicyCreateSchema, db: Session = Depends(get_db)):
    car = db.scalar(select(Car).where(Car.id == carId))
    if not car:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Car not found")

    return {
        "id": uuid.uuid4(),
        "car_id": carId,
        "provider": payload.provider,
        "start_date": payload.startDate,
        "end_date": payload.endDate,
        "paid_amount": payload.paid_amount,
        "status": "ACTIVE"
    }