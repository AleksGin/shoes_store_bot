from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from phrases import AdminMenu


def admin_command_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(
            text=AdminMenu.change_rate,
            callback_data="change_rate",
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=AdminMenu.change_closest_date,
            callback_data="change_date",
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=AdminMenu.restart_bot,
            callback_data="restart",
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=AdminMenu.statistics,
            callback_data="statistic",
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=AdminMenu.control_admins,
            callback_data="admin_control",
        )
    )

    return builder.as_markup(resize_keyboard=True)
