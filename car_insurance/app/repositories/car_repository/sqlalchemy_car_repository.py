# app/repositories/car_repository/sqlalchemy_car_repository.py
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload
from app.db.models import Car
from app.repositories.car_repository.base import CarRepository


class SqlAlchemyCarRepository(CarRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_by_vin(self, vin: str) -> Car | None:
        return self.db.scalars(select(Car).where(Car.vin == vin)).first()

    def create_car(self, car_model: Car) -> Car:
        self.db.add(car_model)
        self.db.commit()

        stmt = (
            select(Car)
            .where(Car.id == car_model.id)
            .options(joinedload(Car.owner))
        )
        return self.db.scalars(stmt).first()

    def get_car_by_id(self, car_id: UUID) -> Car | None:
        stmt = select(Car).where(Car.id == car_id).options(joinedload(Car.owner))
        return self.db.scalars(stmt).first()

    def delete_car(self, car: Car) -> None:
        self.db.delete(car)
        self.db.commit()

    def get_cars(self, page: int, per_page: int, **kwargs):
        raise NotImplementedError