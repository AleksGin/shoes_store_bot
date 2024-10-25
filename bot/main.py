import asyncio
import logging
import sys

import redis.asyncio as redis
from aiogram.fsm.storage.redis import RedisStorage
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from callbacks.callbacks import router as callback_router
from core.config_reader import config
from handlers.handlers import router as handler_router
from middlewares import ServiceMiddleware
from repository import (
    CacheRepo,
    CrossworldTableRepo,
    AsyncGoogleSheetsService,
)
from services import (
    CrossworldService,
    MessageService,
    UpdateDataService,
)
from phrases import CacheTTL


async def main() -> None:
    bot = Bot(
        token=config.bot_config.token_bot.get_secret_value(),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    pool = redis.ConnectionPool.from_url(
        url=config.cache_config.url,
    )

    redis_client = await redis.from_url(config.cache_config.url)

    cache_repo = CacheRepo(pool=pool)

    storage = RedisStorage(
        redis=redis_client,
        state_ttl=CacheTTL.week,
        data_ttl=CacheTTL.week,
    )

    cross_table = CrossworldTableRepo(
        cred_file=config.table_config.cred_file.get_secret_value(),
        sheet_url=config.table_config.url_table,
    )

    async_table = AsyncGoogleSheetsService(sheets_service=cross_table)

    message_service = MessageService(
        bot=bot,
    )
    cross_service = CrossworldService(
        message_service=message_service,
        cache_repo=cache_repo,
        async_table=async_table,
    )
    update_service = UpdateDataService(
        cache_repo=cache_repo,
        cross_service=cross_service,
        async_table=async_table,
    )

    update_service.start_scheduler()

    dp = Dispatcher(storage=storage)

    dp.message.middleware(
        ServiceMiddleware(
            cross_service=cross_service,
            message_service=message_service,
            cross_table=cross_table,
            cache_repo=cache_repo,
            update_service=update_service,
            async_table=async_table,
        )
    )
    dp.callback_query.middleware(
        ServiceMiddleware(
            cross_service=cross_service,
            message_service=message_service,
            cross_table=cross_table,
            cache_repo=cache_repo,
            update_service=update_service,
            async_table=async_table,
        )
    )

    dp.include_routers(handler_router, callback_router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
