import asyncio

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from phrases import Order
from repository import (
    AsyncGoogleSheetsService,
    CacheRepo,
)

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

    async def _check_updates(
        self,
    ):
        cached_keys = await self.cache_repo.get_all_cached_orders()

        for key in cached_keys:
            key_parts = key.decode("utf-8").split(":")

            user_id = int(key_parts[1])
            order_number = key_parts[3]

            await self.__checking_for_relevance(
                order_number=order_number,
                user_id=user_id,
            )

            await asyncio.sleep(7)  # wait for next request

    async def __checking_for_relevance(
        self,
        order_number: str,
        user_id: int,
    ) -> None:
        gsheet_data = await self.async_table.async_search_delivery_status(
            data=order_number
        )

        format_info_from_gsheet = Order.order_number_status_text.format(
            order_number,
            gsheet_data,
        )

        redis_data = await self.cache_repo.get_info_about_order_by_user_id(
            user_id=user_id,
            order_number=order_number,
        )

        if format_info_from_gsheet != redis_data:
            await self.cache_repo.set_info_about_order_by_user_id(
                user_id=user_id,
                order_number=order_number,
                info=format_info_from_gsheet,
            )

    def start_scheduler(self):
        self.scheduler.add_job(
            func=self._check_updates,
            trigger="cron",
            hour=16,
            minute=35,
        )
        self.scheduler.start()
