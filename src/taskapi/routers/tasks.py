from uuid import UUID

from fastapi import APIRouter

from taskapi.core.deps import DbSession
from taskapi.models import TaskStatus
from taskapi.schemas.task import TaskCreate, TaskDetailRead, TaskRead, TaskUpdate
from taskapi.services import task as task_service

router = APIRouter(
    prefix="/organizations/{organization_id}/projects/{project_id}/tasks",
    tags=["tasks"],
)


@router.post("", response_model=TaskRead, status_code=201)
async def create_task(
    organization_id: UUID,
    project_id: UUID,
    data: TaskCreate,
    db: DbSession,
):
    return await task_service.create_task(
        db,
        project_id=project_id,
        title=data.title,
        description=data.description,
        assignee_id=data.assignee_id,
        parent_id=data.parent_id,
    )


@router.get("", response_model=list[TaskRead])
async def list_tasks(
    organization_id: UUID,
    project_id: UUID,
    db: DbSession,
    status_filter: TaskStatus | None = None,
    assignee_id: UUID | None = None,
):
    return await task_service.list_tasks(
        db, project_id=project_id, status_filter=status_filter, assignee_id=assignee_id
    )


@router.get("/{task_id}", response_model=TaskDetailRead)
async def get_task_detail(
    organization_id: UUID,
    project_id: UUID,
    task_id: UUID,
    db: DbSession,
    strategy: str = "selectinload",
):
    return await task_service.get_task_detail(db, task_id, strategy=strategy)


@router.patch("/{task_id}", response_model=TaskRead)
async def update_task(
    organization_id: UUID,
    project_id: UUID,
    task_id: UUID,
    data: TaskUpdate,
    db: DbSession,
):
    return await task_service.update_task(
        db,
        task_id,
        title=data.title,
        description=data.description,
        status_value=data.status,
        assignee_id=data.assignee_id,
    )
