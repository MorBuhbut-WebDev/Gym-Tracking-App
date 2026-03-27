from fastapi import APIRouter, Depends

from app.auth import User
from app.db.unit_of_work import UnitOfWork
from app.dependencies import get_uow, get_user
from app.schemas import (
    ExerciseReorder,
    RoutineAddExercise,
    RoutineExerciseResponse,
    RoutineUpdateExercise,
)
from app.services import RoutineService, get_routines_service

routine_exercise_router = APIRouter(prefix="/{routine_id}/exercises")


@routine_exercise_router.post("/{exercise_id}", status_code=204)
async def add_exercise(
    routine_id: int,
    exercise_id: int,
    payload: RoutineAddExercise,
    uow: UnitOfWork = Depends(get_uow),
    user: User = Depends(get_user),
    service: RoutineService = Depends(get_routines_service),
) -> None:
    return await service.add_exercise(uow, user, routine_id, exercise_id, payload)


@routine_exercise_router.get("/{exercise_id}", response_model=RoutineExerciseResponse)
async def get_exercise(
    routine_id: int,
    exercise_id: int,
    uow: UnitOfWork = Depends(get_uow),
    user: User = Depends(get_user),
    service: RoutineService = Depends(get_routines_service),
) -> RoutineExerciseResponse:
    return await service.get_exercise(uow, user, routine_id, exercise_id)


@routine_exercise_router.put("/", status_code=204)
async def reorder_exercises(
    routine_id: int,
    payload: ExerciseReorder,
    uow: UnitOfWork = Depends(get_uow),
    user: User = Depends(get_user),
    service: RoutineService = Depends(get_routines_service),
) -> None:
    return await service.reorder_exercises(uow, user, routine_id, payload)


@routine_exercise_router.patch("/{exercise_id}", status_code=204)
async def update_exercise(
    routine_id: int,
    exercise_id: int,
    payload: RoutineUpdateExercise,
    uow: UnitOfWork = Depends(get_uow),
    user: User = Depends(get_user),
    service: RoutineService = Depends(get_routines_service),
) -> None:
    return await service.update_exercise(uow, user, routine_id, exercise_id, payload)


@routine_exercise_router.delete("/{exercise_id}", status_code=204)
async def delete_exercise(
    routine_id: int,
    exercise_id: int,
    uow: UnitOfWork = Depends(get_uow),
    user: User = Depends(get_user),
    service: RoutineService = Depends(get_routines_service),
) -> None:
    await service.delete_exercise(uow, user, routine_id, exercise_id)
