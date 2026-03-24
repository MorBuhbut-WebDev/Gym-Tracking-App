from sqlalchemy import func, select

from app.models import OrderedExerciseModel
from app.repositories.base import BaseRepo
from app.repositories.mixins import ReorderMixin, ShiftIndicesMixin


class OrderedExerciseRepo[Model: OrderedExerciseModel](
    BaseRepo[Model], ReorderMixin, ShiftIndicesMixin
):
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

    async def get_exercise_ids(self, parent_id: int) -> list[int]:
        exercise_ids = (
            (
                await self._session.execute(
                    select(self._model.exercise_id).where(
                        getattr(self._model, self._model.PARENT_ID) == parent_id
                    )
                )
            )
            .scalars()
            .all()
        )
        return list(exercise_ids)
