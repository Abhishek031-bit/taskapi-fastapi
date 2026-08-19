from uuid import UUID

from fastapi import APIRouter, Depends, status

from taskapi.core.deps import DbSession, require_role
from taskapi.models import MembershipRole
from taskapi.schemas.project import ProjectCreate, ProjectRead
from taskapi.services import project as project_service

router = APIRouter(
    prefix="/organizations/{organization_id}/projects", tags=["projects"]
)


@router.post("", response_model=ProjectRead, status_code=status.HTTP_201_CREATED)
async def create_project(
    organization_id: UUID,
    data: ProjectCreate,
    db: DbSession,
    _=Depends(require_role(MembershipRole.OWNER, MembershipRole.ADMIN)),
):
    return await project_service.create_project(
        db, name=data.name, organization_id=organization_id
    )


@router.get("", response_model=list[ProjectRead])
async def list_projects(
    organization_id: UUID,
    db: DbSession,
    _=Depends(
        require_role(MembershipRole.OWNER, MembershipRole.ADMIN, MembershipRole.MEMBER)
    ),
):
    return await project_service.list_projects(db, organization_id=organization_id)
