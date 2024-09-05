from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.keyboards.Inline.keyboard_clothes import keyboard_clothes
from bot.keyboards.reply.start_keyboard import to_welcome_keyboard, welcome_keyboard
from bot.menus.clothes import Clothes
from bot.menus.main_menu import MainMenu
from bot.menus.miscellaneous import Misc
from bot.services.message_service import MessageService
from bot.services.crossworld_service import CrossworldService

router = Router()


@router.message(CommandStart())
async def main_menu(message: Message, service: CrossworldService):
    await service.welcome_text(message)


@router.message(F.text == MainMenu.calculate_the_cost)
async def open_second_menu(message: Message, service: CrossworldService):
    await service.open_clothes_keyboard(message)


@router.message(F.text == MainMenu.back_to_main_menu)
async def to_main_menu(message: Message, service: CrossworldService):
    await service.open_main(message)


@router.message(F.text == MainMenu.instruction)
async def instruction(message: Message, service: CrossworldService):
    await service.send_rules(message)


@router.message(F.text == MainMenu.reviews)
async def reviews(message: Message, service: CrossworldService):
    await service.send_reviews(message)


@router.message(F.text == MainMenu.rates)
async def rates(message: Message, service: CrossworldService):
    await service.send_rate(message)


@router.message(F.text == MainMenu.about_delivery)
async def delivery(message: Message, service: CrossworldService):
    await service.send_delivery_info(message)


@router.message(F.text == MainMenu.make_order)
async def order(message: Message, service: CrossworldService):
    await service.make_order(message)


@router.message(F.int)
async def input_amount(message: Message, service: CrossworldService, clothe_name: str):
    try:
        amount = int(message.text)
    except ValueError:
        await message.reply("Пожалуйста, введите корректное число.")
        return

    await service.calculate_func(amount, clothe_name)
