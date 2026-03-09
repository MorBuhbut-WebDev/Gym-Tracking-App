import uuid
from app.exceptions import ConflictException
from app.models import Exercise, Routine
from app.policies.exercises import ExercisePolicy
from app.policies.routines import RoutinePolicy
from app.repositories import ExerciseRepo, RoutineRepo, RoutineExerciseRepo


class RoutineExercisePolicy:
    @staticmethod
    async def assert_not_linked(
        repo: RoutineExerciseRepo, routine_id: int, exercise_id: int
    ) -> None:
        routine_exercise = await repo.get_link(routine_id, exercise_id)

        if routine_exercise is not None:
            raise ConflictException(
                f"Exercise with id {exercise_id} already exists for the routine with id {routine_id}"
            )

    @staticmethod
    async def assert_accessible(
        exercises_repo: ExerciseRepo,
        routines_repo: RoutineRepo,
        user_id: uuid.UUID,
        routine_id: int,
        exercise_id: int,
    ) -> tuple[Routine, Exercise]:
        routine = await RoutinePolicy.assert_exists(
            repo=routines_repo, user_id=user_id, routine_id=routine_id
        )

        exercise = await ExercisePolicy.assert_exists(
            repo=exercises_repo, user_id=user_id, exercise_id=exercise_id
        )

        return routine, exercise
