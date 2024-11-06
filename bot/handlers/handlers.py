import logging

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
)
from phrases import Order
from services import (
    CacheService,
    CrossworldService,
    OrderService,
)

router = Router()


@router.message(CommandStart())
async def main_menu_handler(
    message: Message,
    service: CrossworldService,
    state: FSMContext,
) -> None:
    await service.welcome_text(message=message, state=state)


@router.message(F.text == MainMenu.calculate_the_cost)
async def open_second_menu_handler(
    message: Message,
    service: CrossworldService,
) -> None:
    await service.open_clothes_keyboard(message=message)


@router.message(F.text == MainMenu.back_to_main_menu)
async def to_main_menu_handler(
    message: Message,
    service: CrossworldService,
    state: FSMContext,
) -> None:
    await service.open_main(message=message, state=state)


@router.message(F.text == MainMenu.instruction)
async def instruction_handler(
    message: Message,
    service: CrossworldService,
) -> None:
    await service.send_rules(message=message)


@router.message(F.text == MainMenu.reviews)
async def reviews_handler(
    message: Message,
    service: CrossworldService,
) -> None:
    await service.send_reviews(message=message)


@router.message(F.text == MainMenu.rates)
async def rate_handler(
    message: Message,
    service: CrossworldService,
) -> None:
    await service.send_rate(message=message)


@router.message(F.text == MainMenu.about_delivery)
async def delivery_info_handler(
    message: Message,
    service: CrossworldService,
) -> None:
    await service.send_delivery_info(message=message)


@router.message(F.text == MainMenu.make_order)
async def make_order_handler(
    message: Message,
    service: CrossworldService,
) -> None:
    await service.make_order(message=message)


@router.message(F.text == MainMenu.delivery_status)
async def delivery_status_handler(
    message: Message,
    service: CrossworldService,
    state: FSMContext,
) -> None:
    await service.delivery_status_action(message=message, state=state)


@router.message(F.text == MainMenu.my_orders)
async def my_orders_handler(
    message: Message,
    order_service: OrderService,
    state: FSMContext,
) -> None:
    logging.info("перешел в router.message MainMenu.my_orders")
    await order_service.user_order_process(
        message=message,
        state=state,
    )


@router.message(PriceCalculationStates.waiting_for_amount)
async def input_amount_handler(
    message: Message,
    service: CrossworldService,
    state: FSMContext,
) -> None:
    await service.process_amount(message=message, state=state)


@router.message(PriceCalculationStates.waiting_for_order_buttons)
async def waiting_order_buttons_hanlder(message: Message) -> None:
    await message.answer(text=Order.wrong_waiting_for_order_buttons)


@router.message(OrderStatusState.waiting_order_number_to_delete)
async def delete_process_handler(
    message: Message,
    cache_service: CacheService,
    state: FSMContext,
):
    await cache_service.delete_one(
        message=message,
        state=state,
        user_id=message.from_user.id,  # type: ignore
    )


@router.message(OrderStatusState.waiting_order_number)
async def process_order_handler(
    message: Message,
    service: CrossworldService,
    state: FSMContext,
) -> None:
    if message.from_user:
        await service.delivery_status_process(
            message=message,
            state=state,
            user_id=message.from_user.id,
        )


@router.message(OrderStatusState.waiting_for_press_tracker_button)
async def waiting_tracker_button_handler(message: Message) -> None:
    await message.answer(text=Order.wrong_waiting_for_tracker_button_)


@router.message(OrderStatusState.all_tracker_deleted_notification)
async def all_tracker_deleted_handler(message: Message) -> None:
    await message.answer(text=Order.all_tracker_deleted_notification_text)
