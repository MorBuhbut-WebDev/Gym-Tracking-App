from app.exceptions import ConflictException
from app.repositories import WorkoutExerciseRepo


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
