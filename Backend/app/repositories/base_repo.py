from typing import Generic, Optional, Type, TypeVar, cast

from pydantic import BaseModel
from sqlalchemy import BinaryExpression, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import Base

Model = TypeVar("Model", bound=Base)


class BaseRepo(Generic[Model]):
    def __init__(self, model: Type[Model], session: AsyncSession) -> None:
        self._model = model
        self._session = session

    async def _execute_query(self, condition: BinaryExpression):
        query = select(self._model).where(condition)
        return await self._session.execute(query)

    def add(self, obj: Model) -> Model:
        self._session.add(obj)
        return obj

    async def get_all(self, condition: BinaryExpression) -> list[Model]:
        result = await self._execute_query(condition)
        return cast(list[Model], result.scalars().all())

    async def get(self, condition: BinaryExpression) -> Optional[Model]:
        result = await self._execute_query(condition)
        return result.scalar_one_or_none()

    def update(self, old: Model, updated: BaseModel) -> Model:
        for col, value in updated.model_dump(exclude_unset=True).items():
            if hasattr(old, col):
                setattr(old, col, value)
        return old

    async def delete(self, obj: Model) -> None:
        await self._session.delete(obj)
