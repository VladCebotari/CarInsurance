import uuid
from datetime import date as dt_date
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.db.models import Car
from app.api.schemas.car_schemas import ValidityResponseSchema, ClaimCreateSchema, ClaimResponseSchema

claims_router = APIRouter(prefix="/api/cars", tags=["Claims & Validity"])

@claims_router.get("/{carId}/insurance-valid", response_model=ValidityResponseSchema)
def check_insurance_validity(carId: uuid.UUID, target_date: dt_date = Query(..., alias="date"), db: Session = Depends(get_db)):
    if not (1900 <= target_date.year <= 2100):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Date must be between 1900 and 2100")

    car = db.scalar(select(Car).where(Car.id == carId))
    if not car:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Car not found")

    return {
        "carId": carId,
        "date": target_date,
        "valid": False
    }

@claims_router.post("/{carId}/claims", response_model=ClaimResponseSchema, status_code=status.HTTP_201_CREATED)
def register_claim(carId: uuid.UUID, payload: ClaimCreateSchema, db: Session = Depends(get_db)):
    car = db.scalar(select(Car).where(Car.id == carId))
    if not car:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Car not found")

    return {
        "id": uuid.uuid4(),
        "car_id": carId,
        "claim_date": payload.claimDate,
        "description": payload.description,
        "amount": payload.amount
    }