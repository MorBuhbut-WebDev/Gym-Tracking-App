from datetime import datetime

from pydantic import BaseModel, PositiveInt

from app.schemas.shared import AppBaseModel
from app.schemas.workouts_exercises import WorkoutExerciseNested


class WorkoutCreate(BaseModel):
    routine_id: PositiveInt


class WorkoutBase(BaseModel):
    workout_id: int
    routine_id: int | None
    created_at: datetime
    ended_at: datetime | None
    workout_name: str


class WorkoutResponse(WorkoutBase, AppBaseModel):
    pass


class WorkoutNested(WorkoutBase, AppBaseModel):
    exercises: list[WorkoutExerciseNested]
