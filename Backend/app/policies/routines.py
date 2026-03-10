import uuid

from app.exceptions import ConflictException, NotFoundException
from app.models import Routine
from app.repositories import RoutineRepo


class RoutinePolicy:
    @staticmethod
    async def assert_exists(
        repo: RoutineRepo, user_id: uuid.UUID, routine_id: int
    ) -> Routine:
        routine = await repo.get_by_id(routine_id, user_id)

        if routine is None:
            raise NotFoundException(f"Routine with id: {routine_id} not found")

        return routine

    @staticmethod
    async def assert_name_is_unique(
        repo: RoutineRepo,
        user_id: uuid.UUID,
        routine_name: str,
        routine_id: int | None = None,
    ) -> None:
        routine = await repo.get_by_name(routine_name, routine_id, user_id)

        if routine is not None:
            raise ConflictException(f"{routine_name} already exists")
