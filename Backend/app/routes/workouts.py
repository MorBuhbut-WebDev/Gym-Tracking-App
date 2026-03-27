from fastapi import APIRouter, Depends

from app.auth import User
from app.db import UnitOfWork
from app.dependencies import get_uow, get_user, get_workout_filters
from app.routes.workouts_exercises import workouts_exercises_router
from app.schemas import (
    WorkoutCreate,
    WorkoutFilters,
    WorkoutNested,
    WorkoutResponse,
    WorkoutUpdate,
)
from app.services import WorkoutService, get_workouts_service

workouts_router = APIRouter(prefix="/workouts")
workouts_router.include_router(workouts_exercises_router)


@workouts_router.post("/", response_model=WorkoutResponse, status_code=201)
async def start_workout(
    payload: WorkoutCreate,
    uow: UnitOfWork = Depends(get_uow),
    user: User = Depends(get_user),
    service: WorkoutService = Depends(get_workouts_service),
) -> WorkoutResponse:
    return await service.create(uow, user, payload)


@workouts_router.get("/", response_model=list[WorkoutResponse])
async def get_all_workouts(
    filters: WorkoutFilters = Depends(get_workout_filters),
    uow: UnitOfWork = Depends(get_uow),
    user: User = Depends(get_user),
    service: WorkoutService = Depends(get_workouts_service),
) -> list[WorkoutResponse]:
    return await service.get_all(uow, user, filters)


@workouts_router.get("/{workout_id}", response_model=WorkoutNested)
async def get_workout(
    workout_id: int,
    uow: UnitOfWork = Depends(get_uow),
    user: User = Depends(get_user),
    service: WorkoutService = Depends(get_workouts_service),
) -> WorkoutNested:
    return await service.get(uow, user, workout_id)


@workouts_router.patch("/{workout_id}", status_code=204)
async def update_workout(
    workout_id: int,
    payload: WorkoutUpdate,
    uow: UnitOfWork = Depends(get_uow),
    user: User = Depends(get_user),
    service: WorkoutService = Depends(get_workouts_service),
) -> None:
    return await service.update(uow, user, workout_id, payload)


@workouts_router.delete("/{workout_id}", status_code=204)
async def delete_workout(
    workout_id: int,
    uow: UnitOfWork = Depends(get_uow),
    user: User = Depends(get_user),
    service: WorkoutService = Depends(get_workouts_service),
) -> None:
    await service.delete(uow, user, workout_id)
