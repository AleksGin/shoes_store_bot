from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot.fsm.calculation_state import PriceCalculationStates
from bot.images.paths_to_img import PathsImages
from bot.menus.clothes import Clothes
from bot.services.crossworld_service import CrossworldService

router = Router()


@router.callback_query(F.data == "shoes")
async def shoes_button(
    callback: CallbackQuery, service: CrossworldService, state: FSMContext
) -> None:
    await service.calculate(
        callback=callback,
        clothe_name=Clothes.shoes,
        img_path=PathsImages.SHOES_CALCULATE,
        state=state,
    )


@router.callback_query(F.data == "accessories")
async def accessories_button(
    callback: CallbackQuery, service: CrossworldService, state: FSMContext
) -> None:
    await service.calculate(
        callback=callback,
        clothe_name=Clothes.accessories,
        img_path=PathsImages.ACCESSORIES_CALCULATE,
        state=state,
    )


@router.callback_query(F.data == "jackets")
async def jackets_button(
    callback: CallbackQuery, service: CrossworldService, state: FSMContext
) -> None:
    await service.calculate(
        callback=callback,
        clothe_name=Clothes.jackets,
        img_path=PathsImages.JACKETS_CALCULATE,
        state=state,
    )


@router.callback_query(F.data == "hoodi")
async def hoodi_button(
    callback: CallbackQuery, service: CrossworldService, state: FSMContext
) -> None:
    await service.calculate(
        callback=callback,
        clothe_name=Clothes.hoodi,
        img_path=PathsImages.HOODI_CALCULATE,
        state=state,
    )


@router.callback_query(F.data == "t-shirt")
async def t_shirt_button(
    callback: CallbackQuery, service: CrossworldService, state: FSMContext
) -> None:
    await service.calculate(
        callback=callback,
        clothe_name=Clothes.t_shirt,
        img_path=PathsImages.T_SHITS_CALCULATE,
        state=state,
    )


@router.callback_query(F.data == "make_order")
async def make_order_button(
    callback: CallbackQuery, service: CrossworldService, state: FSMContext
) -> None:
    await service.make_order_action(callback=callback, state=state)


@router.callback_query(F.data == "not_make_order")
async def not_make_order_button(
    callback: CallbackQuery, service: CrossworldService, state: FSMContext
) -> None:
    await service.not_make_order_action(callback=callback, state=state)


@router.callback_query(F.data == "calculate_again")
async def calculate_again_button(
    callback: CallbackQuery, service: CrossworldService
) -> None:
    await service.calculate_again_action(callback=callback)


@router.callback_query(F.data == "delivery_status_check")
async def delivery_status_check_button(
    callback: CallbackQuery, service: CrossworldService, state: FSMContext
) -> None:
    await service.callback_delivery_status(callback=callback, state=state)


@router.callback_query(PriceCalculationStates.waiting_for_order_buttons)
async def orders_buttons(
    callback: CallbackQuery, service: CrossworldService, state: FSMContext
) -> None:
    await service.make_order_action(callback=callback, state=state)
