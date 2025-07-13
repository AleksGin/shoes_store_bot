from typing import (
    Any,
    Awaitable,
    Callable,
)

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from services import (
    CrossworldService,
    MessageService,
    UpdateDataService,
    OrderService,
    CacheService,
)

from repository import (
    CrossworldTableRepo,
    AsyncGoogleSheetsService,
)
from shared.shared_repos import CacheRepo

class ServiceMiddleware(BaseMiddleware):
    def __init__(
        self,
        cross_service: CrossworldService,
        message_service: MessageService,
        cross_table: CrossworldTableRepo,
        cache_repo: CacheRepo,
        update_service: UpdateDataService,
        async_table: AsyncGoogleSheetsService,
        order_service: OrderService,
        cache_service: CacheService,
    ) -> None:
        self.cross_service = cross_service
        self.message_service = message_service
        self.cross_table = cross_table
        self.cache_repo = cache_repo
        self.update_service = update_service
        self.async_table = async_table
        self.order_service = order_service
        self.cache_service = cache_service

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ):
        data["service"] = self.cross_service
        data["message_service"] = self.message_service
        data["cros_table"] = self.cross_table
        data["cache_repo"] = self.cache_repo
        data["update_service"] = self.update_service
        data["async_table"] = self.async_table
        data["order_service"] = self.order_service
        data["cache_service"] = self.cache_service
        return await handler(event, data)
