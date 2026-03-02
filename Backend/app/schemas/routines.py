import uuid
from pydantic import BaseModel

from app.schemas.types import Name


class BaseRoutineSchema(BaseModel):
    routine_name: Name


class CreateRoutineSchema(BaseRoutineSchema):
    pass


class UpdateRoutineSchema(BaseRoutineSchema):
    pass


class ReturnRoutineSchema(BaseModel):
    routine_id: int
    user_id: uuid.UUID
    routine_name: str

    model_config = {"from_attributes": True}
