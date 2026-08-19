from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from taskapi.models import MembershipRole, Organization, User
from taskapi.repositories import organization as org_repo


async def create_organization_with_owner(
    db: AsyncSession, *, name: str, owner: User
) -> Organization:
    org = await org_repo.create_organization(db, name=name)
    await org_repo.create_membership(
        db, user_id=owner.id, organization_id=org.id, role=MembershipRole.OWNER
    )
    await db.commit()
    await db.refresh(org)
    return org


async def list_organizations_for_user(
    db: AsyncSession, user_id: UUID
) -> list[Organization]:
    return await org_repo.list_user_organizations(db, user_id=user_id)
