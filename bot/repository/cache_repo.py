import asyncio
import logging

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
        tracking: bool = False,
    ) -> None:
        async with Redis.from_pool(connection_pool=self.pool) as redis:
            if tracking:
                logging.info("понял, что tracking True и я выполняю внутри tracking")
                key: str = CacheKey.TRACKING_USER_ID_KEY.format(
                    user_id,
                    order_number,
                )
            else:
                key: str = CacheKey.USER_ID_KEY.format(
                    user_id,
                    order_number,
                )
            setting = await redis.set(
                name=key,
                value=info,
                ex=expire_time,
            )
            logging.info(
                f"форма ключа: {key}, инфо: {info}, а сама функция вот так: {setting}"
            )

    async def get_info_about_order_by_user_id(
        self, user_id: int, order_number: str, tracking: bool = False
    ):
        async with Redis.from_pool(connection_pool=self.pool) as redis:
            if tracking:
                await asyncio.sleep(4)
                key: str = CacheKey.TRACKING_USER_ID_KEY.format(
                    user_id,
                    order_number,
                )
            else:
                await asyncio.sleep(4)
                key = CacheKey.USER_ID_KEY.format(
                    user_id,
                    order_number,
                )
            info = await redis.get(name=key)
            await asyncio.sleep(4)
            if info is None:
                return None
            return info.decode("utf-8")

    async def get_all_cached_orders(
        self,
        match_form: str,
    ):
        await asyncio.sleep(4)
        async with Redis.from_pool(connection_pool=self.pool) as redis:
            cursor = 0
            keys = []

            while True:
                cursor, found_keys = await redis.scan(
                    cursor=cursor,
                    match=match_form,
                )
                keys.extend(found_keys)

                if cursor == 0:
                    break

            return keys
