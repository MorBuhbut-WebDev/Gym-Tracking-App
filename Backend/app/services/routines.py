from app.auth import User
from app.db import UnitOfWork, catch_unique_violation
from app.models import Routine
from app.policies import RoutineExercisePolicy, RoutinePolicy
from app.schemas import (
    ExerciseReorder,
    RoutineAddExercise,
    RoutineCreate,
    RoutineExerciseResponse,
    RoutineResponse,
    RoutineUpdate,
    RoutineUpdateExercise,
)


class RoutineService:
    async def create(
        self, uow: UnitOfWork, user: User, payload: RoutineCreate
    ) -> RoutineResponse:
        await RoutinePolicy.assert_name_is_unique(
            repo=uow.routines_repo,
            user_id=user.user_id,
            routine_name=payload.routine_name,
        )

        routine = uow.routines_repo.add(
            Routine.create(routine_name=payload.routine_name, user_id=user.user_id)
        )

        async with catch_unique_violation(f"{payload.routine_name} already exists"):
            await uow.flush()

        return RoutineResponse.model_validate(routine)

    async def get_all(self, uow: UnitOfWork, user: User) -> list[RoutineResponse]:
        routines = await uow.routines_repo.get_all(user.user_id)
        return [RoutineResponse.model_validate(routine) for routine in routines]

    async def get(
        self, uow: UnitOfWork, user: User, routine_id: int
    ) -> RoutineResponse:
        routine = await RoutinePolicy.assert_exists(
            repo=uow.routines_repo,
            user_id=user.user_id,
            routine_id=routine_id,
        )
        return RoutineResponse.model_validate(routine)

    async def update(
        self,
        uow: UnitOfWork,
        user: User,
        routine_id: int,
        payload: RoutineUpdate,
    ) -> RoutineResponse:
        routine = await RoutinePolicy.assert_exists(
            repo=uow.routines_repo,
            user_id=user.user_id,
            routine_id=routine_id,
        )

        await RoutinePolicy.assert_name_is_unique(
            repo=uow.routines_repo,
            user_id=user.user_id,
            routine_name=payload.routine_name,
            routine_id=routine_id,
        )

        routine = uow.routines_repo.update(old=routine, updated=payload)

        async with catch_unique_violation(f"{payload.routine_name} already exists"):
            await uow.flush()

        return RoutineResponse.model_validate(routine)

    async def delete(self, uow: UnitOfWork, user: User, routine_id: int) -> None:
        routine = await RoutinePolicy.assert_exists(
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
        payload: RoutineAddExercise,
    ) -> RoutineExerciseResponse:
        await RoutineExercisePolicy.assert_accessible(
            exercises_repo=uow.exercises_repo,
            routines_repo=uow.routines_repo,
            user_id=user.user_id,
            routine_id=routine_id,
            exercise_id=exercise_id,
        )

        await RoutineExercisePolicy.assert_not_linked(
            repo=uow.routines_exercises_repo,
            routine_id=routine_id,
            exercise_id=exercise_id,
        )

        routine_exercise = await uow.routines_exercises_repo.add_exercise(
            routine_id,
            exercise_id,
            payload,
        )

        await uow.flush()

        return RoutineExerciseResponse.model_validate(routine_exercise)

    async def get_all_exercises(
        self, uow: UnitOfWork, user: User, routine_id: int
    ) -> list[RoutineExerciseResponse]:
        await RoutinePolicy.assert_exists(
            repo=uow.routines_repo,
            user_id=user.user_id,
            routine_id=routine_id,
        )

        exercises = await uow.routines_exercises_repo.get_all(routine_id)

        return [
            RoutineExerciseResponse.model_validate(exercise) for exercise in exercises
        ]

    async def get_exercise(
        self, uow: UnitOfWork, user: User, routine_id: int, exercise_id: int
    ) -> RoutineExerciseResponse:
        _, routine_exercise = await RoutineExercisePolicy.assert_link_exists(
            routines_repo=uow.routines_repo,
            routines_exercises_repo=uow.routines_exercises_repo,
            user_id=user.user_id,
            routine_id=routine_id,
            exercise_id=exercise_id,
        )

        return RoutineExerciseResponse.model_validate(routine_exercise)

    async def update_exercise(
        self,
        uow: UnitOfWork,
        user: User,
        routine_id: int,
        exercise_id: int,
        payload: RoutineUpdateExercise,
    ) -> RoutineExerciseResponse:
        _, routine_exercise = await RoutineExercisePolicy.assert_link_exists(
            routines_repo=uow.routines_repo,
            routines_exercises_repo=uow.routines_exercises_repo,
            user_id=user.user_id,
            routine_id=routine_id,
            exercise_id=exercise_id,
        )

        routine_exercise = uow.routines_exercises_repo.update(
            old=routine_exercise, updated=payload
        )

        return RoutineExerciseResponse.model_validate(routine_exercise)

    async def delete_exercise(
        self, uow: UnitOfWork, user: User, routine_id: int, exercise_id: int
    ) -> None:
        _, routine_exercise = await RoutineExercisePolicy.assert_link_exists(
            routines_repo=uow.routines_repo,
            routines_exercises_repo=uow.routines_exercises_repo,
            user_id=user.user_id,
            routine_id=routine_id,
            exercise_id=exercise_id,
        )

        await uow.routines_exercises_repo.delete(routine_exercise)
        await uow.flush()
        await uow.routines_exercises_repo.shift_indices_after_delete(
            [routine_id], [routine_exercise.exercise_index]
        )

    async def reorder_exercises(
        self,
        uow: UnitOfWork,
        user: User,
        routine_id: int,
        payload: ExerciseReorder,
    ) -> list[RoutineExerciseResponse]:
        await RoutinePolicy.assert_exists(
            repo=uow.routines_repo, user_id=user.user_id, routine_id=routine_id
        )

        await RoutineExercisePolicy.assert_valid_reorder(
            repo=uow.routines_exercises_repo, routine_id=routine_id, payload=payload
        )

        exercises = await uow.routines_exercises_repo.reorder_exercises(
            routine_id, payload
        )

        return [
            RoutineExerciseResponse.model_validate(exercise) for exercise in exercises
        ]


def get_routines_service() -> RoutineService:
    return RoutineService()
