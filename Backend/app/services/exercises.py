from app.schemas import ExerciseCreate, ExerciseUpdate, ExerciseResponse
from app.auth import User
from app.db import UnitOfWork, catch_unique_violation
from app.policies import ExercisePolicy
from app.models import Exercise


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

    async def get_all(self, uow: UnitOfWork, user: User) -> list[ExerciseResponse]:
        exercises = await uow.exercises_repo.get_all(user.user_id)
        return [ExerciseResponse.model_validate(exercise) for exercise in exercises]

    async def get(
        self, uow: UnitOfWork, user: User, exercise_id: int
    ) -> ExerciseResponse:
        exercise = await ExercisePolicy.assert_exists(
            repo=uow.exercises_repo,
            user_id=user.user_id,
            exercise_id=exercise_id,
        )
        return ExerciseResponse.model_validate(exercise)

    async def update(
        self,
        uow: UnitOfWork,
        user: User,
        exercise_id: int,
        payload: ExerciseUpdate,
    ) -> ExerciseResponse:
        exercise = await ExercisePolicy.assert_exists(
            repo=uow.exercises_repo,
            user_id=user.user_id,
            exercise_id=exercise_id,
        )

        await ExercisePolicy.assert_name_is_unique(
            repo=uow.exercises_repo,
            user_id=user.user_id,
            exercise_name=payload.exercise_name,
            exercise_id=exercise_id,
        )

        exercise = uow.exercises_repo.update(old=exercise, updated=payload)

        async with catch_unique_violation(f"{payload.exercise_name} already exists"):
            await uow.flush()

        return ExerciseResponse.model_validate(exercise)

    async def delete(self, uow: UnitOfWork, user: User, exercise_id: int) -> None:
        exercise = await ExercisePolicy.assert_exists(
            repo=uow.exercises_repo,
            user_id=user.user_id,
            exercise_id=exercise_id,
        )

        uow.exercises_repo.soft_delete(exercise)

        routine_ids, deleted_indices = (
            await uow.routines_exercises_repo.get_links_by_exercise(exercise_id)
        )

        if not routine_ids or not deleted_indices:
            return

        await uow.routines_exercises_repo.delete_by_exercise(exercise_id)
        await uow.flush()
        await uow.routines_exercises_repo.shift_indices_after_delete(
            routine_ids,
            deleted_indices,
        )


def get_exercises_service() -> ExerciseService:
    return ExerciseService()
