import logging
from pathlib import Path
from typing import Callable

import aiogram.exceptions
from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery,
    FSInputFile,
    InlineKeyboardMarkup,
    Message,
    ReplyKeyboardMarkup,
)
from phrases import (
    Misc,
    Order,
)


class MessageService:
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    async def send_message(
        self,
        message: Message,
        text: str,
        keyboard: InlineKeyboardMarkup | ReplyKeyboardMarkup | None = None,
        disable_web_page_preview: bool = False,
        path: str | Path | None = None,
        chat_id: int | None = None,
    ) -> Message | None:
        if path:
            await self.bot.send_photo(
                chat_id=chat_id or message.chat.id,
                photo=FSInputFile(path=path),
                caption=text,
                reply_markup=keyboard,
            )
        elif not path and message and text:
            return await message.answer(
                text=text,
                reply_markup=keyboard,
                disable_web_page_preview=disable_web_page_preview,
            )

    async def calculate_callback_action(
        self,
        callback: CallbackQuery,
        path: str | Path,
        clothe_name: str | None = None,
        keyboard: ReplyKeyboardMarkup | InlineKeyboardMarkup | None = None,
    ) -> Message:
        if callback.message is not None:
            await self.bot.edit_message_caption(
                chat_id=callback.from_user.id,
                message_id=callback.message.message_id,
                caption=Misc.selected_type.format(clothe_name),
            )
        return await self.bot.send_photo(
            chat_id=callback.from_user.id,
            photo=FSInputFile(path=path),
            reply_markup=keyboard,
            caption=Order.ask_for_amount_text,
        )

    async def order_handle_callback(
        self,
        callback: CallbackQuery,
        action: Callable | None = None,
        state: FSMContext | None = None,
    ) -> None:
        if isinstance(callback.message, Message):
            await self._delete_message(
                chat_id=callback.from_user.id,
                message_id=callback.message.message_id,
            )

            if state and action:
                await action(callback.message, state)
            elif not state and action:
                await action(callback.message)

    async def notification(
        self,
        user_id: int,
        order_number: str,
        new_status: str,
    ) -> None:
        await self.bot.send_message(
            chat_id=user_id,
            text=Order.notification_about_status_order.format(
                order_number, new_status.split(":")[1]
            ),
        )

    async def hide_keyboard(self, callback: CallbackQuery):
        await self.bot.edit_message_reply_markup(
            message_id=callback.message.message_id,  # type: ignore
            chat_id=callback.from_user.id,
            reply_markup=None,
        )

    async def _delete_message(
        self,
        chat_id: int,
        message_id: int,
    ) -> None:
        try:
            await self.bot.delete_message(
                chat_id=chat_id,
                message_id=message_id,
            )
        except aiogram.exceptions.TelegramBadRequest as e:
            if "message to delete not found" in str(e):
                logging.info(f"error: {e}")
            else:
                logging.info(f"Failed to delete message: {e}")
