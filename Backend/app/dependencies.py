from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from app.db import AsyncSessionLocal


async def get_db() -> AsyncGenerator[AsyncSession]:
    async with AsyncSessionLocal() as async_session:
        yield async_session
