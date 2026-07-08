from fastapi import APIRouter, Depends

from app.api.deps import get_car_service
from app.services.car_service import CarService

cars_router = APIRouter(prefix="/api/cars", tags=["Cars"])


@cars_router.get(
    "/cars-categories",
    response_model=list[str],
    summary="Get car categories",
    description="Returns the available car categories.",
)
def get_car_categories(car_service: CarService = Depends(get_car_service),
                       ) -> list[str]:
    return car_service.get_categories()
