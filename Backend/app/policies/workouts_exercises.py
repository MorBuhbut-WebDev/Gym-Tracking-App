import uuid

from app.exceptions import BadRequestException, ConflictException, NotFoundException
from app.models import Exercise, Workout, WorkoutExercise
from app.policies import ExercisePolicy, WorkoutPolicy
from app.repositories import ExerciseRepo, WorkoutExerciseRepo, WorkoutRepo
from app.schemas import ExerciseReorder


class WorkoutExercisePolicy:
    @staticmethod
    async def assert_not_linked(
        repo: WorkoutExerciseRepo, workout_id: int, exercise_id: int
    ) -> None:
        workout_exercise = await repo.get_link(workout_id, exercise_id)

        if workout_exercise is not None:
            raise ConflictException(
                f"Exercise with id {exercise_id} already exists for the workout with id {workout_id}"
            )

    @staticmethod
    async def assert_accessible(
        exercises_repo: ExerciseRepo,
        workouts_repo: WorkoutRepo,
        user_id: uuid.UUID,
        workout_id: int,
        exercise_id: int,
    ) -> tuple[Workout, Exercise]:
        workout = await WorkoutPolicy.assert_exists(
            repo=workouts_repo, user_id=user_id, workout_id=workout_id
        )

        exercise = await ExercisePolicy.assert_exists(
            repo=exercises_repo, user_id=user_id, exercise_id=exercise_id
        )

        return workout, exercise

    @staticmethod
    async def assert_link_exists(
        workouts_repo: WorkoutRepo,
        workouts_exercises_repo: WorkoutExerciseRepo,
        user_id: uuid.UUID,
        workout_id: int,
        exercise_id: int,
    ) -> tuple[Workout, WorkoutExercise]:
        workout = await WorkoutPolicy.assert_exists(
            repo=workouts_repo, user_id=user_id, workout_id=workout_id
        )

        workout_exercise = await workouts_exercises_repo.get_link(
            workout_id, exercise_id
        )

        if workout_exercise is None:
            raise NotFoundException(
                f"Exercise with id {exercise_id} doesn't exist in workout with id {workout_id}"
            )

        return workout, workout_exercise

    @staticmethod
    async def assert_valid_reorder(
        repo: WorkoutExerciseRepo, workout_id: int, payload: ExerciseReorder
    ) -> None:
        workout_exercise_ids = await repo.get_exercise_ids(workout_id)

        submitted_exercise_ids, _ = payload.unzip()

        if set(workout_exercise_ids) != set(submitted_exercise_ids):
            raise BadRequestException(
                "Submitted exercises must match exactly the exercises in the workout"
            )
