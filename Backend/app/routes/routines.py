from fastapi import APIRouter, Depends

from app.schemas import CreateRoutineSchema, UpdateRoutineSchema, ReturnRoutineSchema
from app.dependencies import get_user, get_uow
from app.auth import User
from app.db import UnitOfWork
from app.services import RoutineService, get_routines_service
from app.routes.routines_exercises import router as routine_exercise_router

router = APIRouter(prefix="/routines")
router.include_router(routine_exercise_router)


@router.post("/", response_model=ReturnRoutineSchema, status_code=201)
async def create_routine(
    routine: CreateRoutineSchema,
    user: User = Depends(get_user),
    uow: UnitOfWork = Depends(get_uow),
    service: RoutineService = Depends(get_routines_service),
):
    return await service.create_routine(routine, uow, user)


@router.get("/", response_model=list[ReturnRoutineSchema], status_code=200)
async def get_all_routines(
    user: User = Depends(get_user),
    uow: UnitOfWork = Depends(get_uow),
    service: RoutineService = Depends(get_routines_service),
):
    return await service.get_all_routines(uow, user)


@router.get("/{routine_id}", response_model=ReturnRoutineSchema, status_code=200)
async def get_routine(
    routine_id: int,
    user: User = Depends(get_user),
    uow: UnitOfWork = Depends(get_uow),
    service: RoutineService = Depends(get_routines_service),
):
    return await service.get_routine(uow, user, routine_id)


@router.put("/{routine_id}", response_model=ReturnRoutineSchema, status_code=200)
async def update_routine(
    routine_id: int,
    new_routine: UpdateRoutineSchema,
    user: User = Depends(get_user),
    uow: UnitOfWork = Depends(get_uow),
    service: RoutineService = Depends(get_routines_service),
):
    return await service.update_routine(uow, user, routine_id, new_routine)


@router.delete("/{routine_id}", status_code=204)
async def delete_routine(
    routine_id: int,
    user: User = Depends(get_user),
    uow: UnitOfWork = Depends(get_uow),
    service: RoutineService = Depends(get_routines_service),
):
    return await service.delete_routine(uow, user, routine_id)
