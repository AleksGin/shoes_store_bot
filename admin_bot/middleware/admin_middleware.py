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


class AdminMiddleware(BaseMiddleware):
    def __init__(self, admin_ids: list[int]) -> None:
        self.admin_ids = admin_ids

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

        return await handler(event, data)
