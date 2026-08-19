from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from taskapi.repositories import project as project_repo


async def create_project(db: AsyncSession, *, name: str, organization_id: UUID):
    project = await project_repo.create_project(
        db, name=name, organization_id=organization_id
    )
    await db.commit()
    return project


async def list_projects(db: AsyncSession, organization_id: UUID):
    return await project_repo.list_projects(db, organization_id=organization_id)
