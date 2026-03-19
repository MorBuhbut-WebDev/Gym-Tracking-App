from collections.abc import AsyncGenerator
from datetime import date

from fastapi import Depends, Query
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import ExpiredSignatureError, JWTError
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import User, verify_access_token
from app.db import AsyncSessionLocal, UnitOfWork
from app.exceptions import UnauthorizedException, UnprocessableException
from app.schemas import WorkoutFilters

security = HTTPBearer()


async def get_user(
    auth_header: HTTPAuthorizationCredentials = Depends(security),
) -> User:
    token = auth_header.credentials
    try:
        user = await verify_access_token(token)
        return user
    except ExpiredSignatureError as e:
        raise UnauthorizedException("Session expired") from e
    except (JWTError, ValueError) as e:
        raise UnauthorizedException("Invalid token") from e


async def get_db() -> AsyncGenerator[AsyncSession]:
    async with AsyncSessionLocal() as async_session:
        yield async_session


async def get_uow(
    session: AsyncSession = Depends(get_db),
) -> AsyncGenerator[UnitOfWork]:
    async with UnitOfWork(session) as uow:
        yield uow


async def get_workout_filters(
    start_date: date | None = Query(None),
    end_date: date | None = Query(None),
) -> WorkoutFilters:
    try:
        return WorkoutFilters(start_date=start_date, end_date=end_date)
    except ValidationError as e:
        raise UnprocessableException(
            " | ".join(err["msg"] for err in e.errors())
        ) from e
