from typing import Self

from pydantic import BaseModel, PositiveInt, model_validator

from app.schemas.shared import AppBaseModel
from app.schemas.types import NotEmptyString


class RoutineAddExercise(BaseModel):
    planned_sets: PositiveInt = 3
    exercise_notes: NotEmptyString | None = None


class RoutineUpdateExercise(BaseModel):
    planned_sets: PositiveInt | None = None
    exercise_notes: NotEmptyString | None = None

    @model_validator(mode="after")
    def ensure_at_least_one_exist(self) -> Self:
        if self.planned_sets is None and self.exercise_notes is None:
            raise ValueError("planned sets | exercise notes must be provided")
        return self


class RoutineExerciseResponse(AppBaseModel):
    exercise_id: int
    routine_id: int
    exercise_index: int
    planned_sets: int
    exercise_notes: str | None
