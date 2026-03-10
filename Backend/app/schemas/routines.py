import uuid

from pydantic import BaseModel

from app.schemas.shared import AppBaseModel
from app.schemas.types import Name


class RoutineBase(BaseModel):
    routine_name: Name


class RoutineCreate(RoutineBase):
    pass


class RoutineUpdate(RoutineBase):
    pass


class RoutineResponse(AppBaseModel):
    routine_id: int
    user_id: uuid.UUID
    routine_name: str
