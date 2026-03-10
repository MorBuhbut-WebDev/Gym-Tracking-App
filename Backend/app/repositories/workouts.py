import uuid
from typing import Optional
from datetime import datetime
from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from dataclasses import dataclass

from app.repositories.base import BaseRepo
from app.models import Workout


@dataclass
class WorkoutDetailRow:
    workout_id: int
    routine_id: int
    created_at: datetime
    ended_at: Optional[datetime]
    workout_name: str
    exercise_id: int
    exercise_index: int
    set_id: int
    set_index: int
    weight: Optional[Decimal]
    reps: Optional[int]
    notes: Optional[str]


class WorkoutRepo(BaseRepo[Workout]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(model=Workout, session=session)

    async def get_with_exercises_and_sets(
        self, workout_id: int
    ) -> list[WorkoutDetailRow]:
        rows = (
            (
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
            )
            .mappings()
            .fetchall()
        )

        return [WorkoutDetailRow(**row) for row in rows]

    async def get_all_by_date_range(
        self, user_id: uuid.UUID, start_date: datetime, end_date: datetime
    ) -> list[Workout]:
        return await self.get_all(
            condition=(Workout.user_id == user_id)
            & (Workout.created_at >= start_date)
            & (Workout.created_at < end_date)
        )
