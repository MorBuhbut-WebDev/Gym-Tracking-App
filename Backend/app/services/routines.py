from app.schemas import (
    CreateRoutineSchema,
    UpdateRoutineSchema,
    ReturnRoutineSchema,
    AddRoutineExerciseSchema,
    UpdateRoutineExerciseSchema,
    ReOrderSchema,
    ReturnRoutineExerciseSchema,
)
from app.auth import User
from app.db import UnitOfWork, catch_unique_violation
from app.policies import RoutinePolicy, RoutineExercisePolicy


class RoutineService:
    async def create_routine(
        self, routine: CreateRoutineSchema, uow: UnitOfWork, user: User
    ) -> ReturnRoutineSchema:
        await RoutinePolicy.assert_name_is_unique(
            repo=uow.routines_repo,
            user_id=user.user_id,
            routine_name=routine.routine_name,
        )

        db_routine = uow.routines_repo.add_routine(routine, user.user_id)

        async with catch_unique_violation(f"{routine.routine_name} already exists"):
            await uow.flush()

        return ReturnRoutineSchema.model_validate(db_routine)

    async def get_all_routines(
        self, uow: UnitOfWork, user: User
    ) -> list[ReturnRoutineSchema]:
        routines = await uow.routines_repo.get_all_routines(user.user_id)

        return [
            ReturnRoutineSchema.model_validate(db_routine) for db_routine in routines
        ]

    async def get_routine(
        self, uow: UnitOfWork, user: User, routine_id: int
    ) -> ReturnRoutineSchema:
        routine = await RoutinePolicy.assert_routine_exist(
            repo=uow.routines_repo,
            user_id=user.user_id,
            routine_id=routine_id,
        )
        return ReturnRoutineSchema.model_validate(routine)

    async def update_routine(
        self,
        uow: UnitOfWork,
        user: User,
        routine_id: int,
        new_routine: UpdateRoutineSchema,
    ) -> ReturnRoutineSchema:
        routine = await RoutinePolicy.assert_routine_exist(
            repo=uow.routines_repo,
            user_id=user.user_id,
            routine_id=routine_id,
        )

        await RoutinePolicy.assert_name_is_unique(
            repo=uow.routines_repo,
            user_id=user.user_id,
            routine_name=new_routine.routine_name,
            routine_id=routine_id,
        )

        updated_routine = uow.routines_repo.update(old=routine, updated=new_routine)

        async with catch_unique_violation(
            f"{updated_routine.routine_name} already exists"
        ):
            await uow.flush()

        return ReturnRoutineSchema.model_validate(updated_routine)

    async def delete_routine(
        self, uow: UnitOfWork, user: User, routine_id: int
    ) -> None:
        routine = await RoutinePolicy.assert_routine_exist(
            repo=uow.routines_repo,
            user_id=user.user_id,
            routine_id=routine_id,
        )

        await uow.routines_repo.delete(routine)

    async def add_exercise(
        self,
        uow: UnitOfWork,
        user: User,
        routine_id: int,
        exercise_id: int,
        exercise: AddRoutineExerciseSchema,
    ) -> ReturnRoutineExerciseSchema:
        await RoutineExercisePolicy.assert_routine_and_exercise_accessible(
            exercises_repo=uow.exercises_repo,
            routines_repo=uow.routines_repo,
            user_id=user.user_id,
            routine_id=routine_id,
            exercise_id=exercise_id,
        )

        await RoutineExercisePolicy.assert_exercise_not_exist(
            repo=uow.routines_exercises_repo,
            routine_id=routine_id,
            exercise_id=exercise_id,
        )

        await RoutineExercisePolicy.assert_exercise_index_is_unique(
            repo=uow.routines_exercises_repo,
            routine_id=routine_id,
            exercise_index=exercise.exercise_index,
        )

        routine_exercise = uow.routines_exercises_repo.add_exercise_to_routine(
            routine_id,
            exercise_id,
            exercise,
        )

        async with catch_unique_violation(
            f"Exercise with position {exercise.exercise_index} already exists!"
        ):
            await uow.flush()

        return ReturnRoutineExerciseSchema.model_validate(routine_exercise)

    async def get_all_exercises(
        self, uow: UnitOfWork, user: User, routine_id: int
    ) -> list[ReturnRoutineExerciseSchema]:
        await RoutinePolicy.assert_routine_exist(
            repo=uow.routines_repo,
            user_id=user.user_id,
            routine_id=routine_id,
        )

        exercises = await uow.routines_exercises_repo.get_all_exercises_from_routine(
            routine_id
        )

        return [
            ReturnRoutineExerciseSchema.model_validate(exercise)
            for exercise in exercises
        ]

    async def get_exercise(
        self, uow: UnitOfWork, user: User, routine_id: int, exercise_id: int
    ) -> ReturnRoutineExerciseSchema:
        _, routine_exercise = await RoutineExercisePolicy.assert_link_accessible(
            routines_repo=uow.routines_repo,
            routines_exercises_repo=uow.routines_exercises_repo,
            user_id=user.user_id,
            routine_id=routine_id,
            exercise_id=exercise_id,
        )

        return ReturnRoutineExerciseSchema.model_validate(routine_exercise)

    async def update_exercise(
        self,
        uow: UnitOfWork,
        user: User,
        routine_id: int,
        exercise_id: int,
        updated_exercise: UpdateRoutineExerciseSchema,
    ) -> ReturnRoutineExerciseSchema:
        _, routine_exercise = await RoutineExercisePolicy.assert_link_accessible(
            routines_repo=uow.routines_repo,
            routines_exercises_repo=uow.routines_exercises_repo,
            user_id=user.user_id,
            routine_id=routine_id,
            exercise_id=exercise_id,
        )

        db_routine_exercise = uow.routines_exercises_repo.update(
            old=routine_exercise, updated=updated_exercise
        )

        return ReturnRoutineExerciseSchema.model_validate(db_routine_exercise)

    async def delete_exercise(
        self, uow: UnitOfWork, user: User, routine_id: int, exercise_id: int
    ) -> None:
        _, routine_exercise = await RoutineExercisePolicy.assert_link_accessible(
            routines_repo=uow.routines_repo,
            routines_exercises_repo=uow.routines_exercises_repo,
            user_id=user.user_id,
            routine_id=routine_id,
            exercise_id=exercise_id,
        )

        await uow.routines_exercises_repo.delete(routine_exercise)

    async def reorder_exercises(
        self,
        uow: UnitOfWork,
        user: User,
        routine_id: int,
        reordered_schema: ReOrderSchema,
    ) -> list[ReturnRoutineExerciseSchema]:
        await RoutinePolicy.assert_routine_exist(
            repo=uow.routines_repo, user_id=user.user_id, routine_id=routine_id
        )

        await RoutineExercisePolicy.assert_submitted_exercises_valid(
            repo=uow.routines_exercises_repo,
            routine_id=routine_id,
            reordered_schema=reordered_schema,
        )

        reordered = await uow.routines_exercises_repo.reorder_exercises(
            routine_id, reordered_schema
        )

        return [
            ReturnRoutineExerciseSchema.model_validate(exercise)
            for exercise in reordered
        ]


def get_routines_service() -> RoutineService:
    return RoutineService()
