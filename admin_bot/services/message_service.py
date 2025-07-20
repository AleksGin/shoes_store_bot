from pathlib import Path
from re import A

from aiogram import Bot
from aiogram.types import (
    FSInputFile,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)
from aiogram.types.message import Message


class MessageService:
    def __init__(self, bot: Bot) -> None:
        self._sender = bot

    async def send_simple_message(
        self,
        chat_id: int,
        message_text: str,
        keyboard: InlineKeyboardMarkup | ReplyKeyboardMarkup | None = None,
    ) -> None:
        if message_text:
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
        
    async def remove_keyboard(
        self,
        chat_id: int,
    ) -> None:
        message_to_delete = await self._sender.send_message(
            chat_id=chat_id,
            text=".",
            reply_markup=ReplyKeyboardRemove(),
        )
        
        await self._sender.delete_message(
            chat_id=chat_id,
            message_id=message_to_delete.message_id,
        )
        
