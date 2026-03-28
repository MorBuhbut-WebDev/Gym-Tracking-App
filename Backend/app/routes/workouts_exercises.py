from fastapi import APIRouter, Depends

from app.auth import User
from app.db.unit_of_work import UnitOfWork
from app.dependencies import get_uow, get_user
from app.routes.workouts_sets import workouts_sets_router
from app.schemas import ExerciseReorder
from app.services import WorkoutService, get_workouts_service

workouts_exercises_router = APIRouter(prefix="/{workout_id}/exercises")
workouts_exercises_router.include_router(workouts_sets_router)


@workouts_exercises_router.post("/{exercise_id}", status_code=204)
async def add_exercise(
    workout_id: int,
    exercise_id: int,
    uow: UnitOfWork = Depends(get_uow),
    user: User = Depends(get_user),
    service: WorkoutService = Depends(get_workouts_service),
) -> None:
    return await service.add_exercise(uow, user, workout_id, exercise_id)


@workouts_exercises_router.delete("/{exercise_id}", status_code=204)
async def delete_exercise(
    workout_id: int,
    exercise_id: int,
    uow: UnitOfWork = Depends(get_uow),
    user: User = Depends(get_user),
    service: WorkoutService = Depends(get_workouts_service),
) -> None:
    await service.delete_exercise(uow, user, workout_id, exercise_id)


@workouts_exercises_router.put("/", status_code=204)
async def reorder_exercises(
    workout_id: int,
    payload: ExerciseReorder,
    uow: UnitOfWork = Depends(get_uow),
    user: User = Depends(get_user),
    service: WorkoutService = Depends(get_workouts_service),
) -> None:
    return await service.reorder_exercises(uow, user, workout_id, payload)
