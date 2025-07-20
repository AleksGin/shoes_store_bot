import asyncio
from typing import TYPE_CHECKING

from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery,
    Message,
)
from fsm import OrderStatusState
from images import PathsImages
from keyboards import (
    delete_one_more_button,
    delete_tracking_orders_buttons,
    to_welcome_keyboard,
)
from shared.shared_pharses import CacheKey
from phrases import Order
from shared.shared_repos import CacheRepo

from .message_service import MessageService

if TYPE_CHECKING:
    from .order_service import OrderService


class CacheService:
    def __init__(
        self,
        cache_repo: CacheRepo,
        message_service: MessageService,
    ) -> None:
        self.cache_repo = cache_repo
        self.message_service = message_service
        self.order_service: "OrderService"

    def set_order_service(self, order_service: "OrderService") -> None:
        self.order_service = order_service
        
    async def get_rate_from_cache(self) -> float:
        
        result = await self.cache_repo.get_yuan_rate(CacheKey.YUAN_RATE_KEY)
        return result
    
    async def get_closest_date(self) -> str:
        result = await self.cache_repo.get_closest_date(CacheKey.CLOSEST_DATE_KEY)
        return result

    async def set_info_into_cache(
        self,
        user_id: int | None,
        order_number: str,
        info: str,
        tracking: bool,
    ) -> None:
        set_into_cache = await self.cache_repo.set_order_status(
            user_id=user_id,
            order_number=order_number,
            info=info,
            tracking=tracking,
        )
        return set_into_cache

    async def check_info_in_cache(
        self,
        order_number: str,
    ):
        check_cache = await self.cache_repo.get_info_about_order(
            order_number=order_number,
        )
        return check_cache

    async def getting_process_info_from_cache(
        self,
        message: Message,
        info_from_cache: str,
        search_message: Message,
    ) -> None:
        await asyncio.sleep(0.35)
        await search_message.delete()
        await self.message_service.send_message(
            message=message,
            text=info_from_cache,
        )
        await self.order_service.ask_for_new_order_or_track(
            message=message,
        )

    async def delete_one(
        self,
        message: Message,
        state: FSMContext,
        user_id: int,
    ) -> None:
        try:
            if message.text is not None:
                order_number = int(message.text)
                delete = await self.cache_repo.delete_tracking_orders(
                    user_id=user_id,
                    order_number=str(order_number),
                    single_order_only=True,
                )
                if delete:
                    await self.message_service.send_message(
                        message=message,
                        text=Order.specific_order_deleted_text.format(order_number),
                        keyboard=delete_one_more_button(),
                    )
                    await state.set_state(
                        state=OrderStatusState.waiting_for_press_tracker_button
                    )
                else:
                    await self.message_service.send_message(
                        message=message,
                        text=Order.delete_order_error,
                    )
        except Exception:
            await self.message_service.send_message(
                message=message,
                text=Order.wrong_value_order_number_for_delete,
            )

    async def delete_all(
        self,
        callback: CallbackQuery,
        state: FSMContext,
        user_id: int,
    ) -> None:
        await self.cache_repo.delete_tracking_orders(
            user_id=user_id,
            single_order_only=False,
        )
        await self.message_service.send_message(
            message=callback.message,  # type: ignore
            text=Order.all_orders_deleted_text,
        )
        await state.set_state(state=OrderStatusState.all_tracker_deleted_notification)

    async def get_all_user_orders(
        self,
        message: Message,
        keys,
    ) -> None:
        keys = [key.decode("utf-8") for key in keys]

        order_info_list = await self.cache_repo.get_multiple_order_infos(keys=keys)

        if order_info_list:
            messages = [
                Order.tracking_list_for_user.format(
                    key.split(":")[3], info.split(":")[1]
                )
                for key, info in zip(keys, order_info_list)
                if info is not None
            ]
            response_text = Order.count_tracking_orders.format(len(keys)) + "\n\n".join(
                messages
            )
        else:
            response_text = Order.tracking_list_error

        await self.message_service.send_message(
            message=message,
            text=response_text,
            keyboard=delete_tracking_orders_buttons(),
            path=PathsImages.MY_ORDERS,
        )
        await self.message_service.send_message(
            message=message,
            text=Order.text_about_tracking_orders,
            keyboard=to_welcome_keyboard(),
        )
