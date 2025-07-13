from pathlib import Path

from aiogram.types import (
    CallbackQuery,
    Message,
)
from keyboards.reply import to_admin_menu
from images import AdminBotImgs
from keyboards.inline import admin_command_keyboard
from phrases import (
    AdminMenu,
    DefaultPhrases,
)
from aiogram.fsm.context import FSMContext

from services.message_service import MessageService
from shared.shared_pharses import CacheKey
from shared.shared_repos import CacheRepo


class AdminPanelService:
    def __init__(
        self,
        message_service: MessageService,
        cache_repo: CacheRepo,
    ) -> None:
        self._message_service = message_service
        self.cache = cache_repo

    async def welcome_text(self, message: Message) -> None:
        try:
            is_admin = await self.check_is_admin_in_cache(message.from_user.id)

            if is_admin:
                await self._message_service.send_message_with_image(
                    mesage_text=AdminMenu.admin_menu,
                    chat_id=message.chat.id,
                    path=Path(AdminBotImgs.welcome_img),
                    keyboard=admin_command_keyboard(),
                )
        except PermissionError:
            await self._message_service.send_simple_message(
                message_text=DefaultPhrases.permission_error,
                chat_id=message.chat.id,
            )

    async def check_is_admin_in_cache(self, user_id: int) -> bool:
        result = await self.cache.is_admin(
            key=CacheKey.ADMINS_KEY,
            user_id=user_id,
        )
        return result

    async def to_admin_menu(self, chat_id: int) -> None:
        await self._message_service.send_simple_message(
            message_text=AdminMenu.admin_menu,
            chat_id=chat_id,
            keyboard=admin_command_keyboard(),
        )

    async def change_yuan_action(self, callback: CallbackQuery, state: FSMContext):
        current_rate = await self.cache.get_yuan_rate(CacheKey.YUAN_RATE_KEY)

        await self._message_service.send_simple_message(
            message_text=DefaultPhrases.current_rate_in_cache.format(current_rate),
            chat_id=callback.from_user.id,
            keyboard=to_admin_menu(),
        )

    def _filter_rate_action(self, user_message_rate: int | float) -> bool: ...
