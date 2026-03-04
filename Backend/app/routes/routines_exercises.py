from fastapi import APIRouter, Depends

from app.schemas import (
    RoutineAddExercise,
    RoutineUpdateExercise,
    ExerciseReorder,
    RoutineExerciseResponse,
)
from app.dependencies import get_user, get_uow
from app.auth import User
from app.db import UnitOfWork
from app.services import RoutineService, get_routines_service

routine_exercise_router = APIRouter(prefix="/{routine_id}/exercises")


@routine_exercise_router.post(
    "/{exercise_id}", response_model=RoutineExerciseResponse, status_code=201
)
async def add_exercise(
    routine_id: int,
    exercise_id: int,
    payload: RoutineAddExercise,
    uow: UnitOfWork = Depends(get_uow),
    user: User = Depends(get_user),
    service: RoutineService = Depends(get_routines_service),
):
    return await service.add_exercise(uow, user, routine_id, exercise_id, payload)


@routine_exercise_router.get("/", response_model=list[RoutineExerciseResponse])
async def get_all_exercises(
    routine_id: int,
    uow: UnitOfWork = Depends(get_uow),
    user: User = Depends(get_user),
    service: RoutineService = Depends(get_routines_service),
):
    return await service.get_all_exercises(uow, user, routine_id)


@routine_exercise_router.get("/{exercise_id}", response_model=RoutineExerciseResponse)
async def get_exercise(
    routine_id: int,
    exercise_id: int,
    uow: UnitOfWork = Depends(get_uow),
    user: User = Depends(get_user),
    service: RoutineService = Depends(get_routines_service),
):
    return await service.get_exercise(uow, user, routine_id, exercise_id)


@routine_exercise_router.put("/", response_model=list[RoutineExerciseResponse])
async def reorder_exercises(
    routine_id: int,
    payload: ExerciseReorder,
    uow: UnitOfWork = Depends(get_uow),
    user: User = Depends(get_user),
    service: RoutineService = Depends(get_routines_service),
):
    return await service.reorder_exercises(uow, user, routine_id, payload)


@routine_exercise_router.patch("/{exercise_id}", response_model=RoutineExerciseResponse)
async def update_exercise(
    routine_id: int,
    exercise_id: int,
    payload: RoutineUpdateExercise,
    uow: UnitOfWork = Depends(get_uow),
    user: User = Depends(get_user),
    service: RoutineService = Depends(get_routines_service),
):
    return await service.update_exercise(uow, user, routine_id, exercise_id, payload)


@routine_exercise_router.delete("/{exercise_id}", status_code=204)
async def delete_exercise(
    routine_id: int,
    exercise_id: int,
    uow: UnitOfWork = Depends(get_uow),
    user: User = Depends(get_user),
    service: RoutineService = Depends(get_routines_service),
):
    await service.delete_exercise(uow, user, routine_id, exercise_id)
