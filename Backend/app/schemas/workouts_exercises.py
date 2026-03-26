from pydantic import BaseModel

from app.schemas.shared import AppBaseModel
from app.schemas.workouts_sets import WorkoutSetResponse


class WorkoutExerciseBase(BaseModel):
    exercise_index: int


class WorkoutExerciseNested(WorkoutExerciseBase, AppBaseModel):
    exercise_id: int
    exercise_name: str
    sets: list[WorkoutSetResponse]


class WorkoutExerciseResponse(WorkoutExerciseBase, AppBaseModel):
    pass
