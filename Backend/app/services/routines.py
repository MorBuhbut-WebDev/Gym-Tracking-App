from app.auth import User
from app.db import UnitOfWork, catch_unique_violation
from app.models import Routine
from app.policies import RoutinePolicy
from app.schemas import RoutineCreate, RoutineResponse


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
