import uuid

from app.repositories import ExerciseRepo, RoutineRepo, RoutineExerciseRepo
from app.errors import NotFoundError, ConflictError, BadRequestError
from app.models import Exercise, Routine, RoutineExercise
from app.policies.exercises import ExercisePolicy
from app.policies.routines import RoutinePolicy
from app.schemas import ReOrderSchema


class RoutineExercisePolicy:
    @staticmethod
    async def assert_exercise_not_exist(
        repo: RoutineExerciseRepo, routine_id: int, exercise_id: int
    ) -> None:
        routine_exercise = await repo.get_exercise_from_routine_by_id(
            routine_id, exercise_id
        )

        if routine_exercise is not None:
            raise ConflictError(
                f"Exercise with id {exercise_id} already exists for the routine with id {routine_id}"
            )

    @staticmethod
    async def assert_exercise_index_is_unique(
        repo: RoutineExerciseRepo, routine_id: int, exercise_index: int
    ) -> None:
        routine_exercise = await repo.get_exercise_from_routine_by_index(
            routine_id, exercise_index
        )

        if routine_exercise is not None:
            raise ConflictError(
                f"Exercise with position {exercise_index} already exists!"
            )

    @staticmethod
    async def assert_routine_and_exercise_accessible(
        exercises_repo: ExerciseRepo,
        routines_repo: RoutineRepo,
        user_id: uuid.UUID,
        routine_id: int,
        exercise_id: int,
    ) -> tuple[Exercise, Routine]:
        routine = await RoutinePolicy.assert_routine_exist(
            repo=routines_repo, user_id=user_id, routine_id=routine_id
        )

        exercise = await ExercisePolicy.assert_exercise_exists(
            repo=exercises_repo, user_id=user_id, exercise_id=exercise_id
        )

        return routine, exercise

    @staticmethod
    async def assert_link_accessible(
        routines_repo: RoutineRepo,
        routines_exercises_repo: RoutineExerciseRepo,
        user_id: uuid.UUID,
        routine_id: int,
        exercise_id: int,
    ) -> tuple[Routine, RoutineExercise]:
        routine = await RoutinePolicy.assert_routine_exist(
            repo=routines_repo, user_id=user_id, routine_id=routine_id
        )

        routine_exercise = (
            await routines_exercises_repo.get_exercise_from_routine_by_id(
                routine_id, exercise_id
            )
        )

        if routine_exercise is None:
            raise NotFoundError(
                f"Exercise with id {exercise_id} doesn't exist in routine with id {routine_id}"
            )

        return routine, routine_exercise

    @staticmethod
    async def assert_submitted_exercises_valid(
        repo: RoutineExerciseRepo, routine_id: int, reordered_schema: ReOrderSchema
    ) -> None:
        routine_exercises_ids = [
            exercise.exercise_id
            for exercise in await repo.get_all_exercises_from_routine(routine_id)
        ]

        submitted_exercises_ids, _ = reordered_schema.unzip()

        if set(routine_exercises_ids) != set(submitted_exercises_ids):
            raise BadRequestError(
                "Submitted exercises must match exactly the exercises in the routine"
            )
