import redis.asyncio as redis
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from repository import (
    AsyncGoogleSheetsService,
    CrossworldTableRepo,
)
from services import (
    CacheService,
    CrossworldService,
    MessageService,
    OrderService,
    UpdateDataService,
)

from core.config_reader import config
from shared.shared_pharses import CacheTTL
from shared.shared_service_factory import SharedServiceFactory
from services import BotCommandHandler


class ServiceFactory:
    @staticmethod
    async def create_services():
        cache_repo = await SharedServiceFactory.get_cache_repo()
        redis_client = await SharedServiceFactory.get_redis_client()

        bot = Bot(
            token=config.bot_config.token_bot.get_secret_value(),
            default=DefaultBotProperties(parse_mode=ParseMode.HTML),
        )

        command_handler = BotCommandHandler(redis_client=redis_client)

        storage = RedisStorage(
            redis=redis_client,
            state_ttl=CacheTTL.week,
            data_ttl=CacheTTL.week,
        )

        message_service = MessageService(bot=bot)

        cross_table = CrossworldTableRepo(
            cred_file=config.table_config.cred_file.get_secret_value(),
            sheet_url=config.table_config.url_table,
        )

        async_table = AsyncGoogleSheetsService(sheets_service=cross_table)

        order_service = OrderService(
            message_sevrice=message_service,
            cache_repo=cache_repo,
            async_table=async_table,
        )

        cache_service = CacheService(
            cache_repo=cache_repo,
            message_service=message_service,
        )

        cross_service = CrossworldService(
            message_service=message_service,
            cache_service=cache_service,
        )

        update_service = UpdateDataService(
            order_service=order_service,
            cache_repo=cache_repo,
            async_table=async_table,
        )

        cross_service.set_order_service(order_service=order_service)
        cache_service.set_order_service(order_service=order_service)
        order_service.set_cache_service(cache_service=cache_service)
        order_service.set_cross_service(cross_service=cross_service)

        return (
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
        )
