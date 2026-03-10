from pydantic import BaseModel
from decimal import Decimal
from typing import Optional


class WorkoutSetBase(BaseModel):
    set_id: int
    set_index: int
    weight: Optional[Decimal]
    reps: Optional[int]
    notes: Optional[str]


class WorkoutSetNested(WorkoutSetBase):
    model_config = {"from_attributes": True}


class WorkoutSetResponse(WorkoutSetBase):
    workout_id: int
    exercise_id: int

    model_config = {"from_attributes": True}
