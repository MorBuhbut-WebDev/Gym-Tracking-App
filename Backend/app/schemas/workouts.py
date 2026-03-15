from datetime import UTC, date, datetime, timedelta
from typing import Self

from pydantic import BaseModel, Field, PositiveInt, model_validator

from app.schemas.shared import AppBaseModel
from app.schemas.workouts_exercises import WorkoutExerciseNested


class WorkoutCreate(BaseModel):
    routine_id: PositiveInt


class WorkoutFilters(BaseModel):
    start_date: date = Field(default_factory=lambda: date.today().replace(day=1))
    end_date: date | None = Field(default=None)

    @model_validator(mode="after")
    def set_end_date_and_convert(self) -> Self:
        if self.end_date is None:
            if self.start_date.month == 12:
                self.end_date = date(self.start_date.year + 1, 1, 1)
            else:
                self.end_date = date(self.start_date.year, self.start_date.month + 1, 1)
        else:
            if self.end_date < self.start_date:
                raise ValueError("end date must be greater or equal to the start date")

            self.end_date = self.end_date + timedelta(days=1)
        return self

    def to_datetime(self) -> tuple[datetime, datetime]:
        assert self.end_date is not None, (
            "end_date must be set before converting to datetime"
        )

        start = datetime(
            self.start_date.year,
            self.start_date.month,
            self.start_date.day,
            tzinfo=UTC,
        )
        end = datetime(
            self.end_date.year,
            self.end_date.month,
            self.end_date.day,
            tzinfo=UTC,
        )
        return start, end


class WorkoutBase(BaseModel):
    workout_id: int
    routine_id: int | None
    created_at: datetime
    ended_at: datetime | None
    workout_name: str


class WorkoutResponse(WorkoutBase, AppBaseModel):
    pass


class WorkoutNested(WorkoutBase, AppBaseModel):
    exercises: list[WorkoutExerciseNested]
