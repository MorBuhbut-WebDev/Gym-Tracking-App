import uuid

from app.exceptions import NotFoundException
from app.models import Workout
from app.repositories import WorkoutRepo


class WorkoutPolicy:
    @staticmethod
    async def assert_exists(
        repo: WorkoutRepo, user_id: uuid.UUID, workout_id: int
    ) -> Workout:
        workout = await repo.get_by_id(workout_id, user_id)

        if workout is None:
            raise NotFoundException(f"Workout with id: {workout_id} not found")

        return workout
