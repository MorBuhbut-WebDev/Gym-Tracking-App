from app.auth import User
from app.db import UnitOfWork
from app.models import Workout
from app.policies import RoutineExercisePolicy, RoutinePolicy
from app.schemas import WorkoutCreate, WorkoutNested


class WorkoutService:
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

        exercises = {}
        for row in rows:
            exercise_id = row.exercise_id
            if exercise_id not in exercises:
                exercises[exercise_id] = {
                    "exercise_id": exercise_id,
                    "exercise_index": row.exercise_index,
                    "sets": [],
                }
            exercises[exercise_id]["sets"].append(
                {
                    "set_id": row.set_id,
                    "set_index": row.set_index,
                    "weight": row.weight,
                    "reps": row.reps,
                    "notes": row.notes,
                }
            )

        workouts = {
            "workout_id": workout.workout_id,
            "routine_id": workout.routine_id,
            "created_at": workout.created_at,
            "ended_at": workout.ended_at,
            "workout_name": workout.workout_name,
            "exercises": list(exercises.values()),
        }

        return WorkoutNested.model_validate(workouts)


def get_workouts_service() -> WorkoutService:
    return WorkoutService()
