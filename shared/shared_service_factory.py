import os
from typing import Optional
import redis.asyncio as redis
from shared.shared_repos import CacheRepo


class SharedServiceFactory:
    _redis_client = None
    _cache_repo = None

    @classmethod
    def _get_redis_url(cls) -> str:
        redis_url: Optional[str] = os.getenv("CACHE_CONFIG__URL")
        if redis_url is None or not redis_url.strip("CACHE_CONFIG__URL"):
            raise ValueError("CACHE_CONFIG__URL environment variable is required!")
        return redis_url

    @classmethod
    async def get_redis_client(cls) -> redis.Redis:
        if cls._redis_client is None:
            redis_url = cls._get_redis_url()
            cls._redis_client = await redis.from_url(url=redis_url)
        return cls._redis_client

    @classmethod
    async def get_cache_repo(cls) -> CacheRepo:
        if cls._cache_repo is None:
            redis_url = cls._get_redis_url()
            redis_client = await cls.get_redis_client()
            pool = redis.ConnectionPool.from_url(url=redis_url)
            cls._cache_repo = CacheRepo(pool=pool, redis=redis_client)
        return cls._cache_repo

    @classmethod
    async def close_connection(cls) -> None:
        if cls._redis_client:
            await cls._redis_client.close()
            cls._redis_client = None
            cls._cache_repo = None
