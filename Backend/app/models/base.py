from app.db.session import Base


class HasParentID(Base):
    __abstract__ = True
    PARENT_ID: str
    EXERCISE_INDEX_CONSTRAINT: str
