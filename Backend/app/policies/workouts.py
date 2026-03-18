import uuid

from app.exceptions import BadRequestException, NotFoundException
from app.models import Workout
from app.repositories import WorkoutRepo
from app.schemas import WorkoutUpdate


class WorkoutPolicy:
    @staticmethod
    async def assert_exists(
        repo: WorkoutRepo, user_id: uuid.UUID, workout_id: int
    ) -> Workout:
        workout = await repo.get_by_id(workout_id, user_id)

        if workout is None:
            raise NotFoundException(f"Workout with id: {workout_id} not found")

        return workout

    @staticmethod
    async def assert_update_dates_valid(
        workout: Workout, payload: WorkoutUpdate
    ) -> None:
        if payload.created_at is not None and payload.ended_at is not None:
            return

        if payload.created_at is not None:
            if workout.ended_at is None:
                return

            if payload.created_at >= workout.ended_at:
                raise BadRequestException(
                    "created_at cannot be after the workout's ended_at"
                )

        elif payload.ended_at is not None and payload.ended_at <= workout.created_at:
            raise BadRequestException("ended_at must be after the workout's created_at")
