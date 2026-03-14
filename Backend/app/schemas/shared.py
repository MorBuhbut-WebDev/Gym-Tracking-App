from typing import NamedTuple, Self

from pydantic import BaseModel, ConfigDict, PositiveInt, model_validator


class AppBaseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class ExerciseOrderItem(BaseModel):
    exercise_id: PositiveInt
    exercise_index: PositiveInt


class UnzippedExercises(NamedTuple):
    exercise_ids: list[int]
    exercise_indices: list[int]


class ExerciseReorder(BaseModel):
    exercises: list[ExerciseOrderItem]

    def unzip(self) -> UnzippedExercises:
        return UnzippedExercises(
            exercise_ids=[exercise.exercise_id for exercise in self.exercises],
            exercise_indices=[exercise.exercise_index for exercise in self.exercises],
        )

    @model_validator(mode="after")
    def ensure_valid_order(self) -> Self:
        if len(self.exercises) < 2:
            raise ValueError("At least two exercises is required")

        self.exercises = sorted(self.exercises, key=lambda e: e.exercise_index)
        exercise_ids, exercise_indices = self.unzip()

        if len(exercise_ids) != len(set(exercise_ids)):
            raise ValueError("Can't process duplicated exercises")

        if exercise_indices[0] != 1:
            raise ValueError("Positions must start from index 1")

        for curr, nxt in zip(exercise_indices, exercise_indices[1:], strict=False):
            if nxt - curr != 1:
                raise ValueError("Exercises positions must be contiguous sequence")

        return self
