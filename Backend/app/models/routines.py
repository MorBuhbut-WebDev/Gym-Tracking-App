import uuid
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import Integer, String, UniqueConstraint, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from app.db import Base


class Routine(Base):
    __tablename__ = "routines"

    routine_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.user_id", ondelete="CASCADE", use_alter=True),
    )
    routine_name: Mapped[str] = mapped_column(String(36))

    __table_args__ = (
        UniqueConstraint("user_id", "routine_name", name="uq_user_routine_name"),
    )

    @classmethod
    def create(cls, *, user_id: uuid.UUID, routine_name: str) -> "Routine":
        return cls(user_id=user_id, routine_name=routine_name)
