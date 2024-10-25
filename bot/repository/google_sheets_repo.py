import asyncio
from concurrent.futures import ThreadPoolExecutor

import pygsheets
import pygsheets.client
import pygsheets.spreadsheet
from aiolimiter import AsyncLimiter


class CrossworldTableRepo:
    def __init__(self, cred_file: str, sheet_url: str) -> None:
        self.cred_file = cred_file
        self.sheet_url = sheet_url

    def _get_sheet_by_url(
        self, google_sheet_client: pygsheets.client.Client
    ) -> pygsheets.Worksheet:
        sheets: pygsheets.Spreadsheet = google_sheet_client.open_by_url(
            url=self.sheet_url
        )
        return sheets.sheet1

    def _get_googlesheet_client(self) -> pygsheets.client.Client:
        return pygsheets.authorize(service_file=self.cred_file)

    def search_delivery_status(
        self, data: str, search_col: int = 1, status_col: int = 2
    ) -> int:
        google_sheet_client = self._get_googlesheet_client()
        wks = self._get_sheet_by_url(
            google_sheet_client=google_sheet_client,
        )
        try:
            find_cell = wks.find(
                pattern=data, matchEntireCell=True, cols=(search_col, search_col)
            )[0]
        except:
            return -1
        find_cell_row = find_cell.row
        delivery_status = wks.get_value((find_cell_row, status_col))
        return delivery_status


class AsyncGoogleSheetsService:
    def __init__(
        self,
        sheets_service: CrossworldTableRepo,
        rate_limit_per_minute=95,
    ):
        self.sheets_service = sheets_service
        self.executor = ThreadPoolExecutor()
        self.limiter = AsyncLimiter(
            max_rate=rate_limit_per_minute,
            time_period=100,
        )

    async def async_search_delivery_status(
        self, data: str, search_col: int = 1, status_col: int = 2
    ) -> int:
        count = 0
        async with self.limiter:
            count += 1
            loop = asyncio.get_running_loop()
            result: int = await loop.run_in_executor(
                self.executor,
                self.sheets_service.search_delivery_status,
                data,
                search_col,
                status_col,
            )
        return result
