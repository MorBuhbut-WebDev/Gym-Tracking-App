import uuid

from app.exceptions import NotFoundException
from app.models import Workout, WorkoutSet
from app.policies import WorkoutPolicy
from app.repositories import WorkoutRepo, WorkoutSetRepo


class WorkoutSetPolicy:
    @staticmethod
    async def assert_link_exists(
        workouts_repo: WorkoutRepo,
        workouts_sets_repo: WorkoutSetRepo,
        user_id: uuid.UUID,
        workout_id: int,
        exercise_id: int,
        set_id: int,
    ) -> tuple[Workout, WorkoutSet]:
        workout = await WorkoutPolicy.assert_exists(
            repo=workouts_repo, user_id=user_id, workout_id=workout_id
        )

        workout_set = await workouts_sets_repo.get_link(workout_id, exercise_id, set_id)

        if workout_set is None:
            raise NotFoundException(
                f"Set with id {set_id} doesn't exist in Exercise with id {exercise_id} and workout with id {workout_id}"
            )

        return workout, workout_set
