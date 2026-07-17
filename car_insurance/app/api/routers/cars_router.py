from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.db.models import Car
from app.api.schemas.car_schemas import CarListSchema

cars_router = APIRouter(prefix="/api/cars", tags=["Cars"])

@cars_router.get("", response_model=List[CarListSchema])
def list_cars(db: Session = Depends(get_db)):
    return db.scalars(select(Car)).all()