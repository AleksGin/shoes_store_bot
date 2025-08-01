from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from menus import Clothes


def keyboard_clothes() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text=Clothes.shoes, callback_data="shoes"),
        InlineKeyboardButton(text=Clothes.accessories, callback_data="accessories"),
    )
    builder.row(InlineKeyboardButton(text=Clothes.hoodi, callback_data="hoodi"))
    builder.row(InlineKeyboardButton(text=Clothes.t_shirt, callback_data="t-shirt"))
    builder.row(InlineKeyboardButton(text=Clothes.jackets, callback_data="jackets"))
    builder.row(InlineKeyboardButton(text=Clothes.bags_and_backpacks, callback_data="bags"))
    builder.row(InlineKeyboardButton(text=Clothes.sports_equipment, callback_data="sports_eq"))

    return builder.as_markup(resize_keyboard=True)
