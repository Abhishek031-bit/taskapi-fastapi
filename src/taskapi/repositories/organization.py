from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from taskapi.models import Membership, MembershipRole, Organization


async def create_organization(db: AsyncSession, *, name: str) -> Organization:
    org = Organization(name=name)
    db.add(org)
    await db.flush()
    await db.refresh(org)
    return org


async def create_membership(
    db: AsyncSession, *, user_id: UUID, organization_id: UUID, role: MembershipRole
) -> Membership:
    membership = Membership(user_id=user_id, organization_id=organization_id, role=role)
    db.add(membership)
    await db.flush()
    await db.refresh(membership)
    return membership


async def list_user_organizations(
    db: AsyncSession, user_id: UUID
) -> list[Organization]:
    result = await db.execute(
        select(Organization)
        .join(Membership, Membership.organization_id == Organization.id)
        .where(Membership.user_id == user_id)
    )
    return list(result.scalars().all())
