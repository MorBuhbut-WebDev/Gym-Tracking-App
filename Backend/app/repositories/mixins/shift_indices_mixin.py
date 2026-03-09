from typing import Protocol, Type

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import HasParentID


class HasSessionAndModel(Protocol):
    _session: AsyncSession
    _model: Type[HasParentID]


class ShiftIndicesMixin(HasSessionAndModel):
    async def shift_indices_after_delete(
        self, parent_ids: list[int], deleted_indices: list[int]
    ) -> None:
        await self._session.execute(
            text(
                f"""
            UPDATE {self._model.__tablename__} t
            SET exercise_index = t.exercise_index - 1
            FROM unnest((:parent_ids)::INT[], (:deleted_indices)::INT[]) v(parent_id, deleted_index)
            WHERE t.{self._model.PARENT_ID} = v.parent_id
              AND t.exercise_index > v.deleted_index
            """
            ),
            {"parent_ids": parent_ids, "deleted_indices": deleted_indices},
        )
