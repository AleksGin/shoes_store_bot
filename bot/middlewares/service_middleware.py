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
)

from repository import (
    CrossworldTableRepo,
    CacheRepo,
)


class ServiceMiddleware(BaseMiddleware):
    def __init__(
        self,
        cross_service: CrossworldService,
        message_service: MessageService,
        cross_table: CrossworldTableRepo,
        cache_repo: CacheRepo,
    ) -> None:
        self.cross_service = cross_service
        self.message_service = message_service
        self.cross_table = cross_table
        self.cache_repo = cache_repo

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

        return await handler(event, data)
