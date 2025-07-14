from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from phrases import AdminManagementMenu


def admin_managemenet_menu() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(
            text=AdminManagementMenu.add_admin,
            callback_data="add_admin",
        ),
    )
    builder.row(
        InlineKeyboardButton(
            text=AdminManagementMenu.delete_admin,
            callback_data="delete_admin",
        ),
    )
    builder.row(
        InlineKeyboardButton(
            text=AdminManagementMenu.admins_list,
            callback_data="admin_list",
        ),
    )
    
    return builder.as_markup(resize_keyboard=True)