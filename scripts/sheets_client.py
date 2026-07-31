from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from scripts.config import EXPECTED_HEADERS, RuntimeConfig
from scripts.models import JobRow, validate_headers


class SheetsClient(Protocol):
    def read_rows(self) -> list[JobRow]:
        ...

    def reread_row(self, row_number: int) -> JobRow:
        ...

    def update_row(self, row_number: int, values: list[str]) -> None:
        ...


@dataclass
class GoogleSheetsClient:
    config: RuntimeConfig

    def __post_init__(self) -> None:
        self._service = None

    def _build_service(self):
        if self._service is not None:
            return self._service
        try:
            from google.oauth2 import service_account
            from google.oauth2.credentials import Credentials
            from googleapiclient.discovery import build
        except ImportError as exc:
            raise RuntimeError("Install Google dependencies with: pip install -e '.[google]'") from exc

        scopes = ["https://www.googleapis.com/auth/spreadsheets"]
        if self.config.service_account_file:
            creds = service_account.Credentials.from_service_account_file(self.config.service_account_file, scopes=scopes)
        elif self.config.token_file:
            creds = Credentials.from_authorized_user_file(self.config.token_file, scopes=scopes)
        else:
            raise RuntimeError("Set JOBBOT_GOOGLE_SERVICE_ACCOUNT_FILE or JOBBOT_GOOGLE_TOKEN_FILE before reading Google Sheets.")
        self._service = build("sheets", "v4", credentials=creds)
        return self._service

    def _values(self, range_name: str) -> list[list[str]]:
        service = self._build_service()
        result = service.spreadsheets().values().get(
            spreadsheetId=self.config.spreadsheet_id,
            range=f"{self.config.worksheet_name}!{range_name}",
        ).execute()
        return result.get("values", [])

    def read_rows(self) -> list[JobRow]:
        values = self._values("A:X")
        if not values:
            return []
        headers = values[0]
        validate_headers(headers)
        rows: list[JobRow] = []
        for index, raw in enumerate(values[1:], start=2):
            mapped = {header: raw[pos] if pos < len(raw) else "" for pos, header in enumerate(headers)}
            rows.append(JobRow(row_number=index, values=mapped))
        return rows

    def reread_row(self, row_number: int) -> JobRow:
        values = self._values(f"A{row_number}:X{row_number}")
        headers = EXPECTED_HEADERS
        raw = values[0] if values else []
        mapped = {header: raw[pos] if pos < len(raw) else "" for pos, header in enumerate(headers)}
        return JobRow(row_number=row_number, values=mapped)

    def update_row(self, row_number: int, values: list[str]) -> None:
        service = self._build_service()
        service.spreadsheets().values().update(
            spreadsheetId=self.config.spreadsheet_id,
            range=f"{self.config.worksheet_name}!A{row_number}:X{row_number}",
            valueInputOption="USER_ENTERED",
            body={"values": [values]},
        ).execute()
