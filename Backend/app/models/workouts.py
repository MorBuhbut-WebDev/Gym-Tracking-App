from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, ForeignKey, func, UniqueConstraint
from sqlalchemy.dialects.postgresql import TIMESTAMP
from datetime import datetime
from typing import Optional

from app.db import Base


class Workout(Base):
    __tablename__ = "workouts"

    workout_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    routine_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("routines.routine_id", ondelete="SET NULL"), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )
    ended_at: Mapped[Optional[datetime]] = mapped_column(
        TIMESTAMP(timezone=True), nullable=True, default=None
    )
    workout_name: Mapped[str] = mapped_column(String(36), nullable=False)

    __table_args__ = (
        UniqueConstraint("routine_id", "workout_name", name="uq_routine_workout_name"),
    )
