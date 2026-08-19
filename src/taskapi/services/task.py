from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from taskapi.models import Task, TaskStatus
from taskapi.repositories import project as project_repo
from taskapi.repositories import task as task_repo


async def _verify_project_in_org(
    db: AsyncSession, project_id: UUID, organization_id: UUID
) -> None:
    project = await project_repo.get_project(db, project_id)
    if project is None or project.organization_id != organization_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found in this organization",
        )


async def create_task(
    db: AsyncSession,
    *,
    organization_id: UUID,
    project_id: UUID,
    title: str,
    description: str | None = None,
    assignee_id: UUID | None = None,
    parent_id: UUID | None = None,
) -> Task:
    await _verify_project_in_org(db, project_id, organization_id)
    task = await task_repo.create_task(
        db,
        title=title,
        project_id=project_id,
        description=description,
        assignee_id=assignee_id,
        parent_id=parent_id,
    )
    await db.commit()
    return task


async def list_tasks(
    db: AsyncSession,
    *,
    project_id: UUID,
    status_filter: TaskStatus | None = None,
    assignee_id: UUID | None = None,
) -> list[Task]:
    return await task_repo.list_tasks(
        db, project_id=project_id, status=status_filter, assignee_id=assignee_id
    )


async def get_task_detail(
    db: AsyncSession, task_id: UUID, strategy: str = "selectinload"
) -> Task:
    if strategy == "joinedload":
        task = await task_repo.get_task_detail_joinedload(db, task_id)
    else:
        task = await task_repo.get_task_detail_selectinload(db, task_id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    return task


async def update_task(
    db: AsyncSession,
    task_id: UUID,
    *,
    title: str | None = None,
    description: str | None = None,
    status_value: TaskStatus | None = None,
    assignee_id: UUID | None = None,
) -> Task:
    task = await task_repo.get_task(db, task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )

    updated = await task_repo.update_task(
        db,
        task,
        title=title,
        description=description,
        status=status_value,
        assignee_id=assignee_id,
    )
    await db.commit()
    return updated
