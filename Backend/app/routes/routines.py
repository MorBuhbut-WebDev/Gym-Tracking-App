from fastapi import APIRouter, Depends

from app.auth import User
from app.db import UnitOfWork
from app.dependencies import get_uow, get_user
from app.routes.routines_exercises import routine_exercise_router
from app.schemas import RoutineCreate, RoutineResponse, RoutineUpdate
from app.services import RoutineService, get_routines_service

routines_router = APIRouter(prefix="/routines")
routines_router.include_router(routine_exercise_router)


@routines_router.post("/", response_model=RoutineResponse, status_code=201)
async def create_routine(
    payload: RoutineCreate,
    uow: UnitOfWork = Depends(get_uow),
    user: User = Depends(get_user),
    service: RoutineService = Depends(get_routines_service),
):
    return await service.create(uow, user, payload)


@routines_router.get("/", response_model=list[RoutineResponse])
async def get_all_routines(
    uow: UnitOfWork = Depends(get_uow),
    user: User = Depends(get_user),
    service: RoutineService = Depends(get_routines_service),
):
    return await service.get_all(uow, user)


@routines_router.get("/{routine_id}", response_model=RoutineResponse)
async def get_routine(
    routine_id: int,
    uow: UnitOfWork = Depends(get_uow),
    user: User = Depends(get_user),
    service: RoutineService = Depends(get_routines_service),
):
    return await service.get(uow, user, routine_id)


@routines_router.put("/{routine_id}", response_model=RoutineResponse)
async def update_routine(
    routine_id: int,
    payload: RoutineUpdate,
    uow: UnitOfWork = Depends(get_uow),
    user: User = Depends(get_user),
    service: RoutineService = Depends(get_routines_service),
):
    return await service.update(uow, user, routine_id, payload)


@routines_router.delete("/{routine_id}", status_code=204)
async def delete_routine(
    routine_id: int,
    uow: UnitOfWork = Depends(get_uow),
    user: User = Depends(get_user),
    service: RoutineService = Depends(get_routines_service),
):
    await service.delete(uow, user, routine_id)
