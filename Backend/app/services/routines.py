from app.schemas import RoutineCreate, RoutineResponse
from app.auth import User
from app.db import UnitOfWork, catch_unique_violation
from app.policies import RoutinePolicy
from app.models import Routine


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
