import time
import logging
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
from shared.shared_pharses import CacheKey
from phrases import DefaultPhrases


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
        self.denied_users = {}

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        if isinstance(event, (Message, CallbackQuery)):
            if event.from_user:
                user_id = event.from_user.id
            
                
                try:
                    is_admin = await self.cache_repo.is_admin(
                        CacheKey.ADMINS_KEY,
                        user_id,
                    )
                except Exception:
                    is_admin = user_id in self.admin_ids

                if not is_admin:
                    await self._send_access_denied_message(event)
                    return 
                else:
                    data["is_admin"] = is_admin
            else:
                data["is_admin"] = False
        else:
            data["is_admin"] = False

        data["admin_service"] = self.admin_service
        data["message_service"] = self.message_service
        data["cache_repo"] = self.cache_repo

        return await handler(event, data)

    async def _send_access_denied_message(self, event):
        user_id = event.from_user.id
        current_time = time.time()

        if user_id in self.denied_users:
            last_denied = self.denied_users[user_id]
            if current_time - last_denied < 60:
                return

        self.denied_users[user_id] = current_time

        try:
            if isinstance(event, Message):
                await event.answer(
                    text=DefaultPhrases.permission_error,
                )
            elif isinstance(event, CallbackQuery):
                await event.answer(text="🚫 Доступ запрещен", show_alert=True)
        except Exception as e:
            logging.error(f"Failed to send access denied message: {e}")
