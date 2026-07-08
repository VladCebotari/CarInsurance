from uuid import UUID

from fastapi import APIRouter, Depends, Query, status

from app.api.deps import get_owner_service
from app.api.responses import error_responses
from app.api.schemas.owner_schemas import (
    OwnerCreate,
    OwnerResponse,
    OwnerUpdate, OwnerDetailResponse,
)
from app.api.schemas.pagination_schemas import PaginatedResponse
from app.services.owner_service import OwnerService
from app.utils.enums.driver_license_category import DriverLicenseCategory

owners_router = APIRouter(
    prefix="/api/owners",
    tags=["Owners"],
)


@owners_router.get(
    "",
    response_model=PaginatedResponse[OwnerDetailResponse],
    summary="Get owners",
    description=(
            "Retrieves owners. Can filter by driver license category using "
            "A, B, C, D, E, or none, and by email."
    ),
    responses=error_responses(400, 500),
)
def get_owners(
        page: int = Query(default=1, ge=1),
        per_page: int = Query(default=50, ge=1, le=100),
        category: list[DriverLicenseCategory] | None = Query(default=None),
        email: str | None = Query(default=None, max_length=255),
        owner_service: OwnerService = Depends(get_owner_service),
) -> PaginatedResponse[OwnerDetailResponse]:
    return owner_service.get_owners(
        page=page,
        per_page=per_page,
        category=category,
        email=email,
    )


@owners_router.post(
    "",
    response_model=OwnerDetailResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create owner",
    description=(
            "Creates a new vehicle owner. Validates the provided owner "
            "information and persists the record. The newly created owner "
            "is returned as a DTO for subsequent operations such as vehicle "
            "registration and policy management."
    ),
    responses=error_responses(400, 409, 500),
)
def create_owner(
        owner_data: OwnerCreate,
        owner_service: OwnerService = Depends(get_owner_service),
):
    """
    Create a new owner.

    Args:
        owner_data (OwnerCreate): Validated owner creation payload.
        owner_service (OwnerService): Service responsible for validation
            and persistence.

    Returns:
        OwnerResponse: DTO representing the created owner.
    """
    return owner_service.create_owner(owner_data)


@owners_router.get(
    "/{owner_id}",
    response_model=OwnerResponse,
    summary="Get owner",
    description=(
            "Retrieves an owner by identifier. Returns the owner details "
            "required for vehicle ownership, insurance, and claims-related "
            "operations."
    ),
    responses=error_responses(404, 500),
)
def get_owner(
        owner_id: UUID,
        owner_service: OwnerService = Depends(get_owner_service),
):
    """
    Retrieve an owner by identifier.

    Args:
        owner_id (UUID): Unique owner identifier.
        owner_service (OwnerService): Service responsible for owner retrieval.

    Returns:
        OwnerResponse: DTO containing owner details.
    """
    return owner_service.get_owner_by_id(owner_id)


@owners_router.patch(
    "/{owner_id}",
    response_model=OwnerResponse,
    summary="Update owner",
    description=(
            "Partially updates an existing owner. Only the fields provided "
            "in the request payload are modified. The updated owner record "
            "is returned after validation and persistence."
    ),
    responses=error_responses(400, 404, 409, 500),
)
def patch_owner(
        owner_id: UUID,
        owner_data: OwnerUpdate,
        owner_service: OwnerService = Depends(get_owner_service),
):
    """
    Partially update an owner.

    Args:
        owner_id (UUID): Unique owner identifier.
        owner_data (OwnerUpdate): Payload containing fields to update.
        owner_service (OwnerService): Service responsible for validation
            and persistence.

    Returns:
        OwnerResponse: DTO representing the updated owner.
    """
    return owner_service.patch_owner(owner_id, owner_data)


@owners_router.delete(
    "/{owner_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete owner",
    description=(
            "Deletes an owner by ID. "
            "All cars belonging to the owner are deleted as well, "
            "including their insurance policies and claims."
    ),
    responses=error_responses(404, 500),
)
def delete_owner(
        owner_id: UUID,
        owner_service: OwnerService = Depends(get_owner_service),
) -> None:
    owner_service.delete_owner(owner_id)
