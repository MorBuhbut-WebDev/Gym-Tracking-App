from typing import Self

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import (
    ExerciseRepo,
    RoutineExerciseRepo,
    RoutineRepo,
    WorkoutExerciseRepo,
    WorkoutRepo,
    WorkoutSetRepo,
)


class UnitOfWork:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._exercises_repo = None
        self._routines_repo = None
        self._routines_exercises_repo = None
        self._workouts_repo = None
        self._workouts_exercises_repo = None
        self._workouts_sets_repo = None

    @property
    def exercises_repo(self) -> ExerciseRepo:
        if self._exercises_repo is None:
            self._exercises_repo = ExerciseRepo(self._session)

        return self._exercises_repo

    @property
    def routines_repo(self) -> RoutineRepo:
        if self._routines_repo is None:
            self._routines_repo = RoutineRepo(self._session)
        return self._routines_repo

    @property
    def routines_exercises_repo(self) -> RoutineExerciseRepo:
        if self._routines_exercises_repo is None:
            self._routines_exercises_repo = RoutineExerciseRepo(self._session)

        return self._routines_exercises_repo

    @property
    def workouts_repo(self) -> WorkoutRepo:
        if self._workouts_repo is None:
            self._workouts_repo = WorkoutRepo(self._session)

        return self._workouts_repo

    @property
    def workouts_exercises_repo(self) -> WorkoutExerciseRepo:
        if self._workouts_exercises_repo is None:
            self._workouts_exercises_repo = WorkoutExerciseRepo(self._session)

        return self._workouts_exercises_repo

    @property
    def workouts_sets_repo(self) -> WorkoutSetRepo:
        if self._workouts_sets_repo is None:
            self._workouts_sets_repo = WorkoutSetRepo(self._session)

        return self._workouts_sets_repo

    async def flush(self) -> None:
        await self._session.flush()

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        if exc:
            await self._session.rollback()
        else:
            await self._session.commit()
