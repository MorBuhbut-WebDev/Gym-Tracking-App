from app.db import Base


class OrderedExerciseModel(Base):
    __abstract__ = True
    PARENT_ID: str
    EXERCISE_INDEX_CONSTRAINT: str
