from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from phrases import (
    AdminManagementMenu,
    AdminMenu,
)


def admin_managemenet_menu(show_list_button: bool = True) -> InlineKeyboardMarkup:
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
    
    if show_list_button:
        builder.row(
            InlineKeyboardButton(
                text=AdminManagementMenu.admins_list,
                callback_data="admin_list",
            ),
        )
    
    builder.row(
        InlineKeyboardButton(
            text=AdminMenu.back_to_admin_menu,
            callback_data="to_admin_menu",
        ),
    )

    return builder.as_markup(resize_keyboard=True)

