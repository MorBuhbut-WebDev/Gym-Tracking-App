import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Row, text
from datetime import datetime

from app.repositories.base_repo import BaseRepo
from app.models import Workout


class WorkoutRepo(BaseRepo[Workout]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(model=Workout, session=session)

    async def get_with_exercises_and_sets(self, workout_id: int) -> list[Row]:
        rows = (
            await self._session.execute(
                text(
                    """
                    SELECT
                        w.workout_id,
                        w.routine_id,
                        w.created_at,
                        w.ended_at,
                        w.workout_name,
                        we.exercise_id,
                        we.exercise_index,
                        ws.set_id,
                        ws.set_index,
                        ws.weight,
                        ws.reps,
                        ws.notes
                    FROM workouts_exercises we
                    JOIN workouts w
                      ON we.workout_id = w.workout_id
                    JOIN workouts_sets ws
                      ON ws.workout_id = we.workout_id
                     AND ws.exercise_id = we.exercise_id
                    WHERE w.workout_id = :workout_id
                    ORDER BY we.exercise_index, ws.set_index
                    """
                ),
                {"workout_id": workout_id},
            )
        ).fetchall()

        return rows

    async def get_all(
        self, user_id: uuid.UUID, start_date: datetime, end_date: datetime
    ) -> list[Workout]:
        return await super().get_all(
            condition=(Workout.user_id == user_id)
            & (Workout.created_at >= start_date)
            & (Workout.created_at < end_date)
        )
