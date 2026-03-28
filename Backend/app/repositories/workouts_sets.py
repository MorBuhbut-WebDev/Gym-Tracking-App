from sqlalchemy import func, select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import WorkoutSet
from app.repositories.base import BaseRepo
from app.schemas import WorkoutSetCreate


class WorkoutSetRepo(BaseRepo[WorkoutSet]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(model=WorkoutSet, session=session)

    async def add_set(self, workout_id: int, exercise_id: int, set: WorkoutSetCreate):
        result = (
            await self._session.execute(
                select(func.max(WorkoutSet.set_index)).where(
                    (WorkoutSet.workout_id == workout_id)
                    & (WorkoutSet.exercise_id == exercise_id)
                )
            )
        ).scalar()

        set_index = 1 if result is None else result + 1

        return self.add(
            WorkoutSet.create(
                workout_id=workout_id,
                exercise_id=exercise_id,
                set_index=set_index,
                weight=set.weight,
                reps=set.reps,
                notes=set.notes,
            )
        )

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
