from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from taskapi.models.task import Task
    from taskapi.models.user import User

from taskapi.core.db import Base


class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    body: Mapped[str] = mapped_column(String(2000))

    task_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tasks.id"))
    author_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    task: Mapped[Task] = relationship(back_populates="comments")
    author: Mapped[User] = relationship()
