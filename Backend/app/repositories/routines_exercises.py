from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func
from typing import Optional

from app.repositories.base_repo import BaseRepo
from app.repositories.mixins import ReorderMixin
from app.models import RoutineExercise
from app.schemas import AddRoutineExerciseSchema


class RoutineExerciseRepo(BaseRepo[RoutineExercise], ReorderMixin):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(model=RoutineExercise, session=session)

    def add_exercise_to_routine(
        self,
        routine_id: int,
        exercise_id: int,
        exercise: AddRoutineExerciseSchema,
    ) -> RoutineExercise:
        routine_exercise = self.add(
            RoutineExercise.create(
                exercise_id=exercise_id,
                routine_id=routine_id,
                exercise_index=exercise.exercise_index,
                planned_sets=exercise.planned_sets,
                exercise_notes=exercise.exercise_notes,
            ),
        )
        return routine_exercise

    async def get_exercise_from_routine_by_id(
        self,
        routine_id: int,
        exercise_id: int,
    ) -> Optional[RoutineExercise]:
        routine_exercise = await self.get(
            condition=(RoutineExercise.routine_id == routine_id)
            & (RoutineExercise.exercise_id == exercise_id),
        )

        return routine_exercise

    async def get_exercise_from_routine_by_index(
        self,
        routine_id: int,
        exercise_index: int,
    ) -> Optional[RoutineExercise]:
        routine_exercise = await self.get(
            condition=(RoutineExercise.routine_id == routine_id)
            & (RoutineExercise.exercise_index == exercise_index),
        )

        return routine_exercise

    async def get_all_exercises_from_routine(
        self, routine_id: int
    ) -> list[RoutineExercise]:
        exercises = await self.get_all(
            condition=(RoutineExercise.routine_id == routine_id)
        )

        return exercises
