import asyncio
import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from phrases import Order
from repository import (
    AsyncGoogleSheetsService,
    CacheRepo,
)
from phrases import CacheKey

from services import CrossworldService


class UpdateDataService:
    def __init__(
        self,
        cross_service: CrossworldService,
        cache_repo: CacheRepo,
        async_table: AsyncGoogleSheetsService,
    ):
        self.cross_service = cross_service
        self.cache_repo = cache_repo
        self.scheduler = AsyncIOScheduler()
        self.async_table = async_table

    async def _update_orders(self):
        logging.info("перешел в update_orders")
        await asyncio.sleep(4)
        await self._update_orders_status()
        logging.info("первым делом выполняю _update_regular_orders")
        await asyncio.sleep(4)

    async def _update_orders_status(
        self,
    ) -> None:
        logging.info("перешел в _update_regular_orders")
        await asyncio.sleep(4)
        cached_keys = await self.cache_repo.get_cached_orders(
            match_form=CacheKey.match_for_key,
        )
        logging.info(f"получил список регулярных ордеров {cached_keys}")
        get_value_cached_keys = await self.cache_repo.get_multiple_order_infos(
            keys=cached_keys,
        )
        logging.info(
            f"получил список значений регулярных ордеров {get_value_cached_keys}"
        )
        gsheet_orders = await self.async_table.async_get_all_orders_status()
        logging.info(f"получил список значений из таблицы {gsheet_orders}")
        await asyncio.sleep(4)

        for key, cached_value in zip(cached_keys, get_value_cached_keys):
            logging.info(f"получил вот такой key: {key}")
            await asyncio.sleep(4)
            order_number = await self.__parse_key(key=key, tracking=False)
            logging.info(f"распарсил ключ и получил {order_number}")
            await asyncio.sleep(4)
            order_status_from_gsheet = gsheet_orders[order_number]
            logging.info(f"получил вот такой статус: {order_status_from_gsheet}")
            format_gsheet_order_status = self.__format_gsheet_orders(
                order_number=str(order_number),
                order_status_from_gsheet=order_status_from_gsheet,
            )
            logging.info(f"order_number из parse_key: {order_number}")
            if cached_value != format_gsheet_order_status:
                logging.info(
                    f"cached_value: {cached_value} не сходится с gsheet_data[order_number]: {format_gsheet_order_status}"
                )
                await self.__set_new_status_into_cache(
                    order_number=str(order_number),
                    format_gsheet_order_status=format_gsheet_order_status,
                )

                await self.__set_new_status_into_cache(
                    order_number=str(order_number),
                    format_gsheet_order_status=format_gsheet_order_status,
                    tracking=True,
                )

                await asyncio.sleep(0.3)  # wait for next request

    async def __set_new_status_into_cache(
        self,
        order_number: str,
        format_gsheet_order_status: str,
        tracking: bool = False,
    ) -> None:
        if tracking:
            await self.__update_new_status_to_track_orders(
                order_number=order_number,
                new_status=format_gsheet_order_status,
            )
        else:
            logging.info("перешел в __set_new_status_into_cache")
            await asyncio.sleep(4)
            await self.cache_repo.set_order_status(
                order_number=order_number,
                info=format_gsheet_order_status,
            )
            logging.info("присваиваю новую инфу")
            await asyncio.sleep(4)

    async def __update_new_status_to_track_orders(
        self,
        order_number: str,
        new_status: str,
    ):
        logging.info("перешел в __update_new_status_to_track")
        tracking_keys = await self.cache_repo.get_cached_orders(
            match_form=CacheKey.match_for_order_to_users.format(order_number)
        )
        await asyncio.sleep(3)
        if tracking_keys:
            logging.info(f"Получил tracking_keys: {tracking_keys}")
            await self.cache_repo.set_multiple_value(
                keys=tracking_keys,
                value=new_status,
            )
            logging.info("выполнил set_multiple_value")
            await self.__notification_user_about_change(
                orders=tracking_keys,
                new_status=new_status,
            )

    async def __notification_user_about_change(
        self,
        orders: list,
        new_status: str,
    ):
        logging.info("перешел в __notification_user_about_change")
        for key in orders:
            logging.info(f"получил вот такой key: {key}")
            user_id, order_number = await self.__parse_key(
                key=key,
                tracking=True,
            )
            logging.info(
                f"распарсил его в parse_key: user_id: {user_id}, order_number: {order_number}"
            )
            await self.cross_service.notification_to_user(
                user_id=user_id,
                order_number=order_number,
                new_status=new_status,
            )

    async def __parse_key(self, key, tracking: bool = False):
        logging.info("перешел в __parse_key")
        await asyncio.sleep(4)
        key_parts = key.decode("utf-8").split(":")
        logging.info(f"к key_parts обратились {key_parts}")

        if tracking:
            logging.info("это трекинг-кей")
            user_id = int(key_parts[1])
            order_number = key_parts[3]
            logging.info(
                f"вернул вот это user_id: {user_id}, order_number: {order_number}"
            )
            await asyncio.sleep(4)
            return user_id, order_number
        else:
            logging.info("это не трекинг кей)")
            order_number = key_parts[1]
            logging.info(
                f"order_number: {order_number} - в таком значении: {type(order_number)}"
            )
            return order_number

    def __format_gsheet_orders(
        self,
        order_number: str,
        order_status_from_gsheet: str,
    ) -> str:
        format_info = Order.order_number_status_text.format(
            order_number,
            order_status_from_gsheet,
        )
        return format_info

    def start_scheduler(self):
        self.scheduler.add_job(
            func=self._update_orders,
            trigger="cron",
            hour=8,
            minute=28,
        )
        self.scheduler.start()
