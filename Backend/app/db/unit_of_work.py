from typing import Self

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import ExerciseRepo


class UnitOfWork:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._exercises_repo = None

    @property
    def exercises_repo(self) -> ExerciseRepo:
        if self._exercises_repo is None:
            self._exercises_repo = ExerciseRepo(self._session)

        return self._exercises_repo

    async def flush(self) -> None:
        await self._session.flush()

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        if exc:
            await self._session.rollback()
        else:
            await self._session.commit()
