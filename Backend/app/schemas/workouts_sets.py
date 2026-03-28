from decimal import Decimal
from typing import Annotated, Self

from pydantic import BaseModel, Field, PositiveInt, model_validator

from app.schemas.shared import AppBaseModel
from app.schemas.types import NotEmptyString


class WorkoutSetBase(BaseModel):
    weight: Annotated[Decimal, Field(gt=0, max_digits=6, decimal_places=3)] | None = (
        None
    )
    reps: PositiveInt | None = None
    notes: NotEmptyString | None = None


class WorkoutSetCreate(WorkoutSetBase):
    pass


class WorkoutSetUpdate(WorkoutSetBase):
    @model_validator(mode="after")
    def ensure_at_least_one_exist(self) -> Self:
        if self.weight is None and self.reps is None and self.notes is None:
            raise ValueError("weight | reps | notes must be provided")
        return self


class WorkoutSetResponse(AppBaseModel):
    set_id: int
    set_index: int
    weight: Decimal | None
    reps: int | None
    notes: str | None


class WorkoutSetNested(WorkoutSetResponse):
    prev_weight: Decimal | None
    prev_reps: int | None
    prev_notes: str | None
