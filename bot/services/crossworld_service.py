from aiogram import Bot
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from bot.keyboards.Inline.keyboard_clothes import keyboard_clothes
from bot.keyboards.Inline.keyboard_miscellaneous import (
    delivery_button,
    instruction_button,
)
from bot.keyboards.reply.start_keyboard import to_welcome_keyboard, welcome_keyboard
from bot.menus.main_menu import MainMenu
from bot.menus.miscellaneous import Misc
from bot.services.message_service import MessageService
from bot.images.paths_to_img import PathsImages
from bot.menus.clothes import Clothes


class CrossworldService:
    def __init__(self, message_service: MessageService, bot: Bot) -> None:
        self.message_service = message_service
        self.bot = bot

    async def calculate(
        self,
        callback: CallbackQuery,
        clothe_name: str,
        img_path: str,
    ) -> Message:
        return await self.message_service.callback_action(
            callback,
            clothe_name,
            img_path,
            to_welcome_keyboard(),
        )

    async def send_rules(self, message: Message) -> Message:
        await self.message_service.send_message(
            message, Misc.instruction_text, instruction_button()
        )
        return await self.open_main(message)

    async def send_reviews(self, message: Message) -> Message:
        await self.message_service.send_message(
            message,
            Misc.reviews_and_link,
            path=PathsImages.REVIEWS_QR,
            chat_id=message.chat.id,
        )
        return await self.open_main(message)

    async def send_rate(self, message: Message) -> Message:
        # await self.message_service.send_pic("*фото с юанем*", message)
        await self.message_service.send_message(
            message,
            Misc.today_rate_text,
            path=PathsImages.YUAN_RATES,
            chat_id=message.chat.id,
        )
        return await self.open_main(message)

    async def send_delivery_info(self, message: Message) -> Message:
        await self.message_service.send_message(
            message,
            Misc.about_delivery,
            delivery_button(),
            path=PathsImages.DELIVERY,
            chat_id=message.chat.id,
        )
        return await self.open_main(message)

    async def make_order(self, message: Message):
        await self.message_service.send_message(
            message, Misc.make_order_text, disable_web_page_preview=True
        )
        return await self.open_main(message)

    async def welcome_text(self, message: Message) -> Message:
        await self.message_service.send_message(
            message,
            Misc.welcome_text,
            path=PathsImages.WELCOME_CROS,
            chat_id=message.chat.id,
        )
        return await self.open_main(message)

    async def open_main(self, message: Message) -> Message:
        return await self.message_service.send_message(
            message, MainMenu.main_menu, welcome_keyboard()
        )

    async def open_clothes_keyboard(self, message: Message) -> Message:
        return await self.message_service.send_message(
            message,
            Misc.choose_type,
            keyboard_clothes(),
            path=PathsImages.SECOND_MENU_IMG_PATH,
            chat_id=message.chat.id,
        )

    async def calculate_func(self, message: int, clothe_name: str):
        if clothe_name == Clothes.shoes:
            return message + 2
