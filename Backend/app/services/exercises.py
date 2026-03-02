from app.schemas import CreateExerciseSchema, UpdateExerciseSchema, ReturnExerciseSchema
from app.auth import User
from app.db import UnitOfWork, catch_unique_violation
from app.policies import ExercisePolicy


class ExerciseService:
    async def create_exercise(
        self, exercise: CreateExerciseSchema, uow: UnitOfWork, user: User
    ) -> ReturnExerciseSchema:
        await ExercisePolicy.assert_name_is_unique(
            repo=uow.exercises_repo,
            user_id=user.user_id,
            exercise_name=exercise.exercise_name,
        )

        db_exercise = uow.exercises_repo.add_exercise(exercise, user.user_id)

        async with catch_unique_violation(f"{exercise.exercise_name} already exists"):
            await uow.flush()

        return ReturnExerciseSchema.model_validate(db_exercise)

    async def get_all_exercises(
        self, uow: UnitOfWork, user: User
    ) -> list[ReturnExerciseSchema]:
        exercises = await uow.exercises_repo.get_all_exercises(user.user_id)

        return [
            ReturnExerciseSchema.model_validate(db_exercise)
            for db_exercise in exercises
        ]

    async def get_exercise(
        self, uow: UnitOfWork, user: User, exercise_id: int
    ) -> ReturnExerciseSchema:
        exercise = await ExercisePolicy.assert_exercise_exists(
            repo=uow.exercises_repo,
            user_id=user.user_id,
            exercise_id=exercise_id,
        )
        return ReturnExerciseSchema.model_validate(exercise)

    async def update_exercise(
        self,
        uow: UnitOfWork,
        user: User,
        exercise_id: int,
        new_exercise: UpdateExerciseSchema,
    ) -> ReturnExerciseSchema:
        exercise = await ExercisePolicy.assert_exercise_exists(
            repo=uow.exercises_repo,
            user_id=user.user_id,
            exercise_id=exercise_id,
        )

        await ExercisePolicy.assert_name_is_unique(
            repo=uow.exercises_repo,
            user_id=user.user_id,
            exercise_name=new_exercise.exercise_name,
            exercise_id=exercise_id,
        )

        updated_exercise = uow.exercises_repo.update(old=exercise, updated=new_exercise)

        async with catch_unique_violation(
            f"{new_exercise.exercise_name} already exists"
        ):
            await uow.flush()

        return ReturnExerciseSchema.model_validate(updated_exercise)

    async def delete_exercise(
        self, uow: UnitOfWork, user: User, exercise_id: int
    ) -> None:
        exercise = await ExercisePolicy.assert_exercise_exists(
            repo=uow.exercises_repo,
            user_id=user.user_id,
            exercise_id=exercise_id,
        )

        uow.exercises_repo.soft_delete_exercise(exercise)


def get_exercises_service() -> ExerciseService:
    return ExerciseService()
