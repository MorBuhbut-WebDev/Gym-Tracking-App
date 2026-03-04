import uuid
from typing import Optional

from app.repositories import RoutineRepo
from app.errors import NotFoundError, ConflictError
from app.models import Routine


class RoutinePolicy:
    @staticmethod
    async def assert_exist(
        repo: RoutineRepo, user_id: uuid.UUID, routine_id: int
    ) -> Routine:
        routine = await repo.get_by_id(routine_id, user_id)

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
        routine = await repo.get_by_name(routine_name, routine_id, user_id)

        if routine is not None:
            raise ConflictError(f"{routine_name} already exists")
