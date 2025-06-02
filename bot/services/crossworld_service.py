import asyncio
from typing import TYPE_CHECKING

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from fsm import (
    OrderStatusState,
    PriceCalculationStates,
)
from images import PathsImages
from keyboards import (
    ask_for_order_keyboard,
    inline_delivery_button,
    instruction_button,
    keyboard_clothes,
    to_welcome_keyboard,
    welcome_keyboard,
)
from menus import (
    ClothesPrice,
    MainMenu,
)
from phrases import (
    Misc,
    Order,
)

from .cache_service import CacheService
from .message_service import MessageService

if TYPE_CHECKING:
    from .order_service import OrderService


class CrossworldService:
    def __init__(
        self,
        message_service: MessageService,
        cache_service: CacheService,
    ) -> None:
        self.message_service = message_service
        self.order_service: "OrderService"
        self.cache_service = cache_service

    def set_order_service(self, order_service: "OrderService"):
        self.order_service = order_service

    async def calculate(
        self,
        callback: CallbackQuery,
        clothe_name: str,
        img_path: str,
        state: FSMContext,
    ):
        data = await state.get_data()

        if "clothe_name" in data:
            await self.message_service.send_message(
                message=callback.message,  # type: ignore
                text=Misc.menu_error,
            )
            return

        await self.message_service.calculate_callback_action(
            callback=callback,
            path=img_path,
            clothe_name=clothe_name,
            keyboard=to_welcome_keyboard(),
        )
        await state.set_state(state=PriceCalculationStates.waiting_for_amount)
        await state.update_data(clothe_name=clothe_name)

    async def send_rules(self, message: Message) -> Message | None:
        await self.message_service.send_message(
            message=message,
            text=Misc.instruction_text,
            keyboard=instruction_button(),
        )
        return await self.open_main(message=message)

    async def send_reviews(self, message: Message) -> Message | None:
        await self.message_service.send_message(
            message=message,
            text=Misc.reviews_and_link,
            path=PathsImages.REVIEWS_QR,
            chat_id=message.chat.id,
        )
        return await self.open_main(message=message)

    async def send_rate(self, message: Message) -> Message | None:
        await self.message_service.send_message(
            message=message,
            text=Misc.today_rate_text,
            path=PathsImages.YUAN_RATES,
            chat_id=message.chat.id,
        )
        return await self.open_main(message=message)

    async def send_delivery_info(self, message: Message) -> Message | None:
        await self.message_service.send_message(
            message=message,
            text=Misc.about_delivery,
            keyboard=inline_delivery_button(),
            path=PathsImages.DELIVERY,
            chat_id=message.chat.id,
        )
        return await self.open_main(message=message)

    async def make_order(self, message: Message) -> Message | None:
        return await self.message_service.send_message(
            message=message,
            text=Order.make_order_text,
            keyboard=to_welcome_keyboard(),
            disable_web_page_preview=True,
        )

    async def welcome_text(self, message: Message, state: FSMContext) -> Message | None:
        await state.clear()
        await self.message_service.send_message(
            message=message,
            text=Misc.welcome_text,
            path=PathsImages.WELCOME_CROS,
            chat_id=message.chat.id,
        )
        return await self.open_main(message=message)

    async def open_main(
        self,
        message: Message,
        state: FSMContext | None = None,
    ) -> Message | None:
        if state:
            await state.clear()
        return await self.message_service.send_message(
            message=message,
            text=MainMenu.main_menu,
            keyboard=welcome_keyboard(),
        )

    async def open_clothes_keyboard(self, message: Message) -> Message | None:
        return await self.message_service.send_message(
            message=message,
            text=Misc.choose_type,
            keyboard=keyboard_clothes(),
            path=PathsImages.SECOND_MENU_IMG_PATH,
            chat_id=message.chat.id,
        )

    async def process_amount(
        self,
        message: Message,
        state: FSMContext,
    ) -> None | Message:
        user_data = await state.get_data()
        clothe_name = user_data.get("clothe_name")

        if clothe_name is None:
            await self.message_service.send_message(
                message=message,
                text=Misc.wrong,
            )
            return
        try:
            if message.text is not None:
                amount = int(message.text)
                await self.__calculate_process(
                    message=message,
                    state=state,
                    amount=amount,
                    clothe_name=clothe_name,
                )
        except ValueError:
            return await self.message_service.send_message(
                message=message,
                text=Order.wrong_value_text,
            )

    async def calculate_again_action(
        self,
        callback: CallbackQuery,
        state: FSMContext,
    ) -> None:
        await state.clear()
        await self.message_service.order_handle_callback(
            callback=callback,
            action=self.open_clothes_keyboard,
        )

    async def callback_delivery_status(
        self,
        callback: CallbackQuery,
        state: FSMContext,
    ) -> None:
        data = await state.get_data()
        if data.get("check_action"):
            await self.message_service.send_message(
                message=callback.message,  # type: ignore
                text=Misc.status_action_error,
            )
            return
        await self.message_service.order_handle_callback(
            callback=callback,
            action=self.delivery_status_action,
            state=state,
        )
        await state.update_data(check_action=True)

    async def delivery_status_action(
        self,
        message: Message,
        state: FSMContext,
    ) -> None:
        data = await state.get_data()
        if not data.get("photo_sent"):
            await self.message_service.send_message(
                message=message,
                text=Order.ask_for_order_number_text,
                keyboard=to_welcome_keyboard(),
                path=PathsImages.DELIVERY_STATUS,
                chat_id=message.chat.id,
            )
            await state.update_data(
                photo_sent=True,
                check_action=True,
            )
        else:
            await self.message_service.send_message(
                message=message,
                text=Order.ask_for_order_number_text,
                keyboard=to_welcome_keyboard(),
                chat_id=message.chat.id,
            )

        await state.set_state(state=OrderStatusState.waiting_order_number)

    async def delivery_status_process(
        self,
        message: Message,
        state: FSMContext,
        user_id: int,
    ) -> Message | None:
        if message.text is not None and message.text.isdigit():
            order_number = message.text
            get_info_from_cache = await self.cache_service.check_info_in_cache(
                order_number=order_number,
            )
            

            search_message = await self.message_service.send_message(
                message=message,
                text=Order.search_order_text,
            )

            if get_info_from_cache:
                await self.cache_service.getting_process_info_from_cache(
                    message=message,
                    info_from_cache=get_info_from_cache,
                    search_message=search_message,  # type: ignore
                )
                await state.update_data(
                    user_id=user_id,
                    order_number=order_number,
                    info=get_info_from_cache,
                )
            else:
                await self.order_service.new_order_number_process_and_set_into_cache(
                    message=message,
                    search_message=search_message,  # type: ignore
                    order_number=order_number,
                    user_id=user_id,
                    state=state,
                )

            await state.set_state(
                state=PriceCalculationStates.waiting_for_order_buttons
            )
        else:
            return await self.message_service.send_message(
                message=message,
                text=Order.wrong_value_order_number_text,
            )

    async def __calculate_process(
        self,
        message: Message,
        state: FSMContext,
        amount: int,
        clothe_name: str,
    ) -> Message | None:
        if amount > 0:
            fixed_price = ClothesPrice.clothes_prices.get(clothe_name)
            delivery_price = ClothesPrice.clothes_delivery_price.get(clothe_name)
            comission = ClothesPrice.clothes_commission.get(clothe_name)

            if fixed_price:
                result = (amount * Misc.rate) + fixed_price

            calculating_message = await self.message_service.send_message(
                message=message,
                text=Order.calculating_process_text,
            )
            await asyncio.sleep(delay=1)
            await calculating_message.delete()
            await self.message_service.send_message(
                message=message,
                text=Order.total_amount.format(
                    int(result),
                    delivery_price,
                    comission,
                ),
            )
            await self.message_service.send_message(
                message=message,
                text=Order.ask_for_order_text,
                keyboard=ask_for_order_keyboard(),
            )
            await state.set_state(
                state=PriceCalculationStates.waiting_for_order_buttons
            )
        else:
            return await self.message_service.send_message(
                message=message,
                text=Order.wrong_less_then_0_text,
            )

    async def delete_process(
        self,
        callback: CallbackQuery,
        user_id: int,
        state: FSMContext,
        single_order_only: bool = False,
    ) -> None:
        if isinstance(callback.message, Message):
            if single_order_only:
                await self.message_service.hide_keyboard(callback=callback)
                await self.message_service.send_message(
                    message=callback.message,
                    text=Order.ask_for_order_number_to_delete,
                )
                await state.set_state(
                    state=OrderStatusState.waiting_order_number_to_delete
                )
            else:
                await self.message_service.hide_keyboard(callback=callback)
                await self.cache_service.delete_all(
                    callback=callback,
                    user_id=user_id,
                    state=state,
                )
