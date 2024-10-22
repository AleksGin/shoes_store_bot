from aiogram import (
    F,
    Router,
)
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from fsm import (
    OrderStatusState,
    PriceCalculationStates,
)
from menus import (
    MainMenu,
    Order,
)
from services import CrossworldService

router = Router()


@router.message(CommandStart())
async def main_menu_handler(message: Message, service: CrossworldService) -> None:
    await service.welcome_text(message=message)


@router.message(F.text == MainMenu.calculate_the_cost)
async def open_second_menu_handler(
    message: Message, service: CrossworldService
) -> None:
    await service.open_clothes_keyboard(message=message)


@router.message(F.text == MainMenu.back_to_main_menu)
async def to_main_menu_handler(
    message: Message, service: CrossworldService, state: FSMContext
) -> None:
    await service.open_main(message=message, state=state)


@router.message(F.text == MainMenu.instruction)
async def instruction_handler(message: Message, service: CrossworldService) -> None:
    await service.send_rules(message=message)


@router.message(F.text == MainMenu.reviews)
async def reviews_handler(message: Message, service: CrossworldService) -> None:
    await service.send_reviews(message=message)


@router.message(F.text == MainMenu.rates)
async def rate_handler(message: Message, service: CrossworldService) -> None:
    await service.send_rate(message=message)


@router.message(F.text == MainMenu.about_delivery)
async def delivery_info_handler(message: Message, service: CrossworldService) -> None:
    await service.send_delivery_info(message=message)


@router.message(F.text == MainMenu.make_order)
async def make_order_handler(message: Message, service: CrossworldService) -> None:
    await service.make_order(message=message)


@router.message(F.text == MainMenu.delivery_status)
async def delivery_status_handler(
    message: Message, service: CrossworldService, state: FSMContext
) -> None:
    await service.delivery_status_action(message=message, state=state)


@router.message(PriceCalculationStates.waiting_for_amount)
async def input_amount_handler(
    message: Message, service: CrossworldService, state: FSMContext
) -> None:
    await service.process_amount(message=message, state=state)


@router.message(PriceCalculationStates.waiting_for_order_buttons)
async def waiting_order_buttons_hanlder(message: Message) -> None:
    await message.answer(Order.wrong_waiting_for_order_buttons)


@router.message(OrderStatusState.waiting_order_number)
async def process_order_handler(
    message: Message, service: CrossworldService, state: FSMContext
) -> None:
    if message.from_user:
        await service.delivery_status_process(
            message=message,
            state=state,
            user_id=message.from_user.id,
        )
