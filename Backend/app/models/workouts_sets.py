from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Float, ForeignKey, UniqueConstraint
from typing import Optional

from app.db import Base


class WorkoutSet(Base):
    __tablename__ = "workouts_sets"

    set_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    workout_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("workouts.workout_id", ondelete="CASCADE"), nullable=False
    )
    exercise_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("exercises.exercise_id"),
        nullable=False,
    )
    set_index: Mapped[int] = mapped_column(Integer, nullable=False)
    weight: Mapped[Optional[float]] = mapped_column(
        Float(precision=3), nullable=True, default=None
    )
    reps: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, default=None)
    notes: Mapped[Optional[str]] = mapped_column(
        String(128), nullable=True, default=None
    )

    __table_args__ = (
        UniqueConstraint(
            "workout_id",
            "exercise_id",
            "set_index",
            name="uq_set_per_exercise_per_workout",
        ),
    )
