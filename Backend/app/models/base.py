from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class OrderedExerciseModel(Base):
    __abstract__ = True
    PARENT_ID: str
    EXERCISE_INDEX_CONSTRAINT: str
    exercise_index: Mapped[int] = mapped_column(Integer)
