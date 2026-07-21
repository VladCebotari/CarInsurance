# app/services/car_service.py
from typing import List
from uuid import UUID
from fastapi import HTTPException, status
from app.db.models import Car
from app.utils.enums.car_category import CarCategory
from app.repositories.car_repository.base import CarRepository


class CarService:
    def __init__(self, car_repository: CarRepository):
        self.car_repository = car_repository

    def get_categories(self) -> List[str]:
        return [category.value for category in CarCategory]

    def create_new_car(self, car_data: dict) -> Car:
        existing_car = self.car_repository.get_by_vin(car_data.get("vin"))
        if existing_car:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Car with this VIN already exists."
            )

        new_car = Car(**car_data)
        return self.car_repository.create_car(new_car)

    def delete_car(self, car_id: UUID) -> None:
        car = self.car_repository.get_car_by_id(car_id)
        if not car:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Car not found"
            )
        self.car_repository.delete_car(car)

    def get_car_by_id(self, car_id: UUID) -> Car:
        car = self.car_repository.get_car_by_id(car_id)
        if not car:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Car not found"
            )
        return car