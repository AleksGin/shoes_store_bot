from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from phrases import (
    Misc,
    Order,
)


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
            text=Order.inline_button_status_check_text,
            callback_data="delivery_status_check",
        )
    )

    return builder.as_markup(resize_keyboard=True)


def view_another_order_button_if_value() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text=Order.another_delivery_button_status_check_text,
            callback_data="another_delivery_button_status_check",
        ),
    )
    return builder.as_markup(resize_keyboard=True)


def view_another_order_button() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text=Order.another_delivery_button_status_check_text,
            callback_data="another_delivery_button_status_check",
        ),
    )
    builder.row(
        InlineKeyboardButton(
            text=Order.ask_for_track_text,
            callback_data="tracking_on",
        ),
    )

    return builder.as_markup(resize_keyboard=True)


def delete_tracking_orders_buttons() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text=Order.delete_a_specific_one_text,
            callback_data="delete_specific",
        ),
    )
    builder.row(
        InlineKeyboardButton(
            text=Order.delete_all_tracking_orders_text,
            callback_data="delete_all",
        ),
    )

    return builder.as_markup(resize_keyboard=True)


def delete_one_more_button() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text=Order.delete_a_specific_one_more_text,
            callback_data="delete_specific",
        ),
    )

    return builder.as_markup(resize_keyboard=True)
