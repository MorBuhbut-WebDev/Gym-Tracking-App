import uuid
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, ForeignKey, func
from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID
from datetime import datetime, timezone
from typing import Optional

from app.db import Base


class Workout(Base):
    __tablename__ = "workouts"

    workout_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    routine_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("routines.routine_id", ondelete="SET NULL")
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.user_id", ondelete="CASCADE", use_alter=True),
    )
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=lambda: datetime.now(tz=timezone.utc),
        server_default=func.now(),
    )
    ended_at: Mapped[Optional[datetime]] = mapped_column(
        TIMESTAMP(timezone=True), default=None
    )
    workout_name: Mapped[str] = mapped_column(String(36))

    @classmethod
    def create(
        cls, *, routine_id: int, user_id: uuid.UUID, workout_name: str
    ) -> "Workout":
        return cls(routine_id=routine_id, user_id=user_id, workout_name=workout_name)
