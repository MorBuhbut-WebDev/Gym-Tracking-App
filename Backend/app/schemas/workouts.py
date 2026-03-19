from datetime import UTC, date, datetime, timedelta
from typing import Self

from pydantic import BaseModel, PositiveInt, model_validator

from app.schemas.shared import AppBaseModel
from app.schemas.workouts_exercises import WorkoutExerciseNested


class WorkoutCreate(BaseModel):
    routine_id: PositiveInt


class WorkoutFilters(BaseModel):
    start_date: date | None = None
    end_date: date | None = None

    @model_validator(mode="after")
    def set_end_date_and_convert(self) -> Self:
        if self.start_date is None:
            self.start_date = date.today().replace(day=1)

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
        assert self.end_date is not None and self.start_date is not None, (
            "end_date and start_date must be set before converting to datetime"
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


class WorkoutUpdate(BaseModel):
    created_at: datetime | None = None
    ended_at: datetime | None = None

    @model_validator(mode="after")
    def validate_dates(self) -> Self:
        if self.created_at is None and self.ended_at is None:
            raise ValueError("At least one of created_at or ended_at must be provided")

        if self.created_at is not None and self.ended_at is not None:
            if self.ended_at <= self.created_at:
                raise ValueError("ended_at must be greater than created_at")

        return self


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
