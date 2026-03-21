from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import WorkoutExercise
from app.repositories.ordered_exercises_base import OrderedExerciseRepo


class WorkoutExerciseRepo(OrderedExerciseRepo[WorkoutExercise]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(model=WorkoutExercise, session=session)

    async def add_exercise(self, workout_id: int, exercise_id: int) -> WorkoutExercise:
        max_exercise_index = await self._compute_next_index(workout_id)

        workout_exercise = self.add(
            WorkoutExercise.create(
                workout_id=workout_id,
                exercise_id=exercise_id,
                exercise_index=max_exercise_index,
            )
        )
        return workout_exercise

    async def get_link(
        self,
        workout_id: int,
        exercise_id: int,
    ) -> WorkoutExercise | None:
        workout_exercise = await self.get(
            condition=(WorkoutExercise.workout_id == workout_id)
            & (WorkoutExercise.exercise_id == exercise_id),
        )

        return workout_exercise

    async def snapshot_exercises(self, workout_id: int, routine_id: int) -> None:
        await self._session.execute(
            text(
                """
            INSERT INTO workouts_exercises (workout_id, exercise_id, exercise_index)
            SELECT
                :workout_id,
                exercise_id,
                exercise_index
            FROM routines_exercises
            WHERE routine_id = :routine_id
            """
            ),
            {"workout_id": workout_id, "routine_id": routine_id},
        )
