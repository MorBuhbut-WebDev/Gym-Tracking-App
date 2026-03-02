import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date
from typing import Optional

from app.repositories.base_repo import BaseRepo
from app.models import Exercise
from app.schemas import CreateExerciseSchema


class ExerciseRepo(BaseRepo[Exercise]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(model=Exercise, session=session)

    def add_exercise(
        self, exercise: CreateExerciseSchema, user_id: uuid.UUID
    ) -> Exercise:
        db_exercise = self.add(
            Exercise.create(user_id=user_id, exercise_name=exercise.exercise_name),
        )
        return db_exercise

    async def get_all_exercises(self, user_id: uuid.UUID) -> list[Exercise]:
        exercises = await self.get_all(
            condition=(
                (Exercise.user_id == user_id)
                & (Exercise.begda <= date.today())
                & (Exercise.endda > date.today())
            ),
        )
        return exercises

    async def get_exercise_by_name(
        self, exercise_name: str, exercise_id: Optional[int], user_id: uuid.UUID
    ) -> Optional[Exercise]:
        condition = (
            (Exercise.user_id == user_id)
            & (Exercise.exercise_name == exercise_name)
            & (Exercise.begda <= date.today())
            & (Exercise.endda > date.today())
        )

        if exercise_id is not None:
            condition &= Exercise.exercise_id != exercise_id

        return await self.get(condition)

    async def get_exercise_by_id(
        self, exercise_id: int, user_id: uuid.UUID
    ) -> Optional[Exercise]:
        return await self.get(
            condition=(
                (Exercise.user_id == user_id)
                & (Exercise.exercise_id == exercise_id)
                & (Exercise.begda <= date.today())
                & (Exercise.endda > date.today())
            ),
        )

    def soft_delete_exercise(self, exercise: Exercise) -> None:
        exercise.endda = date.today()
