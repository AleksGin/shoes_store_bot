import asyncio

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from phrases import (
    CacheKey,
    Order,
)
from repository import (
    AsyncGoogleSheetsService,
)

from shared.shared_repos import CacheRepo

from .order_service import OrderService


class UpdateDataService:
    def __init__(
        self,
        order_service: OrderService,
        cache_repo: CacheRepo,
        async_table: AsyncGoogleSheetsService,
    ):
        self.order_service = order_service
        self.cache_repo = cache_repo
        self.scheduler = AsyncIOScheduler()
        self.async_table = async_table

    async def _update_orders(self):
        await self._update_orders_status()

    async def _update_orders_status(
        self,
    ) -> None:
        cached_keys = await self.cache_repo.get_cached_orders(
            match_form=CacheKey.match_for_key,
        )

        get_value_cached_keys = await self.cache_repo.get_multiple_order_infos(
            keys=cached_keys,
        )

        gsheet_orders = await self.async_table.async_get_all_orders_status()

        for key, cached_value in zip(cached_keys, get_value_cached_keys):
            order_number = await self.__parse_key(key=key, tracking=False)

            order_status_from_gsheet = gsheet_orders[order_number]

            format_gsheet_order_status = self.__format_gsheet_orders(
                order_number=str(order_number),
                order_status_from_gsheet=order_status_from_gsheet,
            )

            if cached_value != format_gsheet_order_status:
                await self.__set_new_status_into_cache(
                    order_number=str(order_number),
                    format_gsheet_order_status=format_gsheet_order_status,
                )

                await self.__set_new_status_into_cache(
                    order_number=str(order_number),
                    format_gsheet_order_status=format_gsheet_order_status,
                    tracking=True,
                )

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
            await self.cache_repo.set_order_status(
                order_number=order_number,
                info=format_gsheet_order_status,
                keep_ttl=True,
            )

    async def __update_new_status_to_track_orders(
        self,
        order_number: str,
        new_status: str,
    ):
        tracking_keys = await self.cache_repo.get_cached_orders(
            match_form=CacheKey.match_for_order_to_users.format(order_number)
        )

        if tracking_keys:
            await self.cache_repo.set_multiple_value(
                keys=tracking_keys,
                value=new_status,
                keep_ttl=True,
            )

            await self.__notification_user_about_change(
                orders=tracking_keys,
                new_status=new_status,
            )

    async def __notification_user_about_change(
        self,
        orders: list,
        new_status: str,
    ):
        for key in orders:
            user_id, order_number = await self.__parse_key(
                key=key,
                tracking=True,
            )

            await asyncio.sleep(0.3)  # wait for next request

            await self.order_service.notification_to_user(
                user_id=user_id,
                order_number=order_number,
                new_status=new_status,
            )

    async def __parse_key(self, key, tracking: bool = False):
        key_parts = key.decode("utf-8").split(":")

        if tracking:
            user_id = int(key_parts[1])
            order_number = key_parts[3]

            return user_id, order_number
        else:
            order_number = key_parts[1]

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
            hour=12,
            minute=5,
        )
        self.scheduler.start()
