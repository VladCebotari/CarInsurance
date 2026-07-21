# app/api/routers/cars.py
from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload
from app.api.deps import get_db, get_car_service
from app.db.models import Car
from app.services.car_service import CarService
from app.api.schemas.car_schemas import CarListSchema, CarCreateSchema

cars_router = APIRouter(prefix="/api/cars", tags=["Cars"])


@cars_router.get("", response_model=List[CarListSchema])
def list_cars(db: Session = Depends(get_db)):
    stmt = select(Car).options(joinedload(Car.owner))
    return db.scalars(stmt).all()

@cars_router.get("/{car_id}", response_model=CarListSchema)
def get_car_by_id(
    car_id: UUID,
    car_service: CarService = Depends(get_car_service)
):
    return car_service.get_car_by_id(car_id)


@cars_router.post(
    "",
    response_model=CarListSchema,
    status_code=status.HTTP_201_CREATED
)
def create_car(
    car_data: CarCreateSchema,
    car_service: CarService = Depends(get_car_service)
):
    """Create a new car"""
    return car_service.create_new_car(car_data.model_dump(by_alias=True))


@cars_router.delete(
    "/{car_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_car(
    car_id: UUID,
    car_service: CarService = Depends(get_car_service)
):
    car_service.delete_car(car_id)
    return None