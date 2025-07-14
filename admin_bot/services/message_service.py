from pathlib import Path

from aiogram import Bot
from aiogram.types import (
    FSInputFile,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
)
from aiogram.types.message import Message
from aiogram.fsm.context import FSMContext


class MessageService:
    def __init__(self, bot: Bot) -> None:
        self._sender = bot

    async def send_simple_message(
        self,
        message_text: str,
        chat_id: int,
        keyboard: InlineKeyboardMarkup | ReplyKeyboardMarkup | None = None,
    ) -> None:
        await self._sender.send_message(
            chat_id=chat_id,
            text=message_text,
            reply_markup=keyboard,
        )

    async def send_message_with_image(
        self,
        mesage_text: str,
        chat_id: int,
        path: Path,
        keyboard: ReplyKeyboardMarkup | InlineKeyboardMarkup | None = None,
    ) -> Message:
        return await self._sender.send_photo(
            caption=mesage_text,
            chat_id=chat_id,
            photo=FSInputFile(path=path),
            reply_markup=keyboard,
        )
        
