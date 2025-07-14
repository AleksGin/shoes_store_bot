from typing import (
    Any,
    Awaitable,
    Callable,
    Dict,
)

from aiogram import BaseMiddleware
from aiogram.types import (
    CallbackQuery,
    Message,
    TelegramObject,
)
from services import (
    AdminPanelService,
    MessageService,
)
from shared.shared_repos import CacheRepo


class AdminMiddleware(BaseMiddleware):
    def __init__(
        self,
        admin_ids: list[int],
        admin_service: AdminPanelService,
        message_service: MessageService,
        cache_repo: CacheRepo,
    ) -> None:
        self.admin_ids = set(admin_ids)
        self.admin_service = admin_service
        self.message_service = message_service
        self.cache_repo = cache_repo

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        if isinstance(event, (Message, CallbackQuery)):
            if event.from_user:
                data["is_admin"] = event.from_user.id in self.admin_ids
            else:
                data["is_admin"] = False
        else:
            data["is_admin"] = False

        data["admin_service"] = self.admin_service
        data["message_service"] = self.message_service
        data["cache_repo"] = self.cache_repo

        return await handler(event, data)
