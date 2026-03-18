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
        repo: WorkoutRepo, user_id: uuid.UUID, workout_id: int, payload: WorkoutUpdate
    ) -> None:
        if payload.created_at is not None and payload.ended_at is not None:
            return

        db_workout_period = await repo.get_period(workout_id, user_id)

        assert db_workout_period is not None, (
            "workout exsistence must be checked before updating dates"
        )

        if payload.created_at is not None:
            if db_workout_period.ended_at is None:
                return

            if payload.created_at >= db_workout_period.ended_at:
                raise BadRequestException(
                    "created_at cannot be after the workout's ended_at"
                )

        elif (
            payload.ended_at is not None
            and payload.ended_at <= db_workout_period.created_at
        ):
            raise BadRequestException("ended_at must be after the workout's created_at")
