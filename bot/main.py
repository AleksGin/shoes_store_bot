import asyncio
import logging
import sys

from aiogram import Dispatcher
from callbacks.callbacks import router as callback_router
from core import ServiceFactory
from handlers.handlers import router as handler_router
from middlewares import ServiceMiddleware


async def main() -> None:
    (
        bot,
        cache_repo,
        storage,
        message_service,
        cross_table,
        async_table,
        order_service,
        cache_service,
        cross_service,
        update_service,
        command_handler,
    ) = await ServiceFactory.create_services()

    await command_handler.start_listening()

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
            order_service=order_service,
            cache_service=cache_service,
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
            order_service=order_service,
            cache_service=cache_service,
        )
    )

    dp.include_routers(handler_router, callback_router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        stream=sys.stdout,
    )
    asyncio.run(main())
