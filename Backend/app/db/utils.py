from contextlib import asynccontextmanager

from sqlalchemy.exc import IntegrityError

from app.exceptions import ConflictException


@asynccontextmanager
async def catch_unique_violation(msg: str):
    try:
        yield
    except IntegrityError as e:
        if e.orig.pgcode == "23505":  # type: ignore
            raise ConflictException(msg) from e
        raise
