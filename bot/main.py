import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiohttp import ClientSession
from callbacks.callbacks import router as callback_router
from core.config_reader import config
from handlers.handlers import router as handler_router
from middlewares import ServiceMiddleware
from repository import CrossworldTableRepo
from services import (
    CrossworldService,
    MessageService,
)


async def main() -> None:
    async with ClientSession() as session:
        bot = Bot(
            token=config.bot_config.token_bot.get_secret_value(),
            default=DefaultBotProperties(parse_mode=ParseMode.HTML),
        )

        cross_table = CrossworldTableRepo(
            cred_file=config.table_config.cred_file.get_secret_value(),
            sheet_url=config.table_config.url_table,
        )
        message_service = MessageService(bot=bot)
        cross_service = CrossworldService(
            message_service=message_service, cross_table=cross_table
        )

        dp = Dispatcher()

        dp.message.middleware(
            ServiceMiddleware(
                cross_service=cross_service,
                message_service=message_service,
                cross_table=cross_table,
            )
        )
        dp.callback_query.middleware(
            ServiceMiddleware(
                cross_service=cross_service,
                message_service=message_service,
                cross_table=cross_table,
            )
        )

        dp.include_routers(handler_router, callback_router)

        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())