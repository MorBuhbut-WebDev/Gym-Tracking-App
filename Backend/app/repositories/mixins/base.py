from typing import Protocol, Type

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import HasParentID


class HasSessionAndModel(Protocol):
    _session: AsyncSession
    _model: Type[HasParentID]
