from aiogram import (
    F,
    Router,
)

from phrases import AdminMenu
from aiogram.filters import CommandStart
from aiogram.types import Message
from services import AdminPanelService

admin_handler_router = Router()


@admin_handler_router.message(CommandStart())
async def start_hanlder(
    message: Message,
    admin_service: AdminPanelService,
    is_admin: bool,
) -> None:
    await admin_service.welcome_text(
        message=message,
        is_admin=is_admin,
    )
