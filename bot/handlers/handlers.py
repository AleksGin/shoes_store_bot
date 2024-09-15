from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.fsm.calculation_state import PriceCalculationStates
from bot.fsm.order_status_state import OrderStatusState
from bot.menus.main_menu import MainMenu
from bot.menus.order import Order
from bot.services.crossworld_service import CrossworldService

router = Router()


@router.message(CommandStart())
async def main_menu_handler(message: Message, service: CrossworldService) -> None:
    await service.welcome_text(message)


@router.message(F.text == MainMenu.calculate_the_cost)
async def open_second_menu_handler(
    message: Message, service: CrossworldService
) -> None:
    await service.open_clothes_keyboard(message)


@router.message(F.text == MainMenu.back_to_main_menu)
async def to_main_menu_handler(
    message: Message, service: CrossworldService, state: FSMContext
) -> None:
    await service.open_main(message, state)


@router.message(F.text == MainMenu.instruction)
async def instruction_handler(message: Message, service: CrossworldService) -> None:
    await service.send_rules(message)


@router.message(F.text == MainMenu.reviews)
async def reviews_handler(message: Message, service: CrossworldService) -> None:
    await service.send_reviews(message)


@router.message(F.text == MainMenu.rates)
async def rate_handler(message: Message, service: CrossworldService) -> None:
    await service.send_rate(message)


@router.message(F.text == MainMenu.about_delivery)
async def delivery_info_handler(message: Message, service: CrossworldService) -> None:
    await service.send_delivery_info(message)


@router.message(F.text == MainMenu.make_order)
async def make_order_handler(message: Message, service: CrossworldService) -> None:
    await service.make_order(message)


@router.message(F.text == MainMenu.delivery_status)
async def delivery_status_handler(
    message: Message, service: CrossworldService, state: FSMContext
) -> None:
    await service.delivery_status_action(message, state)


@router.message(PriceCalculationStates.waiting_for_amount)
async def input_amount_handler(
    message: Message, service: CrossworldService, state: FSMContext
) -> None:
    await service.process_amount(message, state)


@router.message(PriceCalculationStates.waiting_for_order_buttons)
async def waiting_order_buttons_hanlder(message: Message) -> None:
    await message.answer(Order.wrong_waiting_for_order_buttons)


@router.message(OrderStatusState.waiting_order_number)
async def process_order_handler(
    message: Message, service: CrossworldService, state: FSMContext
) -> None:
    await service.delivery_status_process(message, state)
