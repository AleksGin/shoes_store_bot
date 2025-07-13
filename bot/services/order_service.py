from typing import TYPE_CHECKING

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from fsm import (
    OrderStatusState,
    PriceCalculationStates,
)
from keyboards import (
    view_another_order_button,
    view_another_order_button_if_value,
)
from phrases import CacheKey, Order
from repository import (
    AsyncGoogleSheetsService,
)

from shared.shared_repos import CacheRepo

from .message_service import MessageService

if TYPE_CHECKING:
    from .cache_service import CacheService
    from .crossworld_service import CrossworldService


class OrderService:
    def __init__(
        self,
        message_sevrice: MessageService,
        cache_repo: CacheRepo,
        async_table: AsyncGoogleSheetsService,
    ) -> None:
        self.message_service = message_sevrice
        self.cross_service: "CrossworldService"
        self.cache_repo = cache_repo
        self.async_table = async_table
        self.cache_service: "CacheService"

    def set_cross_service(self, cross_service: "CrossworldService"):
        self.cross_service = cross_service

    def set_cache_service(self, cache_service: "CacheService"):
        self.cache_service = cache_service

    async def make_order_action(
        self,
        callback: CallbackQuery,
        state: FSMContext,
    ) -> None:
        await state.clear()

        await self.message_service.order_handle_callback(callback)

        if isinstance(callback.message, Message):
            await self.message_service.send_message(
                message=callback.message,
                text=Order.make_order_text,
                disable_web_page_preview=True,
            )

    async def not_make_order_action(
        self,
        callback: CallbackQuery,
        state: FSMContext,
    ) -> None:
        await self.message_service.order_handle_callback(
            callback=callback,
            action=self.cross_service.open_main,
            state=state,
        )

    async def delete_tracking_order(
        self,
        callback: CallbackQuery,
        state: FSMContext,
        user_id: int,
        single_order_only: bool = False,
    ) -> None:
        get_all_user_orders = await self.__get_all_track_user_orders(
            user_id=user_id,
        )
        if get_all_user_orders:
            if single_order_only:
                await self.cross_service.delete_process(
                    callback=callback,
                    user_id=user_id,
                    state=state,
                    single_order_only=True,
                )
                await state.set_state(
                    state=OrderStatusState.waiting_order_number_to_delete
                )
            else:
                await self.cross_service.delete_process(
                    callback=callback,
                    user_id=user_id,
                    state=state,
                    single_order_only=False,
                )
        else:
            await self.message_service.send_message(
                message=callback.message,  # type: ignore
                text=Order.empty_tracking_list_text,
            )
            await state.set_state(
                state=OrderStatusState.all_tracker_deleted_notification
            )

    async def notification_to_user(
        self,
        user_id: int,
        order_number: str,
        new_status: str,
    ) -> None:
        await self.message_service.notification(
            user_id=user_id,
            order_number=order_number,
            new_status=new_status,
        )

    async def __get_all_track_user_orders(
        self,
        user_id: int,
    ):
        return await self.cache_repo.get_cached_orders(
            match_form=CacheKey.match_for_user_to_orders.format(user_id)
        )

    async def user_order_process(
        self,
        message: Message,
        state: FSMContext,
    ) -> None:
        user_id = message.from_user.id  # type: ignore
        tracking_keys_for_user = await self.__get_all_track_user_orders(
            user_id=user_id,
        )
        if tracking_keys_for_user:
            await self.cache_service.get_all_user_orders(
                message=message,
                keys=tracking_keys_for_user,
            )
            await state.set_state(
                state=PriceCalculationStates.waiting_for_order_buttons
            )
        else:
            await self.message_service.send_message(
                message=message,
                text=Order.empty_tracking_list_text,
            )

    async def ask_for_new_order_or_track(self, message: Message) -> None:
        await self.message_service.send_message(
            message=message,
            text=Order.ask_for_view_new_order_text,
            keyboard=view_another_order_button(),
        )

    async def new_order_number_process_and_set_into_cache(
        self,
        message: Message,
        search_message: Message,
        order_number: str,
        user_id: int,
        state: FSMContext,
    ) -> None:
        value: int = await self.async_table.async_search_delivery_status(
            data=order_number
        )
        await search_message.delete()
        if value == -1:
            await self.message_service.send_message(
                message=message,
                text=Order.wrong_order_number_text.format(order_number),
                keyboard=view_another_order_button_if_value(),
            )
            await state.set_state(
                state=PriceCalculationStates.waiting_for_order_buttons
            )
        else:
            info = Order.order_number_status_text.format(
                order_number,
                value,
            )
            await self.message_service.send_message(
                message=message,
                text=info,
            )
            await self.cache_service.set_info_into_cache(
                user_id=None,
                order_number=order_number,
                info=info,
                tracking=False,
            )
            await self.ask_for_new_order_or_track(
                message=message,
            )
            await state.update_data(
                user_id=user_id,
                order_number=order_number,
                info=info,
            )

    async def tracking_process(
        self,
        callback: CallbackQuery,
        state: FSMContext,
    ) -> None:
        data = await state.get_data()

        user_id, order_number, info = (
            data["user_id"],
            data["order_number"],
            data["info"],
        )

        check_for_already_tracking = await self.cache_repo.get_info_about_order(
            user_id=user_id,
            order_number=order_number,
            tracking=True,
        )

        if check_for_already_tracking:
            await self.message_service.send_message(
                message=callback.message,  # type: ignore
                text=Order.already_tracking_text,
            )
        else:
            await self.cache_service.set_info_into_cache(
                user_id=user_id,
                order_number=order_number,
                info=info,
                tracking=True,
            )

            await self.message_service.send_message(
                message=callback.message,  # type: ignore
                text=Order.order_tracked_text.format(order_number),
            )
