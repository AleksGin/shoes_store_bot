from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from menus import MainMenu


def welcome_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text=MainMenu.calculate_the_cost))
    builder.row(
        KeyboardButton(text=MainMenu.about_delivery),
        KeyboardButton(text=MainMenu.delivery_status),
    )
    builder.row(
        KeyboardButton(text=MainMenu.rates),
        KeyboardButton(text=MainMenu.reviews),
    )
    builder.row(
        KeyboardButton(text=MainMenu.make_order),
        KeyboardButton(text=MainMenu.my_orders),
    )
    builder.row(KeyboardButton(text=MainMenu.instruction))

    return builder.as_markup(resize_keyboard=True)


def to_welcome_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text=MainMenu.back_to_main_menu))

    return builder.as_markup(resize_keyboard=True)
