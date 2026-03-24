import uuid

from app.exceptions import ConflictException
from app.models import Exercise, Workout
from app.policies import ExercisePolicy, WorkoutPolicy
from app.repositories import ExerciseRepo, WorkoutExerciseRepo, WorkoutRepo


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
