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

from shared.shared_service_factory import SharedServiceFactory
from shared.shared_pharses import CacheKey

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

    admin_ids = []
    if settings.admin_bot_config.initial_ids:
        try:
            admin_ids = [
                int(x.strip())
                for x in settings.admin_bot_config.initial_ids.split(",")
                if x.strip()
            ]
        except ValueError:
            logging.error("Ошибка в парсинге admin IDs")
            admin_ids = []

    if settings.admin_bot_config.super_admin_id:
        try:
            super_admin_id = int(settings.admin_bot_config.super_admin_id)
            if super_admin_id not in admin_ids:
                admin_ids.append(super_admin_id)
        except ValueError:
            logging.error("Ошибка в парсинге super admin ID")

    for admin_id in admin_ids:
        try:
            await cache_repo.add_admin_id(
                CacheKey.ADMINS_KEY,
                admin_id,
            )
            logging.info(f"Admin ID {admin_id} added to cache")
        except Exception as e:
            logging.error(f"Failed to add admin {admin_id}: {e}")

    dp = Dispatcher()

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
