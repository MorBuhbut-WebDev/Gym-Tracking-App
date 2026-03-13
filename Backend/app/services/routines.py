from app.auth import User
from app.db import UnitOfWork, catch_unique_violation
from app.models import Routine
from app.policies import RoutinePolicy
from app.schemas import RoutineCreate, RoutineResponse, RoutineUpdate


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


def get_routines_service() -> RoutineService:
    return RoutineService()
