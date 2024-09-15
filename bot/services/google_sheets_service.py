import pygsheets
import pygsheets.client
import pygsheets.spreadsheet


class CrossworldTable:
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
        wks = self._get_sheet_by_url(google_sheet_client=google_sheet_client)
        try:
            find_cell = wks.find(
                pattern=data, matchEntireCell=True, cols=(search_col, search_col)
            )[0]
        except:
            return -1
        find_cell_row = find_cell.row
        delivery_status = wks.get_value((find_cell_row, status_col))
        return delivery_status
