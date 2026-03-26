from decimal import Decimal

from app.schemas.shared import AppBaseModel


class WorkoutSetResponse(AppBaseModel):
    set_id: int
    set_index: int
    weight: Decimal | None
    reps: int | None
    notes: str | None
