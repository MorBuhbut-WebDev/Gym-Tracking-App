from fastapi import APIRouter, Depends

from app.schemas import ExerciseCreate, ExerciseUpdate, ExerciseResponse
from app.dependencies import get_user, get_uow
from app.auth import User
from app.db import UnitOfWork
from app.services import ExerciseService, get_exercises_service

exercises_router = APIRouter(prefix="/exercises")


@exercises_router.post("/", response_model=ExerciseResponse, status_code=201)
async def create_exercise(
    payload: ExerciseCreate,
    uow: UnitOfWork = Depends(get_uow),
    user: User = Depends(get_user),
    service: ExerciseService = Depends(get_exercises_service),
) -> ExerciseResponse:
    return await service.create(uow, user, payload)


@exercises_router.get("/", response_model=list[ExerciseResponse])
async def get_all_exercises(
    uow: UnitOfWork = Depends(get_uow),
    user: User = Depends(get_user),
    service: ExerciseService = Depends(get_exercises_service),
) -> list[ExerciseResponse]:
    return await service.get_all(uow, user)


@exercises_router.get("/{exercise_id}", response_model=ExerciseResponse)
async def get_exercise(
    exercise_id: int,
    uow: UnitOfWork = Depends(get_uow),
    user: User = Depends(get_user),
    service: ExerciseService = Depends(get_exercises_service),
) -> ExerciseResponse:
    return await service.get(uow, user, exercise_id)


@exercises_router.put("/{exercise_id}", response_model=ExerciseResponse)
async def update_exercise(
    exercise_id: int,
    payload: ExerciseUpdate,
    uow: UnitOfWork = Depends(get_uow),
    user: User = Depends(get_user),
    service: ExerciseService = Depends(get_exercises_service),
) -> ExerciseResponse:
    return await service.update(uow, user, exercise_id, payload)


@exercises_router.delete("/{exercise_id}", status_code=204)
async def delete_exercise(
    exercise_id: int,
    uow: UnitOfWork = Depends(get_uow),
    user: User = Depends(get_user),
    service: ExerciseService = Depends(get_exercises_service),
) -> None:
    await service.delete(uow, user, exercise_id)
