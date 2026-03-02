from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, ExpiredSignatureError
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator

from app.auth import verify_access_token, User
from app.errors import UnauthorizedError
from app.db import get_db, UnitOfWork

security = HTTPBearer()


async def get_user(
    auth_header: HTTPAuthorizationCredentials = Depends(security),
) -> User:
    token = auth_header.credentials
    try:
        user = await verify_access_token(token)
        return user
    except ExpiredSignatureError:
        raise UnauthorizedError("Session expired")
    except (JWTError, ValueError):
        raise UnauthorizedError("Invalid token")


async def get_uow(
    session: AsyncSession = Depends(get_db),
) -> AsyncGenerator[UnitOfWork, None]:
    async with UnitOfWork(session) as uow:
        yield uow
