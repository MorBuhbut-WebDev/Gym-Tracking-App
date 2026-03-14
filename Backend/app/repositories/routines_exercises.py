from typing import NamedTuple

from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import RoutineExercise
from app.repositories.base import BaseRepo
from app.repositories.mixins import ShiftIndicesMixin
from app.schemas import RoutineAddExercise


class LinkedRoutine(NamedTuple):
    routine_ids: list[int]
    exercise_indices: list[int]


class RoutineExerciseRepo(BaseRepo[RoutineExercise], ShiftIndicesMixin):
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
    ) -> RoutineExercise | None:
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

    async def get_linked_routines(self, exercise_id: int) -> LinkedRoutine:
        routines = (
            await self._session.execute(
                select(
                    RoutineExercise.routine_id, RoutineExercise.exercise_index
                ).where(RoutineExercise.exercise_id == exercise_id)
            )
        ).fetchall()

        return LinkedRoutine(
            routine_ids=[routine.routine_id for routine in routines],
            exercise_indices=[routine.exercise_index for routine in routines],
        )

    async def delete_by_exercise(self, exercise_id: int) -> None:
        await self._session.execute(
            delete(RoutineExercise).where(RoutineExercise.exercise_id == exercise_id)
        )
