from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.images.paths_to_img import PathsImages
from bot.keyboards.Inline.keyboard_clothes import keyboard_clothes
from bot.keyboards.reply.start_keyboard import to_welcome_keyboard, welcome_keyboard
from bot.menus.clothes import Clothes
from bot.menus.main_menu import MainMenu
from bot.services.crossworld_service import CrossworldService

router = Router()


@router.callback_query(F.data == "shoes")
async def trying(callback: CallbackQuery, service: CrossworldService):
    await service.calculate(callback, Clothes.shoes, PathsImages.SHOES_CALCULATE)


# @router.callback_query(F.data == "")
# @router.callback_query(F.data == "delivery_status_check")
# async def delivery_status_check(callback: CallbackQuery, service: CrossworldService):
#     await service._inline_delivery_buttion(callback)


# @router.callback_query(F.data == "accessories")
