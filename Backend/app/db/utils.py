from sqlalchemy.exc import IntegrityError
from contextlib import asynccontextmanager

from app.errors import ConflictError


@asynccontextmanager
async def catch_unique_violation(msg: str):
    try:
        yield
    except IntegrityError as e:
        if e.orig.pgcode == "23505":
            raise ConflictError(msg)
        raise
