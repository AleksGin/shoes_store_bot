import asyncio
import logging

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
    Misc,
    Order,
)
from repository import (
    CacheRepo,
    CrossworldTableRepo,
)

from .message_service import MessageService


class CrossworldService:
    def __init__(
        self,
        message_service: MessageService,
        cross_table: CrossworldTableRepo,
        cache_repo: CacheRepo,
    ) -> None:
        self.message_service = message_service
        self.cross_table = cross_table
        self.cache_repo = cache_repo

    async def calculate(
        self,
        callback: CallbackQuery,
        clothe_name: str,
        img_path: str,
        state: FSMContext,
    ) -> None:
        await self.message_service.calculate_callback_action(
            callback=callback,
            path=img_path,
            clothe_name=clothe_name,
            keyboard=to_welcome_keyboard(),
        )
        await state.set_state(state=PriceCalculationStates.waiting_for_amount)

        await state.update_data(clothe_name=clothe_name)

    async def send_rules(self, message: Message) -> Message:
        await self.message_service.send_message(
            message=message,
            text=Misc.instruction_text,
            keyboard=instruction_button(),
        )
        return await self.open_main(message=message)

    async def send_reviews(self, message: Message) -> Message:
        await self.message_service.send_message(
            message=message,
            text=Misc.reviews_and_link,
            path=PathsImages.REVIEWS_QR,
            chat_id=message.chat.id,
        )
        return await self.open_main(message=message)

    async def send_rate(self, message: Message) -> Message:
        await self.message_service.send_message(
            message=message,
            text=Misc.today_rate_text,
            path=PathsImages.YUAN_RATES,
            chat_id=message.chat.id,
        )
        return await self.open_main(message=message)

    async def send_delivery_info(self, message: Message) -> Message:
        await self.message_service.send_message(
            message=message,
            text=Misc.about_delivery,
            keyboard=inline_delivery_button(),
            path=PathsImages.DELIVERY,
            chat_id=message.chat.id,
        )
        return await self.open_main(message=message)

    async def make_order(self, message: Message) -> Message:
        return await self.message_service.send_message(
            message=message,
            text=Order.make_order_text,
            keyboard=to_welcome_keyboard(),
            disable_web_page_preview=True,
        )

    async def welcome_text(self, message: Message) -> Message:
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
    ) -> Message:
        if state:
            await state.clear()
        return await self.message_service.send_message(
            message=message,
            text=MainMenu.main_menu,
            keyboard=welcome_keyboard(),
        )

    async def open_clothes_keyboard(self, message: Message) -> Message:
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

    async def make_order_action(
        self, callback: CallbackQuery, state: FSMContext
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
            action=self.open_main,
            state=state,
        )

    async def calculate_again_action(self, callback: CallbackQuery) -> None:
        await self.message_service.order_handle_callback(
            callback=callback,
            action=self.open_clothes_keyboard,
        )

    async def callback_delivery_status(
        self,
        callback: CallbackQuery,
        state: FSMContext,
    ) -> None:
        await self.message_service.order_handle_callback(
            callback=callback,
            action=self.delivery_status_action,
            state=state,
        )

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
            await state.update_data(photo_sent=True)
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
            get_info_from_cache = await self.__check_info_in_cache(
                user_id=user_id,
                order_number=order_number,
            )

            search_message = await self.message_service.send_message(
                message=message,
                text=Order.search_order_text,
            )

            if get_info_from_cache:
                check_for_actual = await self.__is_cache_actual(
                    order_number=order_number,
                    cached_info=get_info_from_cache,
                )
                if check_for_actual:
                    await self.__getting_process_info_from_cache(
                        message=message,
                        info_from_cache=get_info_from_cache,
                        search_message=search_message,
                    )
            else:
                await self.__new_order_number_process_and_set_into_cache(
                    message=message,
                    search_message=search_message,
                    order_number=order_number,
                    user_id=user_id,
                    state=state,
                )
            logging.info("Установил state")
            await state.set_state(
                state=PriceCalculationStates.waiting_for_order_buttons
            )
        else:
            return await self.message_service.send_message(
                message=message,
                text=Order.wrong_value_order_number_text,
            )

    async def __is_cache_actual(self, order_number: str, cached_info: str):
        actual = self.cross_table.search_delivery_status(data=order_number)

        if str(actual) in cached_info:
            return True
        return False

    async def __set_info_to_cache(
        self,
        user_id: int,
        order_number: str,
        info: str,
    ) -> None:
        set_info = await self.cache_repo.set_info_about_order_by_user_id(
            user_id=user_id,
            order_number=order_number,
            info=info,
        )
        return set_info

    async def __check_info_in_cache(
        self,
        user_id: int,
        order_number: str,
    ):
        check_cache = await self.cache_repo.get_info_about_order_by_user_id(
            user_id=user_id,
            order_number=order_number,
        )
        return check_cache

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

    async def __getting_process_info_from_cache(
        self,
        message: Message,
        info_from_cache: str,
        search_message: Message,
    ):
        await asyncio.sleep(0.6)
        await search_message.delete()
        await self.message_service.send_message(
            message=message,
            text=info_from_cache,
        )
        await self.message_service.send_message(
            message=message,
            text=Order.ask_for_view_new_order_text,
            keyboard=inline_delivery_button(),
        )

    async def __new_order_number_process_and_set_into_cache(
        self,
        message: Message,
        search_message: Message,
        order_number: str,
        user_id: int,
        state: FSMContext,
    ):
        value = self.cross_table.search_delivery_status(data=order_number)
        await search_message.delete()
        if value == -1:
            await self.message_service.send_message(
                message=message,
                text=Order.wrong_order_number_text.format(order_number),
                keyboard=inline_delivery_button(),
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
            await self.__set_info_to_cache(
                user_id=user_id,
                order_number=order_number,
                info=info,
            )
            await self.message_service.send_message(
                message=message,
                text=Order.ask_for_view_new_order_text,
                keyboard=inline_delivery_button(),
            )
