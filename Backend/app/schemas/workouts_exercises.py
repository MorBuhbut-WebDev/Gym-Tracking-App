from pydantic import BaseModel

from app.schemas.shared import AppBaseModel
from app.schemas.workouts_sets import WorkoutSetNested


class WorkoutExerciseBase(BaseModel):
    exercise_id: int
    exercise_index: int


class WorkoutExerciseNested(WorkoutExerciseBase, AppBaseModel):
    sets: list[WorkoutSetNested]


class WorkoutExerciseResponse(WorkoutExerciseBase, AppBaseModel):
    workout_id: int
