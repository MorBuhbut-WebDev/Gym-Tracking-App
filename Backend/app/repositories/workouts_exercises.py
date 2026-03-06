from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from app.repositories.base_repo import BaseRepo
from app.models import WorkoutExercise


class WorkoutExerciseRepo(BaseRepo[WorkoutExercise]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(model=WorkoutExercise, session=session)

    async def snapshot_exercises(self, workout_id: int, routine_id: int) -> None:
        await self._session.execute(
            text(
                """
            INSERT INTO workouts_exercises (workout_id, exercise_id, exercise_index)
            SELECT
                :workout_id,
                exercise_id,
                exercise_index
            FROM routines_exercises
            WHERE routine_id = :routine_id    
            """
            ),
            {"workout_id": workout_id, "routine_id": routine_id},
        )
