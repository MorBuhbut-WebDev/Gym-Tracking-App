from typing import cast

from sqlalchemy import RowMapping, text

from app.repositories.mixins.base import HasSessionAndModel
from app.schemas import ExerciseReorder


class ReorderMixin(HasSessionAndModel):
    async def reorder_exercises(
        self, parent_id: int, payload: ExerciseReorder
    ) -> list[RowMapping]:
        await self._session.execute(
            text(f"SET CONSTRAINTS {self._model.EXERCISE_INDEX_CONSTRAINT} DEFERRED")
        )
        exercises = payload.unzip()
        result = await self._session.execute(
            text(
                f"""
            UPDATE {self._model.__tablename__} t
            SET exercise_index = r.exercise_index
            FROM unnest((:exercise_ids)::INT[], (:exercise_indices)::INT[]) r(exercise_id, exercise_index)
            WHERE t.exercise_id = r.exercise_id
              AND t.{self._model.PARENT_ID} = :parent_id
            RETURNING t.*
            """
            ),
            {
                "exercise_ids": exercises.exercise_ids,
                "exercise_indices": exercises.exercise_indices,
                "parent_id": parent_id,
            },
        )
        return cast(list[RowMapping], result.mappings().fetchall())
