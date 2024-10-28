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
        await self._update_regular_orders()
        logging.info("первым делом выполняю _update_regular_orders")
        await asyncio.sleep(4)

        await self._update_tracking_orders()
        logging.info(
            "Я закончил проверять регулярные ордеры, сейчас пойду по трекингам"
        )

    async def _update_regular_orders(
        self,
    ) -> None:
        logging.info("перешел в _update_regular_orders")
        await asyncio.sleep(4)
        get_cached_keys = await self.cache_repo.get_all_cached_orders(
            match_form=CacheKey.match_for_key,
        )
        logging.info(f"получил список регулярных ордеров {get_cached_keys}")
        await asyncio.sleep(4)

        for key in get_cached_keys:
            logging.info(f"получил вот такой key: {key}")
            await asyncio.sleep(4)
            user_id, order_number = await self.__parse_key(key=key)

            await self.__checking_for_relevance_regular(
                order_number=order_number,
                user_id=user_id,
            )

            await asyncio.sleep(7)  # wait for next request

    async def _update_tracking_orders(
        self,
    ) -> None:
        logging.info("перешел в _update_tracking_orders")
        await asyncio.sleep(4)
        get_tracking_orders = await self.cache_repo.get_all_cached_orders(
            match_form=CacheKey.match_tracking_key,
        )
        logging.info(f"получил все трекинги-ореды из кэша: {get_tracking_orders}")
        await asyncio.sleep(4)

        for key in get_tracking_orders:
            logging.info(f"получил вот такой трекинг-кей: {key}")
            await asyncio.sleep(4)
            user_id, order_number = await self.__parse_key(key=key)

            await self.__checking_for_relevance_cached(
                order_number=order_number,
                user_id=user_id,
            )

    async def __checking_for_relevance_regular(
        self,
        order_number: str,
        user_id: int,
    ) -> None:
        logging.info("перешел в __checking_for_relevance_regular")
        await asyncio.sleep(4)
        gsheet_data = await self.async_table.async_search_delivery_status(
            data=order_number
        )
        logging.info(f"получил из таблицы: {gsheet_data}")
        await asyncio.sleep(4)

        format_info_from_gsheet = Order.order_number_status_text.format(
            order_number,
            gsheet_data,
        )
        logging.info(f"придали форму: {format_info_from_gsheet}")

        redis_data = await self.cache_repo.get_info_about_order_by_user_id(
            user_id=user_id,
            order_number=order_number,
        )
        logging.info(f"получил из redis: {redis_data}")
        await asyncio.sleep(4)

        logging.info(f"сравниваем {format_info_from_gsheet} и {redis_data}")
        if format_info_from_gsheet != redis_data:
            logging.info(
                f"инфа из таблицы: {format_info_from_gsheet} не совпадает с кэшем: {redis_data}"
            )
            await asyncio.sleep(4)
            new_info = await self.cache_repo.set_info_about_order_by_user_id(
                user_id=user_id,
                order_number=order_number,
                info=format_info_from_gsheet,
            )
            logging.info(f"присваиваю новую инфу: {new_info}")
            await asyncio.sleep(4)

    async def __checking_for_relevance_cached(
        self,
        order_number: str,
        user_id: int,
    ) -> None:
        logging.info("перешел в __checking_for_relevance_cached")
        await asyncio.sleep(4)
        cached_regular_order_data = (
            await self.cache_repo.get_info_about_order_by_user_id(
                user_id=user_id,
                order_number=order_number,
            )
        )
        logging.info(
            f"получил из кэша вот такой оредр без трекинга: {cached_regular_order_data}"
        )
        await asyncio.sleep(4)
        info = str(cached_regular_order_data)
        await asyncio.sleep(4)
        cached_tracking_order_data = (
            await self.cache_repo.get_info_about_order_by_user_id(
                user_id=user_id,
                order_number=order_number,
                tracking=True,
            )
        )
        logging.info(
            f"получил из кэша (если он есть) трекинг-кей для этого ордера: {cached_tracking_order_data}"
        )
        await asyncio.sleep(4)

        logging.info(
            f"сейчас сравню: {cached_regular_order_data} и {cached_tracking_order_data}"
        )
        if cached_regular_order_data != cached_tracking_order_data:
            logging.info(
                f"да, регуляр {cached_regular_order_data} и трекинг для того же регуляра {cached_tracking_order_data} не совпадают"
            )
            await asyncio.sleep(4)
            set_new_info = await self.cache_repo.set_info_about_order_by_user_id(
                user_id=user_id,
                order_number=order_number,
                info=info,
                tracking=True,
            )
            logging.info(f"записал новое значение для трекинга: {set_new_info}")
            await asyncio.sleep(4)
            await self.cross_service.notification_to_user(
                user_id=user_id,
                order_number=order_number,
                new_status=info,
            )
            logging.info(
                f"уведомил наверное с такими данными: user_id: {user_id}, order_number: {order_number}, new_status: {info}"
            )

    async def __parse_key(self, key):
        logging.info("перешел в __parse_key")
        await asyncio.sleep(4)
        key_parts = key.decode("utf-8").split(":")

        user_id = int(key_parts[1])
        order_number = key_parts[3]
        logging.info(f"вернул вот это user_id: {user_id}, order_number: {order_number}")
        await asyncio.sleep(4)
        return user_id, order_number

    def start_scheduler(self):
        self.scheduler.add_job(
            func=self._update_orders,
            trigger="cron",
            hour=16,
            minute=28,
        )
        self.scheduler.start()
