import uuid
from datetime import datetime
from decimal import Decimal
from typing import NamedTuple

from pydantic import BaseModel
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Workout
from app.repositories.base import BaseRepo


class WorkoutDetailRow(BaseModel):
    workout_id: int
    routine_id: int | None
    created_at: datetime
    ended_at: datetime | None
    workout_name: str
    exercise_id: int
    exercise_index: int
    exercise_name: str
    set_id: int
    set_index: int
    weight: Decimal | None
    reps: int | None
    notes: str | None


class WorkoutPeriod(NamedTuple):
    created_at: datetime
    ended_at: datetime | None


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
                        e.exercise_name,
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
                    JOIN exercises e
                      ON e.exercise_id = we.exercise_id
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

        return [WorkoutDetailRow.model_validate(row) for row in rows]

    async def get_all_by_date_range(
        self, user_id: uuid.UUID, start_date: datetime, end_date: datetime
    ) -> list[Workout]:
        return await self.get_all(
            condition=(Workout.user_id == user_id)
            & (Workout.created_at >= start_date)
            & (Workout.created_at < end_date)
        )

    async def get_by_id(self, workout_id: int, user_id: uuid.UUID) -> Workout | None:
        return await self.get(
            condition=(Workout.user_id == user_id) & (Workout.workout_id == workout_id)
        )

    async def get_period(
        self, workout_id: int, user_id: uuid.UUID
    ) -> WorkoutPeriod | None:
        row = (
            await self._session.execute(
                select(Workout.created_at, Workout.ended_at).where(
                    (Workout.user_id == user_id) & (Workout.workout_id == workout_id)
                )
            )
        ).fetchone()

        return (
            WorkoutPeriod(created_at=row.created_at, ended_at=row.ended_at)
            if row
            else None
        )
