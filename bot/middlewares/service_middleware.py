from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from bot.services.crossworld_service import CrossworldService
from bot.services.google_sheets_service import CrossworldTable
from bot.services.message_service import MessageService


class ServiceMiddleware(BaseMiddleware):
    def __init__(
        self,
        cross_service: CrossworldService,
        message_service: MessageService,
        cross_table: CrossworldTable,
    ) -> None:
        self.cross_service = cross_service
        self.message_service = message_service
        self.cross_table = cross_table

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ):
        data["service"] = self.cross_service
        data["message_service"] = self.message_service
        data["cros_table"] = self.cross_table

        return await handler(event, data)
