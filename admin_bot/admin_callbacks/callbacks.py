from aiogram import (
    F,
    Router,
)
from aiogram.types import CallbackQuery

from services.admin_service import AdminPanelService

admin_callback_router = Router()


@admin_callback_router.callback_query(F.data == "change_rate")
async def admin_change_rate_button(
    self,
    callback: CallbackQuery,
    admin_service: AdminPanelService,
): ...


@admin_callback_router.callback_query(F.data == "restart")
async def admin_restart_button(
    self,
    callback: CallbackQuery,
    admin_service: AdminPanelService,
): ...


@admin_callback_router.callback_query(F.data == "statistic")
async def admin_statistic_button(
    self,
    callback: CallbackQuery,
    admin_service: AdminPanelService,
): ...


@admin_callback_router.callback_query(F.data == "admin_control")
async def admin_admin_control_button(callback: CallbackQuery): 
    """Простейший тест без дополнительных параметров"""
    await callback.message.edit_text(
        text="🎯 Простейший callback работает!"
    )