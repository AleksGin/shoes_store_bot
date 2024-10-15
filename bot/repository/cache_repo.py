from phrases import (
    CacheKey,
    CacheTTL,
)
from redis.asyncio import (
    ConnectionPool,
    Redis,
)


class CacheRepo:
    def __init__(self, pool: ConnectionPool) -> None:
        self.pool = pool

    async def set_info_about_order_by_user_id(
        self,
        user_id: int,
        order_number: int,
        info: str,
        expire_time: int = CacheTTL.day,
    ) -> None:
        async with Redis.from_pool(connection_pool=self.pool) as redis:
            key: str = CacheKey.USER_ID_KEY.format(user_id)
            await redis.zadd(
                name=key,
                mapping={str(order_number): info},
            )
            await redis.expire(
                name=key,
                time=expire_time,
            )

    async def get_info_about_order_by_user_id(
        self,
        user_id: int,
        order_number: int,
    ):
        async with Redis.from_pool(connection_pool=self.pool) as redis:
            key: str = CacheKey.USER_ID_KEY.format(user_id)
            info = await redis.zrangebyscore(
                name=key,
                min=str(order_number),
                max=str(order_number),
            )
            if info:
                return info.decode("utf-8")
            return None
