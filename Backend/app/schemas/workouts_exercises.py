from app.schemas.shared import AppBaseModel
from app.schemas.workouts_sets import WorkoutSetNested


class WorkoutExerciseNested(AppBaseModel):
    exercise_id: int
    exercise_index: int
    exercise_name: str
    sets: list[WorkoutSetNested]
