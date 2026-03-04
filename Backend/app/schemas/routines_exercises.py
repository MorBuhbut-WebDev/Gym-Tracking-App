from pydantic import BaseModel, model_validator, PositiveInt, ConfigDict
from typing import Optional, Self

from app.schemas.types import NotEmptyString


class RoutineAddExercise(BaseModel):
    model_config = ConfigDict(extra="forbid")

    planned_sets: PositiveInt = 3
    exercise_notes: Optional[NotEmptyString] = None


class RoutineUpdateExercise(BaseModel):
    planned_sets: Optional[PositiveInt] = None
    exercise_notes: Optional[NotEmptyString] = None

    @model_validator(mode="after")
    def ensure_at_least_one_exist(self) -> Self:
        if self.planned_sets is None and self.exercise_notes is None:
            raise ValueError("planned sets | exercise notes must be provided")
        return self


class RoutineExerciseResponse(BaseModel):
    exercise_id: int
    routine_id: int
    exercise_index: int
    planned_sets: int
    exercise_notes: Optional[str]

    model_config = {"from_attributes": True}
