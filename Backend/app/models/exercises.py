import uuid
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import Integer, String, Date, UniqueConstraint, func, text
from sqlalchemy.dialects.postgresql import UUID
from datetime import date

from app.db import Base


class Exercise(Base):
    __tablename__ = "exercises"

    exercise_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    begda: Mapped[date] = mapped_column(
        Date, nullable=False, server_default=func.current_date()
    )
    endda: Mapped[date] = mapped_column(
        Date, nullable=False, server_default=text("DATE '9999-12-31'")
    )
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    exercise_name: Mapped[str] = mapped_column(String(36), nullable=False)

    __table_args__ = (
        UniqueConstraint(
            "user_id", "exercise_name", "endda", name="uq_user_endda_exercise_name"
        ),
    )

    @classmethod
    def create(cls, *, user_id: uuid.UUID, exercise_name: str) -> "Exercise":
        return cls(user_id=user_id, exercise_name=exercise_name)
