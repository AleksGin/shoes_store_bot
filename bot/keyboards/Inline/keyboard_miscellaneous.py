from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.menus.miscellaneous import Misc


def instruction_button() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text=Misc.instruction_button_text,
            url="https://telegra.ph/Instrukciya-dlya-novichkov-04-18",
        )
    )

    return builder.as_markup()


# def reviews_button() -> InlineKeyboardMarkup:
#     builder = InlineKeyboardBuilder()
#     builder.row(
#         InlineKeyboardButton(text=Misc.reviews, url="https://t.me/crswrld_comment")
#     )

#     return builder.as_markup()


def delivery_button() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text=Misc.delivery_status_order, callback_data="delivery_status_check"
        )
    )

    return builder.as_markup()
