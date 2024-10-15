from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from menus import Misc


def instruction_button() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text=Misc.instruction_button_text,
            url="",  # LINK
        )
    )

    return builder.as_markup(resize_keyboard=True)


def inline_delivery_button() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text=Misc.inline_button_status_check_text,
            callback_data="delivery_status_check",
        )
    )

    return builder.as_markup(resize_keyboard=True)
