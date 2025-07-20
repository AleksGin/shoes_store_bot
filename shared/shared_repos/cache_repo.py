from datetime import datetime
import json
import logging
from typing import (
    Any,
    List,
    Optional,
)

from redis.asyncio import (
    ConnectionPool,
    Redis,
)

from shared.shared_pharses import (
    CacheErrors,
    CacheKey,
    CacheTTL,
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
        keep_ttl: bool = False,
    ) -> None:
        async with Redis.from_pool(connection_pool=self.pool) as redis:
            if tracking:
                key: str = CacheKey.TRACKING_USER_ID_KEY.format(
                    user_id,
                    order_number,
                )
            else:
                key: str = CacheKey.ORDER_STATUS_KEY.format(
                    order_number,
                )
            if keep_ttl:
                await redis.set(
                    name=key,
                    value=info,
                    keepttl=True,
                )
            else:
                await redis.set(
                    name=key,
                    value=info,
                    ex=expire_time,
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

        return [info.decode("utf-8") if info else None for info in infos]

    async def set_multiple_value(self, keys, value, keep_ttl: bool = False):
        async with Redis.pipeline(self=self.redis) as pipe:
            for key in keys:
                if keep_ttl:
                    await pipe.set(name=key, value=value, keepttl=True)
                else:
                    await pipe.set(name=key, value=value)
            await pipe.execute()

    async def delete_tracking_orders(
        self,
        user_id: int,
        order_number: str | None = None,
        single_order_only: bool = False,
    ):
        async with Redis.from_pool(connection_pool=self.pool) as redis:
            if single_order_only:
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

    async def get_yuan_rate(self, key: str, default_rate: int = 0) -> float:
        async with Redis.from_pool(connection_pool=self.pool) as redis:
            result = await redis.get(key)
            if result is not None:
                try:
                    return float(result.decode("utf-8"))
                except (ValueError, AttributeError):
                    raise ValueError(CacheErrors.uncorrect_value)
            return default_rate

    async def set_yuan_rate(
        self,
        key: str,
        rate: int | float,
    ) -> bool:
        async with Redis.from_pool(connection_pool=self.pool) as redis:
            result = await redis.set(key, str(rate))
            await redis.persist(key)
            return result is not None

    async def get_admin_ids(self, key: str) -> List[int]:
        async with Redis.from_pool(connection_pool=self.pool) as redis:
            result = await redis.smembers(key)  # type: ignore
            if not result:
                return []
            try:
                return [int(admin_id.decode("utf-8")) for admin_id in result]
            except (ValueError, AttributeError):
                raise ValueError(f"Некорректные ID админов в Redis: {result}")

    async def add_admin_id(
        self,
        key: str,
        user_id: int,
    ) -> bool:
        async with Redis.from_pool(connection_pool=self.pool) as redis:
            result = await redis.sadd(key, user_id)  # type: ignore
            await redis.persist(key)
            return result > 0

    async def remove_admin_id(
        self,
        key: str,
        user_id: int,
    ) -> bool:
        async with Redis.from_pool(connection_pool=self.pool) as redis:
            result = await redis.srem(key, user_id)  # type: ignore
            return result > 0

    async def is_admin(
        self,
        key: str,
        user_id: int,
    ) -> bool:
        async with Redis.from_pool(connection_pool=self.pool) as redis:
            result = await redis.sismember(key, user_id)  # type: ignore
            return result > 0

    async def get_closest_date(self, key: str) -> str:
        async with Redis.from_pool(connection_pool=self.pool) as redis:
            result = await redis.get(key)
            return result.decode("utf-8")

    async def set_closest_day(
        self,
        key: str,
        date: str,
    ) -> bool:
        async with Redis.from_pool(connection_pool=self.pool) as redis:
            result = await redis.set(key, date)
            await redis.persist(key)
            return result is not None

    async def add_admin_log(
        self,
        action: str,
        admin_id: int,
        new_value: Optional[str] = None,
        max_logs: int = 5,
    ) -> None:
        async with Redis.from_pool(connection_pool=self.pool) as redis:
            try:
                log_entry: dict[str, Any] = {
                    "action": action,
                    "admin_id": admin_id,
                    "timestamp": datetime.now().strftime("%d.%m.%Y %H:%M"),
                }

                if new_value is not None:
                    log_entry["new_value"] = new_value

                existing_logs_json = await redis.get(CacheKey.ADMIN_LOGS_KEY)
                if existing_logs_json:
                    logs = json.loads(existing_logs_json.decode("utf-8"))
                else:
                    logs = []

                logs.insert(0, log_entry)

                logs = logs[:max_logs]

                await redis.set(
                    CacheKey.ADMIN_LOGS_KEY,
                    json.dumps(logs, ensure_ascii=False),
                )
                await redis.persist(CacheKey.ADMIN_LOGS_KEY)
            except Exception as e:
                logging.info(f"При добавлении логов что-то пошло не так: {e}")

    async def get_admin_logs(self, limit: int = 5) -> List[dict]:
        async with Redis.from_pool(connection_pool=self.pool) as redis:
            try:
                logs_json = await redis.get(CacheKey.ADMIN_LOGS_KEY)
                if logs_json:
                    logs = json.loads(logs_json.decode("utf-8"))
                    return logs[:limit]
                return []
            except Exception:
                return []

    async def send_bot_command(self, command_data: dict) -> bool:
        try:
            async with Redis.from_pool(connection_pool=self.pool) as redis:
                result = await redis.publish(
                    "bot_commands",
                    json.dumps(command_data),
                )

                return result > 0
        except Exception:
            return False
