from app.auth import User
from app.db import UnitOfWork
from app.models import Workout
from app.policies import RoutineExercisePolicy, RoutinePolicy, WorkoutPolicy
from app.repositories.workouts import WorkoutDetailRow
from app.schemas import WorkoutCreate, WorkoutFilters, WorkoutNested, WorkoutResponse
from app.schemas.workouts_exercises import WorkoutExerciseNested
from app.schemas.workouts_sets import WorkoutSetNested


class WorkoutService:
    def _build_workout_response_nested(
        self, rows: list[WorkoutDetailRow]
    ) -> WorkoutNested:
        assert rows, "rows must not be empty"

        exercises: dict[int, WorkoutExerciseNested] = {}
        for row in rows:
            exercise_id = row.exercise_id
            if exercise_id not in exercises:
                exercises[exercise_id] = WorkoutExerciseNested(
                    exercise_id=row.exercise_id,
                    exercise_index=row.exercise_index,
                    sets=[],
                )
            exercises[exercise_id].sets.append(
                WorkoutSetNested(
                    set_id=row.set_id,
                    set_index=row.set_index,
                    weight=row.weight,
                    reps=row.reps,
                    notes=row.notes,
                )
            )

        return WorkoutNested(
            workout_id=rows[0].workout_id,
            routine_id=rows[0].routine_id,
            created_at=rows[0].created_at,
            ended_at=rows[0].ended_at,
            workout_name=rows[0].workout_name,
            exercises=list(exercises.values()),
        )

    async def create(
        self, uow: UnitOfWork, user: User, payload: WorkoutCreate
    ) -> WorkoutNested:
        routine = await RoutinePolicy.assert_exists(
            repo=uow.routines_repo, user_id=user.user_id, routine_id=payload.routine_id
        )

        await RoutineExercisePolicy.assert_has_exercises(
            repo=uow.routines_exercises_repo, routine_id=payload.routine_id
        )

        workout = uow.workouts_repo.add(
            Workout.create(
                routine_id=payload.routine_id,
                user_id=user.user_id,
                workout_name=routine.routine_name,
            )
        )

        await uow.flush()

        await uow.workouts_exercises_repo.snapshot_exercises(
            workout_id=workout.workout_id, routine_id=payload.routine_id
        )

        await uow.workouts_sets_repo.generate_sets(
            workout_id=workout.workout_id, routine_id=payload.routine_id
        )

        rows = await uow.workouts_repo.get_with_exercises_and_sets(workout.workout_id)

        return self._build_workout_response_nested(rows)

    async def get_all(
        self, uow: UnitOfWork, user: User, filters: WorkoutFilters
    ) -> list[WorkoutResponse]:
        start_date, end_date = filters.to_datetime()
        workouts = await uow.workouts_repo.get_all_by_date_range(
            user_id=user.user_id, start_date=start_date, end_date=end_date
        )
        return [WorkoutResponse.model_validate(workout) for workout in workouts]

    async def get(self, uow: UnitOfWork, user: User, workout_id: int) -> WorkoutNested:
        workout = await WorkoutPolicy.assert_exists(
            repo=uow.workouts_repo, user_id=user.user_id, workout_id=workout_id
        )
        rows = await uow.workouts_repo.get_with_exercises_and_sets(workout.workout_id)

        return self._build_workout_response_nested(rows)


def get_workouts_service() -> WorkoutService:
    return WorkoutService()
