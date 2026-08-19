from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from taskapi.models.task import TaskStatus


class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    assignee_id: UUID | None = None
    parent_id: UUID | None = None


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: TaskStatus | None = None
    assignee_id: UUID | None = None


class TaskRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    decription: str | None
    status: TaskStatus
    project_is: UUID
    assignee_id: UUID | None
    parent_id: UUID | None
    created_at: datetime


class CommentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    body: str
    author_id: UUID
    created_at: datetime


class TaskDetailRead(TaskRead):
    subtasks: list[TaskRead] = []
    comments: list[CommentRead] = []
