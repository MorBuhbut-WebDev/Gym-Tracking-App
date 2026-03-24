from typing import NamedTuple

from pydantic import BaseModel
from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import RoutineExercise
from app.repositories.mixins import ReorderMixin, ShiftIndicesMixin
from app.repositories.ordered_exercises_base import OrderedExerciseRepo
from app.schemas import ExerciseReorder, RoutineAddExercise


class LinkedRoutine(NamedTuple):
    routine_ids: list[int]
    exercise_indices: list[int]


class RoutineExerciseRow(BaseModel):
    exercise_id: int
    routine_id: int
    exercise_index: int
    planned_sets: int
    exercise_notes: str | None


class RoutineExerciseRepo(
    OrderedExerciseRepo[RoutineExercise], ShiftIndicesMixin, ReorderMixin
):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(model=RoutineExercise, session=session)

    async def add_exercise(
        self,
        routine_id: int,
        exercise_id: int,
        exercise: RoutineAddExercise,
    ) -> RoutineExercise:
        max_exercise_index = await self._compute_next_index(routine_id)

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
        return await super().get_link(routine_id, exercise_id)

    async def get_all(self, routine_id: int) -> list[RoutineExercise]:
        exercises = await super().get_all(
            condition=(RoutineExercise.routine_id == routine_id)
        )

        return exercises

    async def get_exercise_ids(self, routine_id: int) -> list[int]:
        return await super().get_exercise_ids(routine_id)

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

    async def reorder_exercises(
        self, parent_id: int, payload: ExerciseReorder
    ) -> list[RoutineExerciseRow]:
        exercises = await super().reorder_exercises(parent_id, payload)
        return [RoutineExerciseRow.model_validate(exercise) for exercise in exercises]

    async def count_by_routine(self, routine_id: int) -> int:
        result = (
            await self._session.execute(
                select(func.count())
                .select_from(RoutineExercise)
                .where(RoutineExercise.routine_id == routine_id)
            )
        ).scalar()

        return 0 if result is None else result
