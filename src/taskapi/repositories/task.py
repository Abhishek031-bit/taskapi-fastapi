from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from taskapi.models import Task, TaskStatus


async def create_task(
    db: AsyncSession,
    *,
    title: str,
    project_id: UUID,
    description: str | None = None,
    assignee_id: UUID | None = None,
    parent_id: UUID | None = None,
) -> Task:
    task = Task(
        title=title,
        project_id=project_id,
        description=description,
        assignee_id=assignee_id,
        parent_id=parent_id,
    )
    db.add(task)
    await db.flush()
    await db.refresh(task)
    return task


async def list_tasks(
    db: AsyncSession,
    *,
    project_id: UUID,
    status: TaskStatus | None = None,
    assignee_id: UUID | None = None,
) -> list[Task]:
    query = select(Task).where(Task.project_id == project_id)

    if status is not None:
        query = query.where(Task.status == status)
    if assignee_id is not None:
        query = query.where(Task.assignee_id == assignee_id)

    result = await db.execute(query)
    return list(result.scalars().all())


async def get_task_detail_selectinload(db: AsyncSession, task_id: UUID) -> Task | None:
    query = (
        select(Task)
        .where(Task.id == task_id)
        .options(selectinload(Task.subtasks), selectinload(Task.comments))
    )
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def get_task_detail_joinedload(db: AsyncSession, task_id: UUID) -> Task | None:
    query = (
        select(Task)
        .where(Task.id == task_id)
        .options(joinedload(Task.subtasks), joinedload(Task.comments))
    )
    result = await db.execute(query)
    return result.unique().scalar_one_or_none()


async def get_task(db: AsyncSession, task_id: UUID) -> Task | None:
    result = await db.execute(select(Task).where(Task.id == task_id))
    return result.scalar_one_or_none()


async def update_task(db: AsyncSession, task: Task, **fields) -> Task:
    for key, value in fields.items():
        if value is not None:
            setattr(task, key, value)
    await db.flush()
    await db.refresh(task)
    return task
