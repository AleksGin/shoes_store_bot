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
    view_another_order_button,
    welcome_keyboard,
    delete_tracking_orders_buttons,
    view_another_order_button_if_value,
    delete_one_more_button,
)
from menus import (
    ClothesPrice,
    MainMenu,
)
from phrases import (
    Misc,
    Order,
    CacheKey,
)
from repository import (
    AsyncGoogleSheetsService,
    CacheRepo,
)

from .message_service import MessageService


class CrossworldService:
    def __init__(
        self,
        message_service: MessageService,
        cache_repo: CacheRepo,
        async_table: AsyncGoogleSheetsService,
    ) -> None:
        self.message_service = message_service
        self.cache_repo = cache_repo
        self.async_table = async_table

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
            action=self.open_main,
            state=state,
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
        logging.info("перешел в __get_all_track_user_orders")
        return await self.cache_repo.get_cached_orders(
            match_form=CacheKey.match_for_user_to_orders.format(user_id)
        )

    async def user_order_process(
        self,
        message: Message,
        state: FSMContext,
    ) -> None:
        logging.info("перешел в user_order_process")
        user_id = message.from_user.id
        logging.info(f"получил {user_id}")
        tracking_keys_for_user = await self.__get_all_track_user_orders(
            user_id=user_id,
        )
        if tracking_keys_for_user:
            await self.__get_all_user_orders(
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

    async def delivery_status_process(
        self,
        message: Message,
        state: FSMContext,
        user_id: int,
    ) -> Message | None:
        if message.text is not None and message.text.isdigit():
            order_number = message.text
            get_info_from_cache = await self.__check_info_in_cache(
                order_number=order_number,
            )

            search_message = await self.message_service.send_message(
                message=message,
                text=Order.search_order_text,
            )

            if get_info_from_cache:
                logging.info("проверил что есть ключ в кэше")
                await self.__getting_process_info_from_cache(
                    message=message,
                    info_from_cache=get_info_from_cache,
                    search_message=search_message,  # type: ignore
                )
                await state.update_data(
                    user_id=user_id,
                    order_number=order_number,
                    info=get_info_from_cache,
                )
                logging.info(
                    f"добавил в стейт вот это: user_id: {user_id}, order_number: {order_number}, info: {get_info_from_cache}"
                )
            else:
                logging.info("понял что нет ключа в кэше")
                await self.__new_order_number_process_and_set_into_cache(
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

    async def tracking_process(
        self,
        callback: CallbackQuery,
        state: FSMContext,
    ) -> None:
        logging.info("перешел в tracking_process после нажатия кнопки для отслеживания")
        data = await state.get_data()
        logging.info(f"получил из стейта инфу {data}")

        user_id, order_number, info = (
            data["user_id"],
            data["order_number"],
            data["info"],
        )
        logging.info(f"более подробная инфа {user_id} {order_number} {info}")

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
            await self.__set_info_into_cache(
                user_id=user_id,
                order_number=order_number,
                info=info,
                tracking=True,
            )

            await self.message_service.send_message(
                message=callback.message,  # type: ignore
                text=Order.order_tracked_text.format(order_number),
            )

    async def __set_info_into_cache(
        self,
        user_id: int | None,
        order_number: str,
        info: str,
        tracking: bool,
    ) -> None:
        logging.info("перешел в метод __set_info_to_cache")
        set_into_cache = await self.cache_repo.set_order_status(
            user_id=user_id,
            order_number=order_number,
            info=info,
            tracking=tracking,
        )
        return set_into_cache

    async def __check_info_in_cache(
        self,
        order_number: str,
    ):
        check_cache = await self.cache_repo.get_info_about_order(
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
    ) -> None:
        await asyncio.sleep(0.5)
        await search_message.delete()
        await self.message_service.send_message(
            message=message,
            text=info_from_cache,
        )
        await self.__ask_for_new_order_or_track(
            message=message,
        )

    async def __new_order_number_process_and_set_into_cache(
        self,
        message: Message,
        search_message: Message,
        order_number: str,
        user_id: int,
        state: FSMContext,
    ) -> None:
        logging.info("перешел в new_order_number_process")
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
            set_info = await self.__set_info_into_cache(
                user_id=None,
                order_number=order_number,
                info=info,
                tracking=False,
            )
            logging.info(f"засунул в кэш {set_info}")
            await self.__ask_for_new_order_or_track(
                message=message,
            )
            await state.update_data(
                user_id=user_id,
                order_number=order_number,
                info=info,
            )
            logging.info(
                f"в кэше не нашел, добавил: user_id: {user_id}, order_number: {order_number}, info: {info}"
            )

    async def __ask_for_new_order_or_track(self, message: Message) -> None:
        await self.message_service.send_message(
            message=message,
            text=Order.ask_for_view_new_order_text,
            keyboard=view_another_order_button(),
        )

    async def __get_all_user_orders(
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
        )
        await self.message_service.send_message(
            message=message,
            text=Order.text_about_tracking_orders,
            keyboard=to_welcome_keyboard(),
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
                await self.delete_process(
                    callback=callback,
                    user_id=user_id,
                    state=state,
                    single_order_only=True,
                )
                await state.set_state(
                    state=OrderStatusState.waiting_order_number_to_delete
                )
            else:
                await self.delete_process(
                    callback=callback,
                    user_id=user_id,
                    state=state,
                    single_order_only=False,
                )
        else:
            await self.message_service.send_message(
                message=callback.message,
                text=Order.empty_tracking_list_text,
            )
            await state.set_state(
                state=OrderStatusState.all_tracker_deleted_notification
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
                await self.delete_all(
                    callback=callback,
                    user_id=user_id,
                    state=state,
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
            message=callback.message,
            text=Order.all_orders_deleted_text,
        )
        await state.set_state(state=OrderStatusState.all_tracker_deleted_notification)
