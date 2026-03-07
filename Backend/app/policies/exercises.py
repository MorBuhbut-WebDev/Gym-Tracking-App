import uuid
from typing import Optional

from app.exceptions import ConflictException, NotFoundException
from app.models import Exercise
from app.repositories import ExerciseRepo


class ExercisePolicy:
    @staticmethod
    async def assert_exists(
        repo: ExerciseRepo, user_id: uuid.UUID, exercise_id: int
    ) -> Exercise:
        exercise = await repo.get_by_id(exercise_id, user_id)

        if exercise is None:
            raise NotFoundException(f"Exercise with id: {exercise_id} is not found")

        return exercise

    @staticmethod
    async def assert_name_is_unique(
        repo: ExerciseRepo,
        user_id: uuid.UUID,
        exercise_name: str,
        exercise_id: Optional[int] = None,
    ) -> None:
        exercise = await repo.get_by_name(exercise_name, exercise_id, user_id)

        if exercise is not None:
            raise ConflictException(f"{exercise_name} already exists")
