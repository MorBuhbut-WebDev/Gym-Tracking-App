from typing import Protocol

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import OrderedExerciseModel


class HasSessionAndModel(Protocol):
    _session: AsyncSession
    _model: type[OrderedExerciseModel]
