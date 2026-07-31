from __future__ import annotations

from collections.abc import Mapping

from scripts.config import EXPECTED_HEADERS
from scripts.models import ChangedRowError, JobRow, ValidationError, ensure_prepared_update_is_safe


def changed_row_guard(original: JobRow, current: JobRow) -> None:
    checks = ["Job Number", "Status", "Position Title", "Company"]
    changed = [field for field in checks if original[field] != current[field]]
    if changed:
        raise ChangedRowError(f"Row changed during processing; update aborted to prevent overwrite. Changed fields: {', '.join(changed)}")


def build_row_update(headers: list[str], existing_values: Mapping[str, str], updates: Mapping[str, str]) -> list[str]:
    unknown = [key for key in updates if key not in headers]
    if unknown:
        raise ValidationError(f"Cannot update unknown columns: {', '.join(unknown)}")
    ensure_prepared_update_is_safe(updates)
    return [updates.get(header, existing_values.get(header, "")) for header in headers]


def success_update_allowed(headers: list[str]) -> None:
    missing = [header for header in EXPECTED_HEADERS if header not in headers]
    if missing:
        raise ValidationError(f"Cannot write success update; missing headers: {', '.join(missing)}")
