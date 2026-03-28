from fastapi import APIRouter, Depends

from app.auth import User
from app.db.unit_of_work import UnitOfWork
from app.dependencies import get_uow, get_user
from app.schemas import WorkoutSetCreate, WorkoutSetResponse, WorkoutSetUpdate
from app.services import WorkoutService, get_workouts_service

workouts_sets_router = APIRouter(prefix="/{exercise_id}/sets")


@workouts_sets_router.post("/", response_model=WorkoutSetResponse, status_code=201)
async def add_set(
    workout_id: int,
    exercise_id: int,
    payload: WorkoutSetCreate,
    uow: UnitOfWork = Depends(get_uow),
    user: User = Depends(get_user),
    service: WorkoutService = Depends(get_workouts_service),
) -> WorkoutSetResponse:
    return await service.add_set(uow, user, workout_id, exercise_id, payload)


@workouts_sets_router.delete("/{set_id}", status_code=204)
async def delete_set(
    workout_id: int,
    exercise_id: int,
    set_id: int,
    uow: UnitOfWork = Depends(get_uow),
    user: User = Depends(get_user),
    service: WorkoutService = Depends(get_workouts_service),
) -> None:
    await service.delete_set(uow, user, workout_id, exercise_id, set_id)


@workouts_sets_router.patch("/{set_id}", status_code=204)
async def update_set(
    workout_id: int,
    exercise_id: int,
    set_id: int,
    payload: WorkoutSetUpdate,
    uow: UnitOfWork = Depends(get_uow),
    user: User = Depends(get_user),
    service: WorkoutService = Depends(get_workouts_service),
) -> None:
    return await service.update_set(uow, user, workout_id, exercise_id, set_id, payload)
