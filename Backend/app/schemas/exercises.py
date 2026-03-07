import uuid
from datetime import date

from pydantic import BaseModel

from app.schemas.types import Name


class ExerciseBase(BaseModel):
    exercise_name: Name


class ExerciseCreate(ExerciseBase):
    pass


class ExerciseUpdate(ExerciseBase):
    pass


class ExerciseResponse(BaseModel):
    exercise_id: int
    user_id: uuid.UUID
    exercise_name: str
    begda: date
    endda: date

    model_config = {"from_attributes": True}
