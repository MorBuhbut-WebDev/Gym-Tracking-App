import uuid
from jose import jwt
from typing import cast, TypedDict, Optional


from app.auth.cache import jwks_cache
from app.auth.dtos import User
from app.config import settings


class JWTPayload(TypedDict):
    sub: str


async def verify_access_token(token: str) -> User:
    kid = cast(Optional[str], jwt.get_unverified_header(token).get("kid", None))

    if kid is None:
        raise ValueError("missing kid")

    public_key = await jwks_cache.get_public_key(kid)

    payload = cast(
        JWTPayload,
        jwt.decode(
            token=token,
            key=public_key,
            algorithms=["ES256"],
            issuer=settings.SUPABASE_EXPECTED_ISSUER,
            audience=settings.SUPABASE_EXPECTED_AUDIENCE,
        ),
    )

    user_id = uuid.UUID(payload["sub"])

    if not user_id:
        raise ValueError("missing sub")

    return User(user_id)
