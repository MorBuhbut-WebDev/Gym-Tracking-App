from pydantic import BaseModel, PositiveInt, Field, model_validator
from typing import Optional, Self
from datetime import datetime, date, timedelta, timezone

from app.schemas.workouts_exercises import WorkoutExerciseNested


class WorkoutCreate(BaseModel):
    routine_id: PositiveInt


class WorkoutFilters(BaseModel):
    start_date: date = Field(default_factory=lambda: date.today().replace(day=1))
    end_date: Optional[date] = Field(default=None)

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

    def to_datetimes(self) -> tuple[datetime, datetime]:
        start = datetime(
            self.start_date.year,
            self.start_date.month,
            self.start_date.day,
            tzinfo=timezone.utc,
        )
        end = datetime(
            self.end_date.year,
            self.end_date.month,
            self.end_date.day,
            tzinfo=timezone.utc,
        )
        return start, end


class WorkoutBase(BaseModel):
    workout_id: int
    routine_id: Optional[int]
    created_at: datetime
    ended_at: Optional[datetime]
    workout_name: str


class WorkoutResponse(WorkoutBase):
    model_config = {"from_attributes": True}


class WorkoutNested(WorkoutBase):
    exercises: list[WorkoutExerciseNested]

    model_config = {"from_attributes": True}
