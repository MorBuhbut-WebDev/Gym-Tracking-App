from decimal import Decimal

from pydantic import BaseModel

from app.schemas.shared import AppBaseModel


class WorkoutSetBase(BaseModel):
    set_id: int
    set_index: int
    weight: Decimal | None
    reps: int | None
    notes: str | None


class WorkoutSetNested(WorkoutSetBase, AppBaseModel):
    pass


class WorkoutSetResponse(WorkoutSetBase, AppBaseModel):
    workout_id: int
    exercise_id: int
