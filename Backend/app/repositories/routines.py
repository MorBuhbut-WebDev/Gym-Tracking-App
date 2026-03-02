import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.repositories.base_repo import BaseRepo
from app.models import Routine
from app.schemas import CreateRoutineSchema


class RoutineRepo(BaseRepo[Routine]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(model=Routine, session=session)

    def add_routine(self, routine: CreateRoutineSchema, user_id: uuid.UUID) -> Routine:
        db_routine = self.add(
            Routine.create(routine_name=routine.routine_name, user_id=user_id),
        )
        return db_routine

    async def get_all_routines(self, user_id: uuid.UUID) -> list[Routine]:
        routines = await self.get_all(
            condition=(Routine.user_id == user_id),
        )
        return routines

    async def get_routine_by_name(
        self, routine_name: str, routine_id: Optional[int], user_id: uuid.UUID
    ) -> Optional[Routine]:
        condition = (Routine.user_id == user_id) & (
            Routine.routine_name == routine_name
        )

        if routine_id is not None:
            condition &= Routine.routine_id != routine_id

        return await self.get(condition)

    async def get_routine_by_id(
        self, routine_id: int, user_id: uuid.UUID
    ) -> Optional[Routine]:
        return await self.get(
            condition=(
                (Routine.user_id == user_id) & (Routine.routine_id == routine_id)
            ),
        )
