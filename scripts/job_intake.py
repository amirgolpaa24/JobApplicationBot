from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from scripts.config import EXPECTED_HEADERS, LINK_FIELDS
from scripts.models import JobRow, ValidationError


PREPARATION_ONLY_FIELDS = [
    *LINK_FIELDS,
    "Prepared Date",
    "Errors",
]


@dataclass(frozen=True)
class AddJobPreflight:
    command_received: str
    posting_url: str
    normalized_url: str

    def render(self) -> str:
        return "\n".join(
            [
                f"Command received: {self.command_received}",
                f"Posting URL: {self.posting_url}",
                f"Normalized URL: {self.normalized_url}",
                "Spreadsheet action: Use the connected Google Drive/Sheets plugin in Codex.",
                "Required result: add one new BotResults row only if no duplicate posting exists.",
                "Preparation action: none; leave preparation-only columns blank.",
            ]
        )


def normalize_posting_url(url: str) -> str:
    text = url.strip()
    parsed = urlsplit(text)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValidationError("Add-job command requires one absolute http(s) posting URL.")
    query = [(key, value) for key, value in parse_qsl(parsed.query, keep_blank_values=True) if not key.lower().startswith("utm_")]
    normalized_query = urlencode(sorted(query), doseq=True)
    path = parsed.path.rstrip("/") or "/"
    return urlunsplit((parsed.scheme.lower(), parsed.netloc.lower(), path, normalized_query, ""))


def next_job_number(rows: list[JobRow]) -> str:
    numbers: list[int] = []
    for row in rows:
        try:
            numbers.append(int(str(row.job_number).strip()))
        except ValueError:
            continue
    return str(max(numbers, default=0) + 1)


def find_duplicate_job(rows: list[JobRow], posting_url: str, job_id: str = "", title: str = "", company: str = "") -> JobRow | None:
    normalized_target = normalize_posting_url(posting_url)
    normalized_sheet_urls = {
        "LinkedIn Job Posting Link",
        "Direct Application Link",
    }
    for row in rows:
        for field in normalized_sheet_urls:
            existing_url = row[field].strip()
            try:
                normalized_existing = normalize_posting_url(existing_url) if existing_url else ""
            except ValidationError:
                normalized_existing = ""
            if normalized_existing and normalized_existing == normalized_target:
                return row
        if job_id and row["Job ID"].strip() and row["Job ID"].strip().lower() == job_id.strip().lower():
            return row
        if title and company:
            same_title = row.position_title.strip().lower() == title.strip().lower()
            same_company = row.company.strip().lower() == company.strip().lower()
            if same_title and same_company:
                return row
    return None


def build_added_row(headers: list[str], values: dict[str, str], added_at: datetime) -> list[str]:
    missing = [header for header in EXPECTED_HEADERS if header not in headers]
    if missing:
        raise ValidationError(f"Missing required spreadsheet headers: {', '.join(missing)}")
    row = {header: values.get(header, "") for header in headers}
    row["Date Added"] = values.get("Date Added") or added_at.strftime("%Y-%m-%d %H:%M")
    row["Status"] = "Discovered"
    for field in PREPARATION_ONLY_FIELDS:
        row[field] = ""
    return [row.get(header, "") for header in headers]
