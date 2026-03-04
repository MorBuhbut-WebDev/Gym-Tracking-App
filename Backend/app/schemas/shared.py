from pydantic import BaseModel, model_validator, PositiveInt
from typing import Self


class Exercise(BaseModel):
    exercise_id: PositiveInt
    exercise_index: PositiveInt


class ExerciseReorder(BaseModel):
    exercises: list[Exercise]

    def unzip(self) -> tuple[list[PositiveInt], list[PositiveInt]]:
        exercise_ids = [exercise.exercise_id for exercise in self.exercises]
        exercise_positions = [exercise.exercise_index for exercise in self.exercises]
        return exercise_ids, exercise_positions

    @model_validator(mode="after")
    def ensure_valid_order(self) -> Self:
        if len(self.exercises) < 2:
            raise ValueError("At least two exercises is required")

        self.exercises = sorted(self.exercises, key=lambda e: e.exercise_index)
        exercise_ids, exercise_positions = self.unzip()

        if len(exercise_ids) != len(set(exercise_ids)):
            raise ValueError("Can't process duplicated exercises")

        if exercise_positions[0] != 1:
            raise ValueError("Positions must start from index 1")

        for curr, nxt in zip(exercise_positions, exercise_positions[1:]):
            if nxt - curr != 1:
                raise ValueError("Exercises positions must be contiguous sequence")

        return self
