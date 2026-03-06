from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from app.repositories.base_repo import BaseRepo
from app.models import WorkoutSet


class WorkoutSetRepo(BaseRepo[WorkoutSet]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(model=WorkoutSet, session=session)

    async def generate_sets(self, workout_id: int, routine_id: int) -> None:
        await self._session.execute(
            text(
                """
            INSERT INTO workouts_sets (workout_id, exercise_id, set_index)
            SELECT
                :workout_id,
                re.exercise_id,
                gs.set_index
            FROM routines_exercises re
            CROSS JOIN generate_series(1, re.planned_sets) gs(set_index)
            WHERE re.routine_id = :routine_id    
            """
            ),
            {"workout_id": workout_id, "routine_id": routine_id},
        )
