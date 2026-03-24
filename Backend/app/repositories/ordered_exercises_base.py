from sqlalchemy import func, select

from app.models import OrderedExerciseModel
from app.repositories.base import BaseRepo


class OrderedExerciseRepo[Model: OrderedExerciseModel](BaseRepo[Model]):
    async def _compute_next_index(self, parent_id: int) -> int:
        result = (
            await self._session.execute(
                select(func.max(self._model.exercise_index)).where(
                    getattr(self._model, self._model.PARENT_ID) == parent_id
                )
            )
        ).scalar()

        if result is not None and not isinstance(result, int):
            raise ValueError(f"Expected an integer result, got {type(result)}")

        return 1 if result is None else result + 1

    async def get_link(
        self,
        parent_id: int,
        exercise_id: int,
    ) -> Model | None:
        result = await self.get(
            condition=(getattr(self._model, self._model.PARENT_ID) == parent_id)
            & (self._model.exercise_id == exercise_id),
        )

        return result
