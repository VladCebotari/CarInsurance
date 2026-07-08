from fastapi import APIRouter

from app.utils.enums.driver_license_category import DriverLicenseCategory

licenses_router = APIRouter(
    prefix="/api/licenses",
    tags=["Licenses"],
)


@licenses_router.get(
    "",
    response_model=list[str],
    summary="Get driver license categories",
)
def get_driver_license_categories() -> list[str]:
    return [category.value for category in DriverLicenseCategory]
