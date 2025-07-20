import asyncio
import logging
import sys

from aiogram import (
    Bot,
    Dispatcher,
)
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from core import settings
from services import (
    AdminPanelService,
    MessageService,
)

from shared import SharedServiceFactory
from shared import CacheSetup

from middleware import AdminMiddleware
from handlers import admin_handler_router
from admin_callbacks import admin_callback_router


async def main() -> None:
    bot = Bot(
        token=settings.admin_bot_config.token_bot,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    cache_repo = await SharedServiceFactory.get_cache_repo()

    message_service = MessageService(bot=bot)
    admin_service = AdminPanelService(
        message_service=message_service,
        cache_repo=cache_repo,
    )

    dp = Dispatcher()

    admin_ids = await CacheSetup(
        cache_repo=cache_repo,
        settings=settings,
    )

    admin_middleware = AdminMiddleware(
        admin_ids=admin_ids,
        admin_service=admin_service,
        message_service=message_service,
        cache_repo=cache_repo,
    )

    dp.message.middleware(admin_middleware)
    dp.callback_query.middleware(admin_middleware)

    dp.include_routers(
        admin_handler_router,
        admin_callback_router,
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        stream=sys.stdout,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    asyncio.run(main())
