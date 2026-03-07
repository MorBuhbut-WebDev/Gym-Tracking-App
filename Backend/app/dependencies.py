from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from app.db import AsyncSessionLocal


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as async_session:
        yield async_session
