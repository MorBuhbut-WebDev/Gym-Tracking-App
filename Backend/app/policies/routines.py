import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.repositories import RoutineRepo, RoutineExerciseRepo
from app.errors import NotFoundError, ConflictError
from app.models import Routine, RoutineExercise


class RoutinePolicy:
    @staticmethod
    async def assert_routine_exist(
        repo: RoutineRepo, user_id: uuid.UUID, routine_id: int
    ) -> Routine:
        routine = await repo.get_routine_by_id(routine_id, user_id)

        if routine is None:
            raise NotFoundError(f"Routine with id: {routine_id} not found")

        return routine

    @staticmethod
    async def assert_name_is_unique(
        repo: RoutineRepo,
        user_id: uuid.UUID,
        routine_name: str,
        routine_id: Optional[int] = None,
    ) -> None:
        routine = await repo.get_routine_by_name(routine_name, routine_id, user_id)

        if routine is not None:
            raise ConflictError(f"{routine_name} already exists")
