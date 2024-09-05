import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiohttp import ClientSession

from bot.services.message_service import MessageService
import file_for_test
from bot.callbacks.callbacks import router as callback_router
from bot.middlewares.service_middleware import ServiceMiddleware
from bot.services.crossworld_service import CrossworldService
from config_reader import config


async def main():
    async with ClientSession() as session:
        bot = Bot(
            token=config.token_bot.get_secret_value(),
            default=DefaultBotProperties(parse_mode=ParseMode.HTML),
        )
        # contextno_repo = ContextnoRepo(session, config.contextno_url)
        # pool = redis.ConnectionPool.from_url(config.redis_url)
        # cache_repo = CacheRepository(pool)
        message_service = MessageService(bot)
        cross_service = CrossworldService(message_service, bot)

        dp = Dispatcher()

        dp.message.middleware(ServiceMiddleware(cross_service, message_service))
        dp.callback_query.middleware(ServiceMiddleware(cross_service, message_service))

        dp.include_routers(file_for_test.router, callback_router)

        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
