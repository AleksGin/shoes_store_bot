from aiogram import (
    F,
    Router,
)

from phrases import AdminMenu
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from services import AdminPanelService
from fsm.admin_states import AdminManagementStates

admin_handler_router = Router()


@admin_handler_router.message(CommandStart())
async def start_hanlder(
    message: Message,
    admin_service: AdminPanelService,
) -> None:
    await admin_service.welcome_text(
        message=message,
    )


@admin_handler_router.message(F.text == AdminMenu.back_to_admin_menu)
async def to_admin_menu(
    message: Message,
    admin_service: AdminPanelService,
) -> None:
    await admin_service.to_admin_menu(message=message)


@admin_handler_router.message(AdminManagementStates.waiting_for_rate_input)
async def rate_input_hanlder(
    message: Message,
    admin_service: AdminPanelService,
    state: FSMContext,
) -> None:
    await admin_service.yuan_input_process(
        message=message,
        state=state,
    )


@admin_handler_router.message(AdminManagementStates.waiting_for_date_input)
async def date_input_handler(
    message: Message,
    admin_service: AdminPanelService,
    state: FSMContext,
) -> None:
    await admin_service.change_date_process(
        message=message,
        state=state,
    )


@admin_handler_router.message(AdminManagementStates.waiting_for_add_admin_id)
async def add_admin_id_handler(
    message: Message,
    admin_service: AdminPanelService,
    state: FSMContext,
) -> None:
    await admin_service.add_admin_process(
        message=message,
        state=state,
    )


@admin_handler_router.message(AdminManagementStates.waiting_for_remove_admin_id)
async def remove_admin_id_handler(
    message: Message,
    admin_service: AdminPanelService,
    state: FSMContext,
) -> None:
    await admin_service.delete_admin_process(
        message=message,
        state=state,
    )
