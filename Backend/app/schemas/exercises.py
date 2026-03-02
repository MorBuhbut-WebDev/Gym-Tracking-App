import uuid
from pydantic import BaseModel
from datetime import date

from app.schemas.types import Name


class BaseExerciseSchema(BaseModel):
    exercise_name: Name


class CreateExerciseSchema(BaseExerciseSchema):
    pass


class UpdateExerciseSchema(BaseExerciseSchema):
    pass


class ReturnExerciseSchema(BaseModel):
    exercise_id: int
    user_id: uuid.UUID
    exercise_name: str
    begda: date
    endda: date

    model_config = {"from_attributes": True}
