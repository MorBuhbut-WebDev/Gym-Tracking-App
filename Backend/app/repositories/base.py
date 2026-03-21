from pydantic import BaseModel
from sqlalchemy import ColumnElement, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import Base


class BaseRepo[Model: Base]:
    def __init__(self, model: type[Model], session: AsyncSession) -> None:
        self._model = model
        self._session = session

    async def _execute_query(self, condition: ColumnElement[bool]):
        query = select(self._model).where(condition)
        return await self._session.execute(query)

    def add(self, obj: Model) -> Model:
        self._session.add(obj)
        return obj

    async def get_all(self, condition: ColumnElement[bool]) -> list[Model]:
        result = await self._execute_query(condition)
        return list(result.scalars().all())

    async def get(self, condition: ColumnElement[bool]) -> Model | None:
        result = await self._execute_query(condition)
        return result.scalar_one_or_none()

    def update(self, old: Model, updated: BaseModel) -> Model:
        for col, value in updated.model_dump(exclude_unset=True).items():
            if hasattr(old, col):
                setattr(old, col, value)
        return old

    async def delete(self, obj: Model) -> None:
        await self._session.delete(obj)
