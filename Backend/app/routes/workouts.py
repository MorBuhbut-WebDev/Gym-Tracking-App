from fastapi import APIRouter, Depends

from app.schemas import WorkoutCreate, WorkoutNested
from app.dependencies import get_user, get_uow
from app.auth import User
from app.db import UnitOfWork
from app.services import WorkoutService, get_workouts_service

workouts_router = APIRouter(prefix="/workouts")


@workouts_router.post("/", response_model=WorkoutNested, status_code=201)
async def create_workout(
    payload: WorkoutCreate,
    uow: UnitOfWork = Depends(get_uow),
    user: User = Depends(get_user),
    service: WorkoutService = Depends(get_workouts_service),
):
    return await service.create(uow, user, payload)
