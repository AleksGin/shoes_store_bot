from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from phrases import Order


def ask_for_order_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(
            text=Order.agree_order_text,
            callback_data="make_order",
        ),
        InlineKeyboardButton(
            text=Order.not_agree_order_text,
            callback_data="not_make_order",
        ),
    )
    builder.row(
        InlineKeyboardButton(
            text=Order.calculate_again_text,
            callback_data="calculate_again",
        ),
    )

    return builder.as_markup(resize_keyboard=True)


