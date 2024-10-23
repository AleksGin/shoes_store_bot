from apscheduler.schedulers.asyncio import AsyncIOScheduler
from services import CrossworldService
from repository import CacheRepo
import asyncio


class UpdateDataService:
    def __init__(
        self,
        cross_service: CrossworldService,
        cache_repo: CacheRepo,
    ):
        self.cross_service = cross_service
        self.cache_repo = cache_repo

    async def update_cache_from_gsheet(self):
        gsheet_data = ...

        redis_data = ...

        if gsheet_data != redis_data:
            ...
            # await self.cache_repo.set_info_about_order_by_user_id


scheduler = AsyncIOScheduler()

scheduler.add_job()