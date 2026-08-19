from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from taskapi.models import Project


async def create_project(
    db: AsyncSession, *, name: str, organization_id: UUID
) -> Project:
    project = Project(name=name, organization_id=organization_id)
    db.add(project)
    await db.flush()
    await db.refresh(project)
    return project


async def list_projects(db: AsyncSession, organization_id: UUID) -> list[Project]:
    result = await db.execute(
        select(Project).where(Project.organization_id == organization_id)
    )
    return list(result.scalars().all())


async def get_project(db: AsyncSession, project_id: UUID) -> Project | None:
    result = await db.execute(select(Project).where(Project.id == project_id))
    return result.scalar_one_or_none()
