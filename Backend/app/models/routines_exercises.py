from sqlalchemy import (
    ForeignKey,
    Integer,
    PrimaryKeyConstraint,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import OrderedExerciseModel


class RoutineExercise(OrderedExerciseModel):
    __tablename__ = "routines_exercises"
    EXERCISE_INDEX_CONSTRAINT = "uq_routine_exercise_order"
    PARENT_ID = "routine_id"

    exercise_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("exercises.exercise_id", ondelete="CASCADE")
    )
    routine_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("routines.routine_id", ondelete="CASCADE")
    )
    exercise_index: Mapped[int] = mapped_column(Integer)
    planned_sets: Mapped[int] = mapped_column(Integer)
    exercise_notes: Mapped[str | None] = mapped_column(String(128), default=None)

    __table_args__ = (
        UniqueConstraint(
            "routine_id",
            "exercise_index",
            name=EXERCISE_INDEX_CONSTRAINT,
            deferrable=True,
            initially="IMMEDIATE",
        ),
        PrimaryKeyConstraint("exercise_id", "routine_id"),
    )

    @classmethod
    def create(
        cls,
        *,
        exercise_id: int,
        routine_id: int,
        exercise_index: int,
        planned_sets: int,
        exercise_notes: str | None,
    ) -> "RoutineExercise":
        return cls(
            exercise_id=exercise_id,
            routine_id=routine_id,
            exercise_index=exercise_index,
            planned_sets=planned_sets,
            exercise_notes=exercise_notes,
        )
