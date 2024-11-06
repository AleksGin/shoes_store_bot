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
    def __init__(self, pool: ConnectionPool, redis: Redis) -> None:
        self.pool = pool
        self.redis = redis

    async def set_order_status(
        self,
        order_number: str,
        info: str,
        expire_time: int = CacheTTL.month,
        user_id: int | None = None,
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
                key: str = CacheKey.ORDER_STATUS_KEY.format(
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

    async def get_info_about_order(
        self,
        order_number: str,
        user_id: int | None = None,
        tracking: bool = False,
    ):
        async with Redis.from_pool(connection_pool=self.pool) as redis:
            if tracking:
                key: str = CacheKey.TRACKING_USER_ID_KEY.format(
                    user_id,
                    order_number,
                )
            else:
                key = CacheKey.ORDER_STATUS_KEY.format(
                    order_number,
                )
            info = await redis.get(name=key)
            if info is None:
                return None
            return info.decode("utf-8")

    async def get_cached_orders(
        self,
        match_form: str,
    ):
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

    async def get_multiple_order_infos(self, keys):
        async with Redis.from_pool(connection_pool=self.pool) as redis:
            infos = await redis.mget(keys=keys)
            logging.info(f"сделал в mget-методе: {infos}")

        return [info.decode("utf-8") if info else None for info in infos]

    async def set_multiple_value(self, keys, value):
        logging.info("перешел в set_multiple_value")
        async with Redis.pipeline(self=self.redis) as pipe:
            for key in keys:
                logging.info(f"получил key: {key}")
                await pipe.set(name=key, value=value)
                logging.info(
                    f"установил новое значение для key: {key} с value: {value}"
                )
            sett = await pipe.execute()
            logging.info(f"sett я выполнил я только сейчас после установки всех значений для всех пользователей = {sett}")
            

    async def delete_tracking_orders(
        self,
        user_id: int,
        order_number: str | None = None,
        single_order_only: bool = False,
    ):
        logging.info("перешел в delete_tracking_orders")
        async with Redis.from_pool(connection_pool=self.pool) as redis:
            if single_order_only:
                logging.info(f"обратился {single_order_only}")
                result = await redis.delete(
                    CacheKey.TRACKING_USER_ID_KEY.format(
                        user_id,
                        order_number,
                    )
                )
                return result > 0
            else:
                orders = await self.get_cached_orders(
                    match_form=CacheKey.match_for_user_to_orders.format(user_id)
                )
                if orders:
                    await redis.delete(*orders)
        return False
