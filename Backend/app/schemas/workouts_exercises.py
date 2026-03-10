from pydantic import BaseModel

from app.schemas.workouts_sets import WorkoutSetNested


class WorkoutExerciseBase(BaseModel):
    exercise_id: int
    exercise_index: int


class WorkoutExerciseNested(WorkoutExerciseBase):
    sets: list[WorkoutSetNested]

    model_config = {"from_attributes": True}


class WorkoutExerciseResponse(WorkoutExerciseBase):
    workout_id: int

    model_config = {"from_attributes": True}
