from app.auth import User
from app.db.unit_of_work import UnitOfWork
from app.models import Workout
from app.policies import (
    RoutineExercisePolicy,
    RoutinePolicy,
    WorkoutExercisePolicy,
    WorkoutPolicy,
    WorkoutSetPolicy,
)
from app.schemas import (
    ExerciseReorder,
    WorkoutCreate,
    WorkoutExerciseNested,
    WorkoutFilters,
    WorkoutNested,
    WorkoutResponse,
    WorkoutSetCreate,
    WorkoutSetNested,
    WorkoutSetResponse,
    WorkoutUpdate,
)


class WorkoutService:
    async def create(
        self, uow: UnitOfWork, user: User, payload: WorkoutCreate
    ) -> WorkoutResponse:
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

        return WorkoutResponse.model_validate(workout)

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
        rows = await uow.workouts_repo.get_with_exercises_and_sets(
            workout.workout_id, user.user_id
        )

        exercises: dict[int, WorkoutExerciseNested] = {}
        for row in rows:
            exercise_id = row.exercise_id
            if exercise_id not in exercises:
                exercises[exercise_id] = WorkoutExerciseNested(
                    exercise_id=row.exercise_id,
                    exercise_index=row.exercise_index,
                    exercise_name=row.exercise_name,
                    sets=[],
                )
            exercises[exercise_id].sets.append(
                WorkoutSetNested(
                    set_id=row.set_id,
                    set_index=row.set_index,
                    weight=row.weight,
                    reps=row.reps,
                    notes=row.notes,
                    prev_weight=row.prev_weight,
                    prev_reps=row.prev_reps,
                    prev_notes=row.prev_notes,
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

    async def update(
        self, uow: UnitOfWork, user: User, workout_id: int, payload: WorkoutUpdate
    ) -> None:
        workout = await WorkoutPolicy.assert_exists(
            repo=uow.workouts_repo, user_id=user.user_id, workout_id=workout_id
        )

        WorkoutPolicy.assert_update_dates_valid(workout, payload)

        workout = uow.workouts_repo.update(old=workout, updated=payload)

    async def delete(self, uow: UnitOfWork, user: User, workout_id: int) -> None:
        workout = await WorkoutPolicy.assert_exists(
            repo=uow.workouts_repo, user_id=user.user_id, workout_id=workout_id
        )

        await uow.workouts_repo.delete(workout)

    async def add_exercise(
        self, uow: UnitOfWork, user: User, workout_id: int, exercise_id: int
    ) -> None:
        await WorkoutExercisePolicy.assert_accessible(
            exercises_repo=uow.exercises_repo,
            workouts_repo=uow.workouts_repo,
            user_id=user.user_id,
            workout_id=workout_id,
            exercise_id=exercise_id,
        )

        await WorkoutExercisePolicy.assert_not_linked(
            repo=uow.workouts_exercises_repo,
            workout_id=workout_id,
            exercise_id=exercise_id,
        )

        await uow.workouts_exercises_repo.add_exercise(workout_id, exercise_id)

    async def delete_exercise(
        self, uow: UnitOfWork, user: User, workout_id: int, exercise_id: int
    ) -> None:
        _, workout_exercise = await WorkoutExercisePolicy.assert_link_exists(
            workouts_repo=uow.workouts_repo,
            workouts_exercises_repo=uow.workouts_exercises_repo,
            user_id=user.user_id,
            workout_id=workout_id,
            exercise_id=exercise_id,
        )

        await uow.workouts_exercises_repo.delete(workout_exercise)
        await uow.flush()
        await uow.workouts_exercises_repo.shift_indices_after_delete(
            [workout_id], [workout_exercise.exercise_index]
        )

    async def reorder_exercises(
        self,
        uow: UnitOfWork,
        user: User,
        workout_id: int,
        payload: ExerciseReorder,
    ) -> None:
        await WorkoutPolicy.assert_exists(
            repo=uow.workouts_repo, user_id=user.user_id, workout_id=workout_id
        )

        await WorkoutExercisePolicy.assert_valid_reorder(
            repo=uow.workouts_exercises_repo, workout_id=workout_id, payload=payload
        )

        await uow.workouts_exercises_repo.reorder_exercises(workout_id, payload)

    async def add_set(
        self,
        uow: UnitOfWork,
        user: User,
        workout_id: int,
        exercise_id: int,
        payload: WorkoutSetCreate,
    ) -> WorkoutSetResponse:
        await WorkoutExercisePolicy.assert_link_exists(
            workouts_repo=uow.workouts_repo,
            workouts_exercises_repo=uow.workouts_exercises_repo,
            user_id=user.user_id,
            workout_id=workout_id,
            exercise_id=exercise_id,
        )

        set = await uow.workouts_sets_repo.add_set(workout_id, exercise_id, payload)

        return WorkoutSetResponse.model_validate(set)

    async def delete_set(
        self,
        uow: UnitOfWork,
        user: User,
        workout_id: int,
        exercise_id: int,
        set_id: int,
    ) -> None:
        _, workout_set = await WorkoutSetPolicy.assert_link_exists(
            workouts_repo=uow.workouts_repo,
            workouts_sets_repo=uow.workouts_sets_repo,
            user_id=user.user_id,
            workout_id=workout_id,
            exercise_id=exercise_id,
            set_id=set_id,
        )

        await WorkoutSetPolicy.assert_set_deletable(
            workouts_sets_repo=uow.workouts_sets_repo,
            workout_id=workout_id,
            exercise_id=exercise_id,
        )

        await uow.workouts_sets_repo.delete(workout_set)
        await uow.flush()
        await uow.workouts_sets_repo.shift_indices_after_delete(
            workout_id, exercise_id, workout_set.set_index
        )


def get_workouts_service() -> WorkoutService:
    return WorkoutService()
