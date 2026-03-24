import uuid

from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Routine
from app.repositories.base import BaseRepo


class RoutineDetailRow(BaseModel):
    routine_id: int
    user_id: uuid.UUID
    routine_name: str
    exercise_id: int
    exercise_index: int
    planned_sets: int
    exercise_notes: str | None
    exercise_name: str


class RoutineRepo(BaseRepo[Routine]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(model=Routine, session=session)

    async def get_all(self, user_id: uuid.UUID) -> list[Routine]:
        routines = await super().get_all(
            condition=(Routine.user_id == user_id),
        )
        return routines

    async def get_by_name(
        self, routine_name: str, routine_id: int | None, user_id: uuid.UUID
    ) -> Routine | None:
        condition = (Routine.user_id == user_id) & (
            Routine.routine_name == routine_name
        )

        if routine_id is not None:
            condition &= Routine.routine_id != routine_id

        return await self.get(condition)

    async def get_by_id(self, routine_id: int, user_id: uuid.UUID) -> Routine | None:
        return await self.get(
            condition=(
                (Routine.user_id == user_id) & (Routine.routine_id == routine_id)
            ),
        )

    async def get_with_exercises(self, routine_id: int) -> list[RoutineDetailRow]:
        rows = (
            (
                await self._session.execute(
                    text(
                        """
                    SELECT
                        r.routine_id,
                        r.user_id,
                        r.routine_name,
                        re.exercise_id,
                        re.exercise_index,
                        re.planned_sets,
                        re.exercise_notes,
                        e.exercise_name
                    FROM routines_exercises re
                    JOIN routines r
                      ON re.routine_id = r.routine_id
                    JOIN exercises e
                      ON re.exercise_id = e.exercise_id
                    WHERE r.routine_id = :routine_id
                    ORDER BY re.exercise_index 
                    """
                    ),
                    {"routine_id": routine_id},
                )
            )
            .mappings()
            .fetchall()
        )

        return [RoutineDetailRow.model_validate(row) for row in rows]
