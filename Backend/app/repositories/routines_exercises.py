from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select
from typing import Optional
from dataclasses import dataclass

from app.repositories.base import BaseRepo
from app.models import RoutineExercise
from app.schemas import RoutineAddExercise, ExerciseReorder
from app.repositories.mixins import ShiftIndicesMixin, ReorderMixin


@dataclass
class RoutineExerciseRow:
    exercise_id: int
    routine_id: int
    exercise_index: int
    planned_sets: int
    exercise_notes: Optional[str]


class RoutineExerciseRepo(BaseRepo[RoutineExercise], ShiftIndicesMixin, ReorderMixin):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(model=RoutineExercise, session=session)

    async def add_exercise(
        self,
        routine_id: int,
        exercise_id: int,
        exercise: RoutineAddExercise,
    ) -> RoutineExercise:
        result = (
            await self._session.execute(
                select(func.max(RoutineExercise.exercise_index)).where(
                    RoutineExercise.routine_id == routine_id
                )
            )
        ).scalar()

        max_exercise_index = 1 if result is None else result + 1

        routine_exercise = self.add(
            RoutineExercise.create(
                exercise_id=exercise_id,
                routine_id=routine_id,
                exercise_index=max_exercise_index,
                planned_sets=exercise.planned_sets,
                exercise_notes=exercise.exercise_notes,
            ),
        )
        return routine_exercise

    async def get_link(
        self,
        routine_id: int,
        exercise_id: int,
    ) -> Optional[RoutineExercise]:
        routine_exercise = await self.get(
            condition=(RoutineExercise.routine_id == routine_id)
            & (RoutineExercise.exercise_id == exercise_id),
        )

        return routine_exercise

    async def get_all(self, routine_id: int) -> list[RoutineExercise]:
        exercises = await super().get_all(
            condition=(RoutineExercise.routine_id == routine_id)
        )

        return exercises

    async def reorder_exercises(
        self, parent_id: int, payload: ExerciseReorder
    ) -> list[RoutineExerciseRow]:
        exercises = await super().reorder_exercises(parent_id, payload)
        return [RoutineExerciseRow(**exercise) for exercise in exercises]

    async def count_by_routine(self, routine_id: int) -> int:
        result = (
            await self._session.execute(
                select(func.count())
                .select_from(RoutineExercise)
                .where(RoutineExercise.routine_id == routine_id)
            )
        ).scalar()

        return 0 if result is None else result
