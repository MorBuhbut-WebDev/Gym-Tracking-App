import uuid
from datetime import date
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Exercise
from app.repositories.base import BaseRepo


class ExerciseRepo(BaseRepo[Exercise]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(model=Exercise, session=session)

    @property
    def _is_active(self):
        return (Exercise.begda <= date.today()) & (Exercise.endda > date.today())

    async def get_all(self, user_id: uuid.UUID) -> list[Exercise]:
        exercises = await super().get_all(
            condition=((Exercise.user_id == user_id) & self._is_active),
        )
        return exercises

    async def get_by_name(
        self, exercise_name: str, exercise_id: Optional[int], user_id: uuid.UUID
    ) -> Optional[Exercise]:
        condition = (
            (Exercise.user_id == user_id)
            & (Exercise.exercise_name == exercise_name)
            & self._is_active
        )

        if exercise_id is not None:
            condition &= Exercise.exercise_id != exercise_id

        return await self.get(condition)

    async def get_by_id(
        self, exercise_id: int, user_id: uuid.UUID
    ) -> Optional[Exercise]:
        return await self.get(
            condition=(
                (Exercise.user_id == user_id)
                & (Exercise.exercise_id == exercise_id)
                & self._is_active
            ),
        )

    def soft_delete(self, exercise: Exercise) -> None:
        exercise.endda = date.today()
