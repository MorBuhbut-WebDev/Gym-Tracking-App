from datetime import date

from pydantic import BaseModel

from app.schemas.shared import AppBaseModel
from app.schemas.types import Name


class ExerciseBase(BaseModel):
    exercise_name: Name


class ExerciseCreate(ExerciseBase):
    pass


class ExerciseUpdate(ExerciseBase):
    pass


class ExerciseResponse(AppBaseModel):
    exercise_id: int
    exercise_name: str
    begda: date
