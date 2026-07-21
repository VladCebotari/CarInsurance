import uuid
from datetime import date
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import MetaData, Table, inspect, select
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.db.models import Car
from app.api.schemas.car_schemas import PolicyCreateSchema, PolicyResponseSchema

policies_router = APIRouter(prefix="/api", tags=["Policies"])

def get_policies_table(db: Session) -> Table:
    bind = db.get_bind()
    inspector = inspect(bind)
    tables = inspector.get_table_names()

    table_name = "policies" if "policies" in tables else "insurance_policies"
    return Table(table_name, MetaData(), autoload_with=bind)


@policies_router.get("/policies", response_model=List[PolicyResponseSchema])
def list_policies(
    car_id: Optional[uuid.UUID] = Query(None, description="Filter policies by car ID"),
    db: Session = Depends(get_db),
):

    policies_table = get_policies_table(db)
    stmt = select(policies_table)

    if car_id:
        stmt = stmt.where(policies_table.c.car_id == car_id)

    rows = db.execute(stmt).mappings().all()
    return rows


@policies_router.get("/policies/active-policy", response_model=PolicyResponseSchema)
def get_active_policy(
    car_id: uuid.UUID = Query(..., description="ID of the car"),
    today: Optional[date] = Query(default_factory=date.today),
    db: Session = Depends(get_db),
):
    car = db.scalar(select(Car).where(Car.id == car_id))
    if not car:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Car not found"
        )

    policies_table = get_policies_table(db)
    stmt = select(policies_table).where(
        policies_table.c.car_id == car_id,
        policies_table.c.start_date <= today,
        policies_table.c.end_date >= today,
    )

    active_policy = db.execute(stmt).mappings().first()

    if not active_policy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active insurance policy found for this car",
        )

    return active_policy


@policies_router.post(
    "/cars/{carId}/policies",
    response_model=PolicyResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
def create_insurance_policy(
    carId: uuid.UUID,
    payload: PolicyCreateSchema,
    db: Session = Depends(get_db),
):
    car = db.scalar(select(Car).where(Car.id == carId))
    if not car:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Car not found"
        )

    if payload.endDate < payload.startDate:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="endDate must be greater than or equal to startDate",
        )

    policies_table = get_policies_table(db)

    new_policy = {
        "id": uuid.uuid4(),
        "car_id": carId,
        "provider": payload.provider,
        "start_date": payload.startDate,
        "end_date": payload.endDate,
        "paid_amount": payload.paid_amount,
        "status": "ACTIVE",
    }

    stmt = policies_table.insert().values(**new_policy)
    db.execute(stmt)
    db.commit()

    return new_policy