from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, Field, PositiveInt

from app.schemas.shared import AppBaseModel
from app.schemas.types import NotEmptyString


class WorkoutSetCreate(BaseModel):
    weight: Annotated[Decimal, Field(gt=0, max_digits=6, decimal_places=3)] | None = (
        None
    )
    reps: PositiveInt | None = None
    notes: NotEmptyString | None = None


class WorkoutSetResponse(AppBaseModel):
    set_id: int
    set_index: int
    weight: Decimal | None
    reps: int | None
    notes: str | None
    prev_weight: Decimal | None
    prev_reps: int | None
    prev_notes: str | None
