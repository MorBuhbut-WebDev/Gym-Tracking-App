from sqlalchemy import ForeignKey, Integer, PrimaryKeyConstraint, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import OrderedExerciseModel


class WorkoutExercise(OrderedExerciseModel):
    __tablename__ = "workouts_exercises"
    EXERCISE_INDEX_CONSTRAINT = "uq_workout_exercise_order"
    PARENT_ID = "workout_id"

    workout_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("workouts.workout_id", ondelete="CASCADE")
    )
    exercise_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("exercises.exercise_id", ondelete="CASCADE")
    )

    __table_args__ = (
        UniqueConstraint(
            "workout_id",
            "exercise_index",
            name=EXERCISE_INDEX_CONSTRAINT,
            deferrable=True,
            initially="IMMEDIATE",
        ),
        PrimaryKeyConstraint("workout_id", "exercise_id"),
    )
