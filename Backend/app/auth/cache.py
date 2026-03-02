import asyncio
import time
import httpx
from jose import jwk
from jose.backends.base import Key
from typing import TypedDict, cast

from app.config import settings


class JWKS(TypedDict):
    keys: list[dict[str, any]]


class Cache:
    def __init__(self) -> None:
        self._jwks_cache: dict[str, dict] = {}
        self._last_fetch = 0.0
        self._cache_ttl = 3600
        self._lock = asyncio.Lock()

    async def _fetch_jwks(self) -> JWKS:
        async with httpx.AsyncClient() as client:
            response = await client.get(settings.SUPABASE_JWKS_URl, timeout=5.0)
            response.raise_for_status()
            return cast(JWKS, response.json())

    def _is_expired(self) -> bool:
        return time.time() - self._last_fetch > self._cache_ttl

    async def _ensure_kid(self, kid: str) -> None:
        if kid in self._jwks_cache and not self._is_expired():
            return

        async with self._lock:
            if kid not in self._jwks_cache or self._is_expired():
                jwks = await self._fetch_jwks()
                self._jwks_cache = {key["kid"]: key for key in jwks["keys"]}
                self._last_fetch = time.time()

    async def get_public_key(self, kid: str) -> Key:
        try:
            await self._ensure_kid(kid)
            return jwk.construct(self._jwks_cache[kid])
        except KeyError:
            raise ValueError("missing kid")


jwks_cache = Cache()
