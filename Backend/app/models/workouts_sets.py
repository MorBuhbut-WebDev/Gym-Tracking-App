from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Numeric, UniqueConstraint, ForeignKeyConstraint
from typing import Optional
from decimal import Decimal

from app.db import Base


class WorkoutSet(Base):
    __tablename__ = "workouts_sets"

    set_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    workout_id: Mapped[int] = mapped_column(Integer)
    exercise_id: Mapped[int] = mapped_column(Integer)
    set_index: Mapped[int] = mapped_column(Integer)
    weight: Mapped[Optional[Decimal]] = mapped_column(
        Numeric(precision=6, scale=3), default=None
    )
    reps: Mapped[Optional[int]] = mapped_column(Integer, default=None)
    notes: Mapped[Optional[str]] = mapped_column(String(128), default=None)

    __table_args__ = (
        ForeignKeyConstraint(
            ["workout_id", "exercise_id"],
            ["workouts_exercises.workout_id", "workouts_exercises.exercise_id"],
            ondelete="CASCADE",
        ),
        UniqueConstraint(
            "workout_id",
            "exercise_id",
            "set_index",
            name="uq_set_per_exercise_per_workout",
        ),
    )
