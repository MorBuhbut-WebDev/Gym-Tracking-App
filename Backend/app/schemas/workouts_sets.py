from decimal import Decimal

from pydantic import BaseModel


class WorkoutSetBase(BaseModel):
    set_id: int
    set_index: int
    weight: Decimal | None
    reps: int | None
    notes: str | None


class WorkoutSetNested(WorkoutSetBase):
    model_config = {"from_attributes": True}


class WorkoutSetResponse(WorkoutSetBase):
    workout_id: int
    exercise_id: int

    model_config = {"from_attributes": True}
