from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.repositories.owner_repository.sqlalchemy_owner_repository import SqlAlchemyOwnerRepository
from app.services.car_service import CarService
from app.services.owner_service import OwnerService
from app.repositories.car_repository.sqlalchemy_car_repository import SqlAlchemyCarRepository

def get_car_service(
    db: Session = Depends(get_db),
) -> CarService:
    car_repository = SqlAlchemyCarRepository(db)
    return CarService(car_repository)

def get_owner_service(
        db: Session = Depends(get_db),
) -> OwnerService:
    owner_repository = SqlAlchemyOwnerRepository(db)

    return OwnerService(owner_repository)
