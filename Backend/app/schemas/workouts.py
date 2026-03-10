from pydantic import BaseModel, PositiveInt
from typing import Optional
from datetime import datetime

from app.schemas.workouts_exercises import WorkoutExerciseNested


class WorkoutCreate(BaseModel):
    routine_id: PositiveInt


class WorkoutBase(BaseModel):
    workout_id: int
    routine_id: Optional[int]
    created_at: datetime
    ended_at: Optional[datetime]
    workout_name: str


class WorkoutResponse(WorkoutBase):
    model_config = {"from_attributes": True}


class WorkoutNested(WorkoutBase):
    exercises: list[WorkoutExerciseNested]

    model_config = {"from_attributes": True}
