from fastapi import APIRouter, Depends

from app.schemas import (
    AddRoutineExerciseSchema,
    UpdateRoutineExerciseSchema,
    ReOrderSchema,
    ReturnRoutineExerciseSchema,
)
from app.dependencies import get_user, get_uow
from app.auth import User
from app.db import UnitOfWork
from app.services import RoutineService, get_routines_service

router = APIRouter(prefix="/{routine_id}/exercises")


@router.post(
    "/{exercise_id}", response_model=ReturnRoutineExerciseSchema, status_code=201
)
async def add_exercise(
    routine_id: int,
    exercise_id: int,
    exercise: AddRoutineExerciseSchema,
    user: User = Depends(get_user),
    uow: UnitOfWork = Depends(get_uow),
    service: RoutineService = Depends(get_routines_service),
):
    return await service.add_exercise(uow, user, routine_id, exercise_id, exercise)


@router.get("/", response_model=list[ReturnRoutineExerciseSchema], status_code=200)
async def get_all_exercises(
    routine_id: int,
    user: User = Depends(get_user),
    uow: UnitOfWork = Depends(get_uow),
    service: RoutineService = Depends(get_routines_service),
):
    return await service.get_all_exercises(uow, user, routine_id)


@router.get(
    "/{exercise_id}", response_model=ReturnRoutineExerciseSchema, status_code=200
)
async def get_exercise(
    routine_id: int,
    exercise_id: int,
    user: User = Depends(get_user),
    uow: UnitOfWork = Depends(get_uow),
    service: RoutineService = Depends(get_routines_service),
):
    return await service.get_exercise(uow, user, routine_id, exercise_id)


@router.patch(
    "/{exercise_id}", response_model=ReturnRoutineExerciseSchema, status_code=200
)
async def update_exercise(
    routine_id: int,
    exercise_id: int,
    updated_exercise: UpdateRoutineExerciseSchema,
    user: User = Depends(get_user),
    uow: UnitOfWork = Depends(get_uow),
    service: RoutineService = Depends(get_routines_service),
):
    return await service.update_exercise(
        uow, user, routine_id, exercise_id, updated_exercise
    )


@router.delete("/{exercise_id}", response_model=None, status_code=204)
async def delete_exercise(
    routine_id: int,
    exercise_id: int,
    user: User = Depends(get_user),
    uow: UnitOfWork = Depends(get_uow),
    service: RoutineService = Depends(get_routines_service),
):
    await service.delete_exercise(uow, user, routine_id, exercise_id)


@router.put("/", response_model=list[ReturnRoutineExerciseSchema], status_code=200)
async def reorder_exercises(
    routine_id: int,
    reordered_schema: ReOrderSchema,
    user: User = Depends(get_user),
    uow: UnitOfWork = Depends(get_uow),
    service: RoutineService = Depends(get_routines_service),
):
    return await service.reorder_exercises(uow, user, routine_id, reordered_schema)
