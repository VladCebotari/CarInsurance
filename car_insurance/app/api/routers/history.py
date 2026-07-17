import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, text
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.db.models import Car
from app.api.schemas.car_schemas import HistoryItem, HistoryPolicyItem, HistoryClaimItem

history_router = APIRouter(prefix="/api/cars", tags=["History"])


@history_router.get("/{carId}/history", response_model=List[HistoryItem])
def retrieve_car_history(carId: uuid.UUID, db: Session = Depends(get_db)):
    car = db.scalar(select(Car).where(Car.id == carId))
    if not car:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Car not found")

    history_list = []

    policies_query = text("""
                          SELECT id, start_date, end_date, provider, paid_amount, status
                          FROM insurance_policies
                          WHERE car_id = :car_id
                          """)
    policies = db.execute(policies_query, {"car_id": carId}).all()

    for policy in policies:
        history_list.append({
            "sort_date": policy.start_date,
            "data": HistoryPolicyItem(
                type="POLICY",
                policyId=policy.id,
                startDate=policy.start_date,
                endDate=policy.end_date,
                provider=policy.provider,
                paid_amount=float(policy.paid_amount),
                status=policy.status
            )
        })

    claims_query = text("""
                        SELECT id, claim_date, amount, description
                        FROM claims
                        WHERE car_id = :car_id
                        """)
    claims = db.execute(claims_query, {"car_id": carId}).all()

    for claim in claims:
        history_list.append({
            "sort_date": claim.claim_date,
            "data": HistoryClaimItem(
                type="CLAIM",
                claimId=claim.id,
                claimDate=claim.claim_date,
                amount=float(claim.amount),
                description=claim.description
            )
        })

    history_list.sort(key=lambda item: item["sort_date"])

    return [item["data"] for item in history_list]