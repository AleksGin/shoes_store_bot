from email import message
from aiogram import Bot
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    CallbackQuery,
    FSInputFile,
)

from pathlib import Path


from bot.menus.clothes import Clothes
from bot.menus.miscellaneous import Misc


class MessageService:
    def __init__(self, bot: Bot):
        self.bot = bot

    async def send_message(
        self,
        message: Message,
        text: str,
        keyboard: InlineKeyboardMarkup | ReplyKeyboardMarkup | None = None,
        disable_web_page_preview: bool = False,
        path: str | Path | None = None,
        chat_id: int | None = None,
    ) -> Message:
        if path:
            return await self.bot.send_photo(
                chat_id or message.chat.id,
                FSInputFile(path=path),
                caption=text,
                reply_markup=keyboard,
            )
        elif not path and message:
            return await message.answer(
                text,
                reply_markup=keyboard,
                disable_web_page_preview=disable_web_page_preview,
            )

    async def callback_action(
        self,
        callback: CallbackQuery,
        clothe_name: str,
        path: str | Path,
        keyboard: ReplyKeyboardMarkup | InlineKeyboardMarkup | None = None,
    ) -> Message:
        await self.bot.edit_message_caption(
            chat_id=callback.from_user.id,
            message_id=callback.message.message_id,
            caption=f"<b>Выбрано: {clothe_name}</b>",
        )
        await self.bot.send_photo(
            callback.from_user.id,
            FSInputFile(path=path),
            reply_markup=keyboard,
        )
        return await self.bot.send_message(callback.from_user.id, Misc.conversion_text)
    
    
    

        # return await self.bot.send_message(callback.from_user.id, Misc.wrong)

    


    # async def send_message(
    #     self,
    #     message: Message,
    #     text: str | None = None,
    #     keyboard: InlineKeyboardMarkup | ReplyKeyboardMarkup | None = None,
    #     disable_web_page_preview: bool = False,
    # ) -> Message:
    #     if text:
    #         return await message.answer(
    #             text,
    #             reply_markup=keyboard,
    #             disable_web_page_preview=disable_web_page_preview,
    #         )
    #     return await message.answer(
    #         "",
    #         reply_markup=keyboard,
    #         disable_web_page_preview=disable_web_page_preview,
    #     )

    # async def send_pic_and_cap(
    #     self,
    #     caption: str,
    #     path: str | Path,
    #     chat_id: int | str,
    #     keyboard: ReplyKeyboardMarkup | InlineKeyboardMarkup | None = None,
    # ) -> Message:
    #     return await self.bot.send_photo(
    #         chat_id=chat_id,
    #         photo=FSInputFile(path=path),
    #         caption=caption,
    #         reply_markup=keyboard,
    #     )
