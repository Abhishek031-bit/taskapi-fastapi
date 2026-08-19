from __future__ import annotations

import uuid
from datetime import datetime
from enum import StrEnum
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from taskapi.core.db import Base

if TYPE_CHECKING:
    from taskapi.models.comment import Comment
    from taskapi.models.project import Project
    from taskapi.models.user import User


class TaskStatus(StrEnum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(String(2000))
    status: Mapped[TaskStatus] = mapped_column(default=TaskStatus.TODO)

    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id"))
    assignee_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    parent_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("tasks.id"))

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    project: Mapped[Project] = relationship(back_populates="tasks")
    assignee: Mapped[User | None] = relationship(foreign_keys=[assignee_id])

    parent: Mapped[Task | None] = relationship(
        back_populates="subtasks", remote_side=[id]
    )
    subtasks: Mapped[list[Task]] = relationship(back_populates="parent")
    comments: Mapped[list[Comment]] = relationship(back_populates="task")
