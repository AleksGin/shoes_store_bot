from aiogram import (
    F,
    Router,
)
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from services.admin_service import AdminPanelService

admin_callback_router = Router()


@admin_callback_router.callback_query(F.data == "change_rate")
async def admin_change_rate_button(
    callback: CallbackQuery,
    admin_service: AdminPanelService,
    state: FSMContext,
) -> None:
    await admin_service.change_rate_action(
        callback=callback,
        state=state,
    )


@admin_callback_router.callback_query(F.data == "change_date")
async def admin_change_date_button(
    callback: CallbackQuery,
    admin_service: AdminPanelService,
    state: FSMContext,
) -> None:
    await admin_service.change_date_action(
        callback=callback,
        state=state,
    )


@admin_callback_router.callback_query(F.data == "restart")
async def admin_restart_button(
    callback: CallbackQuery,
    admin_service: AdminPanelService,
): 
    await admin_service.restart_cros_bot_action(callback)


@admin_callback_router.callback_query(F.data == "statistic")
async def admin_statistic_button(
    callback: CallbackQuery,
    admin_service: AdminPanelService,
) -> None:
    await admin_service.get_admin_logs(callback=callback)


@admin_callback_router.callback_query(F.data == "admin_control")
async def admin_admin_control_button(
    callback: CallbackQuery,
    admin_service: AdminPanelService,
) -> None:
    await admin_service.open_admin_control(callback=callback)


@admin_callback_router.callback_query(F.data == "to_admin_menu")
async def to_admin_menu_button(
    callback: CallbackQuery,
    admin_service: AdminPanelService,
) -> None:
    await admin_service.to_admin_menu(callback=callback)


@admin_callback_router.callback_query(F.data == "add_admin")
async def add_admin_button(
    callback: CallbackQuery,
    admin_service: AdminPanelService,
    state: FSMContext,
) -> None:
    await admin_service.add_admin_action(
        callback=callback,
        state=state,
    )


@admin_callback_router.callback_query(F.data == "delete_admin")
async def delete_admin_button(
    callback: CallbackQuery,
    admin_service: AdminPanelService,
    state: FSMContext,
) -> None:
    await admin_service.delete_admin_action(
        callback=callback,
        state=state,
    )


@admin_callback_router.callback_query(F.data == "admin_list")
async def admin_list_button(
    callback: CallbackQuery,
    admin_service: AdminPanelService,
) -> None:
    await admin_service.get_admin_ids(callback=callback)
