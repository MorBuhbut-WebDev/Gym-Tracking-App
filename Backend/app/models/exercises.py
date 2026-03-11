import uuid
from datetime import date

from sqlalchemy import Date, ForeignKey, Integer, String, UniqueConstraint, func, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class Exercise(Base):
    __tablename__ = "exercises"

    exercise_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.user_id", ondelete="CASCADE"),
    )
    begda: Mapped[date] = mapped_column(
        Date, default=date.today, server_default=func.current_date()
    )
    endda: Mapped[date] = mapped_column(
        Date,
        default=date(9999, 12, 31),
        server_default=text("DATE '9999-12-31'"),
    )
    exercise_name: Mapped[str] = mapped_column(String(36))

    __table_args__ = (
        UniqueConstraint(
            "user_id", "exercise_name", "endda", name="uq_user_endda_exercise_name"
        ),
    )

    @classmethod
    def create(cls, *, user_id: uuid.UUID, exercise_name: str) -> "Exercise":
        return cls(user_id=user_id, exercise_name=exercise_name)
