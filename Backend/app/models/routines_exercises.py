from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, ForeignKey, String, UniqueConstraint
from typing import Optional

from app.db import Base


class RoutineExercise(Base):
    __tablename__ = "routines_exercises"
    EXERCISE_INDEX_CONSTRAINT = "uq_routine_exercise_order"
    PARENT_ID = "routine_id"

    exercise_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("exercises.exercise_id"),
        primary_key=True,
    )
    routine_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("routines.routine_id", ondelete="CASCADE"), primary_key=True
    )
    exercise_index: Mapped[int] = mapped_column(Integer, nullable=False)
    planned_sets: Mapped[int] = mapped_column(Integer, nullable=False)
    exercise_notes: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)

    __table_args__ = (
        UniqueConstraint(
            "routine_id",
            "exercise_index",
            name=EXERCISE_INDEX_CONSTRAINT,
            deferrable=True,
            initially="IMMEDIATE",
        ),
    )

    @classmethod
    def create(
        cls,
        *,
        exercise_id: int,
        routine_id: int,
        exercise_index: int,
        planned_sets: int,
        exercise_notes: Optional[str]
    ) -> "RoutineExercise":
        return cls(
            exercise_id=exercise_id,
            routine_id=routine_id,
            exercise_index=exercise_index,
            planned_sets=planned_sets,
            exercise_notes=exercise_notes,
        )
