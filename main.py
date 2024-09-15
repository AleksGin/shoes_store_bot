import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

import bot.handlers.handlers as handlers
from bot.callbacks.callbacks import router as callback_router
from bot.middlewares.service_middleware import ServiceMiddleware
from bot.services.crossworld_service import CrossworldService
from bot.services.google_sheets_service import CrossworldTable
from bot.services.message_service import MessageService
from config_reader import config


async def main() -> None:
    bot = Bot(
        token=config.token_bot.get_secret_value(),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    cross_table = CrossworldTable(
        cred_file=config.cred_file.get_secret_value(),
        sheet_url=config.url_table.get_secret_value(),
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

    dp.include_routers(handlers.router, callback_router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
