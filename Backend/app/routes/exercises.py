from fastapi import APIRouter, Depends

from app.schemas import CreateExerciseSchema, UpdateExerciseSchema, ReturnExerciseSchema
from app.dependencies import get_user, get_uow
from app.auth import User
from app.db import UnitOfWork
from app.services import ExerciseService, get_exercises_service

router = APIRouter(prefix="/exercises")


@router.post("/", response_model=ReturnExerciseSchema, status_code=201)
async def create_exercise(
    exercise: CreateExerciseSchema,
    user: User = Depends(get_user),
    uow: UnitOfWork = Depends(get_uow),
    service: ExerciseService = Depends(get_exercises_service),
):
    return await service.create_exercise(exercise, uow, user)


@router.get("/", response_model=list[ReturnExerciseSchema], status_code=200)
async def get_all_exercises(
    user: User = Depends(get_user),
    uow: UnitOfWork = Depends(get_uow),
    service: ExerciseService = Depends(get_exercises_service),
):
    return await service.get_all_exercises(uow, user)


@router.get("/{exercise_id}", response_model=ReturnExerciseSchema, status_code=200)
async def get_exercise(
    exercise_id: int,
    user: User = Depends(get_user),
    uow: UnitOfWork = Depends(get_uow),
    service: ExerciseService = Depends(get_exercises_service),
):
    return await service.get_exercise(uow, user, exercise_id)


@router.put("/{exercise_id}", response_model=ReturnExerciseSchema, status_code=200)
async def update_exercise(
    exercise_id: int,
    new_exercise: UpdateExerciseSchema,
    user: User = Depends(get_user),
    uow: UnitOfWork = Depends(get_uow),
    service: ExerciseService = Depends(get_exercises_service),
):
    return await service.update_exercise(uow, user, exercise_id, new_exercise)


@router.delete("/{exercise_id}", status_code=204)
async def delete_exercise(
    exercise_id: int,
    user: User = Depends(get_user),
    uow: UnitOfWork = Depends(get_uow),
    service: ExerciseService = Depends(get_exercises_service),
):
    return await service.delete_exercise(uow, user, exercise_id)
