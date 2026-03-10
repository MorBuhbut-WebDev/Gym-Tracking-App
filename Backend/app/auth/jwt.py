import uuid
from typing import cast

from jose import jwt
from pydantic import BaseModel

from app.auth.cache import jwks_cache
from app.auth.user_dto import User
from app.config import settings


class JWTPayload(BaseModel):
    sub: str


async def verify_access_token(token: str) -> User:
    kid = jwt.get_unverified_header(token).get("kid", None)

    if not isinstance(kid, str):
        raise ValueError("missing or invalid kid")

    public_key = await jwks_cache.get_public_key(kid)

    payload = JWTPayload.model_validate(
        jwt.decode(
            token=token,
            key=public_key,
            algorithms=["ES256"],
            issuer=settings.SUPABASE_EXPECTED_ISSUER,
            audience=settings.SUPABASE_EXPECTED_AUDIENCE,
        )
    )

    try:
        user_id = uuid.UUID(payload.sub)
    except ValueError as e:
        raise ValueError(f"sub '{payload.sub}' is not a valid UUID") from e

    return User(user_id)
