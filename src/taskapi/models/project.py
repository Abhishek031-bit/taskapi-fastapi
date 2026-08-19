from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from taskapi.core.db import Base
from taskapi.models.task import Task

if TYPE_CHECKING:
    from taskapi.models.organizations import Organization


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255))
    organization_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id"))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    organization: Mapped[Organization] = relationship(back_populates="projects")
    tasks: Mapped[list[Task]] = relationship(back_populates="project")
