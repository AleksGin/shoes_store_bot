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
        order_number: str,
        info: str,
        expire_time: int = CacheTTL.day,
    ) -> None:
        async with Redis.from_pool(connection_pool=self.pool) as redis:
            key: str = CacheKey.USER_ID_KEY.format(
                user_id,
                order_number,
            )
            await redis.set(
                name=key,
                value=info,
                ex=expire_time,
            )

    async def get_info_about_order_by_user_id(
        self,
        user_id: int,
        order_number: str,
    ):
        async with Redis.from_pool(connection_pool=self.pool) as redis:
            key = CacheKey.USER_ID_KEY.format(
                user_id,
                order_number,
            )
            info = await redis.get(name=key)
            if info is None:
                return None
            return info.decode("utf-8")

    async def get_all_cached_orders(self):
        async with Redis.from_pool(connection_pool=self.pool) as redis:
            cursor = 0
            keys = []

            while True:
                cursor, found_keys = await redis.scan(
                    cursor=cursor,
                    match="user:*:order:*",
                )
                keys.extend(found_keys)

                if cursor == 0:
                    break

            return keys
