from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal, InvalidOperation

from scripts.models import JobRow, SelectionError


def _parse_score(value: str) -> Decimal:
    try:
        return Decimal(str(value).strip() or "0")
    except InvalidOperation:
        return Decimal("0")


def _parse_date(value: str) -> date:
    text = str(value).strip()
    if not text:
        return date.min
    for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%m/%d/%y", "%B %d, %Y", "%b %d, %Y"):
        try:
            return datetime.strptime(text, fmt).date()
        except ValueError:
            continue
    try:
        return datetime.fromisoformat(text).date()
    except ValueError:
        return date.min


def _parse_job_number(value: str) -> int:
    try:
        return int(str(value).strip())
    except ValueError:
        return 2**31 - 1


def _priority_rank(value: str) -> int:
    priority_order = {
        "high": 0,
        "mid": 1,
        "medium": 1,
        "low": 2,
    }
    return priority_order.get(str(value).strip().lower(), 3)


def select_next_job(rows: list[JobRow]) -> tuple[JobRow, str]:
    eligible = [row for row in rows if row.status == "Discovered"]
    if not eligible:
        raise SelectionError("No eligible rows with Status exactly Discovered.")
    selected = sorted(
        eligible,
        key=lambda row: (
            _priority_rank(row["Priority"]),
            -_parse_score(row["Fit Score"]),
            -_parse_date(row["Date Added"]).toordinal(),
            -_parse_date(row["Posting Date"]).toordinal(),
            _parse_job_number(row.job_number),
        ),
    )[0]
    return selected, "Priority High before Mid before Low, then highest Fit Score, newest Date Added, newest Posting Date, lowest Job Number tie-breaker."


def select_job_number(rows: list[JobRow], job_number: str) -> JobRow:
    matches = [row for row in rows if row.job_number == str(job_number)]
    if not matches:
        raise SelectionError(f"Job Number {job_number} does not exist.")
    row = matches[0]
    if row.status != "Discovered":
        raise SelectionError(f"Job Number {job_number} has Status {row.status!r}, not 'Discovered'.")
    return row
