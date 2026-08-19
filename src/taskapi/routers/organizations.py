from fastapi import APIRouter, status

from taskapi.core.deps import CurrentUser, DbSession
from taskapi.schemas.organization import OrganizationCreate, OrganizationRead
from taskapi.services import organization as org_service

router = APIRouter(prefix="/organizations", tags=["organizations"])


@router.post("", response_model=OrganizationRead, status_code=status.HTTP_201_CREATED)
async def create_organization(
    data: OrganizationCreate, db: DbSession, current_user: CurrentUser
):
    org = await org_service.create_organization_with_owner(
        db, name=data.name, owner=current_user
    )
    return org


@router.get("", response_model=list[OrganizationRead])
async def list_organizations(db: DbSession, current_user: CurrentUser):
    return await org_service.list_organizations_for_user(db, user_id=current_user.id)
