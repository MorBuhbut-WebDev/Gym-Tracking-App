from typing import Generic, TypeVar, Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, BinaryExpression, func
from pydantic import BaseModel

from app.db import Base


Model = TypeVar("Model", bound=Base)
Schema = TypeVar("Schema", bound=BaseModel)


class BaseRepo(Generic[Model]):
    def __init__(self, model: Type[Model], session: AsyncSession) -> None:
        self._model = model
        self._session = session

    async def _execute_query(self, condition: BinaryExpression):
        query = select(self._model).where(condition)
        return await self._session.execute(query)

    def add(self, obj: Model):
        self._session.add(obj)
        return obj

    async def get_all(self, condition: BinaryExpression):
        result = await self._execute_query(condition)
        return result.scalars().all()

    # async def count_all(self, condition: BinaryExpression):
    #     count = (
    #         await self._session.execute(
    #             select(func.count()).select_from(self._model).where(condition)
    #         )
    #     ).scalar()
    #     return count if count is not None else 0

    async def get(self, condition: BinaryExpression):
        result = await self._execute_query(condition)
        return result.scalar_one_or_none()

    def update(self, old: Model, updated: Schema):
        for col, value in updated.model_dump(exclude_unset=True).items():
            if hasattr(old, col):
                setattr(old, col, value)
        return old

    async def delete(self, obj: Model):
        await self._session.delete(obj)
