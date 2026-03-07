from app.auth import User
from app.db import UnitOfWork, catch_unique_violation
from app.models import Exercise
from app.policies import ExercisePolicy
from app.schemas import ExerciseCreate, ExerciseResponse


class ExerciseService:
    async def create(
        self, uow: UnitOfWork, user: User, payload: ExerciseCreate
    ) -> ExerciseResponse:
        await ExercisePolicy.assert_name_is_unique(
            repo=uow.exercises_repo,
            user_id=user.user_id,
            exercise_name=payload.exercise_name,
        )

        exercise = uow.exercises_repo.add(
            Exercise.create(user_id=user.user_id, exercise_name=payload.exercise_name)
        )

        async with catch_unique_violation(f"{payload.exercise_name} already exists"):
            await uow.flush()

        return ExerciseResponse.model_validate(exercise)
