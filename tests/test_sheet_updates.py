from __future__ import annotations

from datetime import datetime

import pytest

from scripts.config import EXPECTED_HEADERS
from scripts.models import ChangedRowError, JobRow, LinkSet, ValidationError, updates_for_success
from scripts.sheet_updates import build_row_update, changed_row_guard


def test_preserves_unrelated_spreadsheet_columns() -> None:
    existing = {header: "" for header in EXPECTED_HEADERS}
    existing["Job Number"] = "42"
    existing["Notes"] = "preserve me"
    updated = build_row_update(EXPECTED_HEADERS, existing, {"Errors": "brief error"})
    assert updated[EXPECTED_HEADERS.index("Notes")] == "preserve me"
    assert updated[EXPECTED_HEADERS.index("Errors")] == "brief error"


def test_refuses_to_mark_prepared_without_four_links() -> None:
    existing = {header: "" for header in EXPECTED_HEADERS}
    with pytest.raises(ValidationError, match="Cannot mark Prepared"):
        build_row_update(EXPECTED_HEADERS, existing, {"Status": "Prepared"})


def test_success_update_requires_all_links() -> None:
    with pytest.raises(ValidationError, match="Cannot mark Prepared"):
        updates_for_success(LinkSet("", "tex", "pdf", "tex"), datetime(2026, 1, 1), "CA$115,000")


def test_success_update_requires_expected_salary() -> None:
    links = LinkSet("resume.pdf", "resume.tex", "cover.pdf", "cover.tex")
    with pytest.raises(ValidationError, match="Expected Salary"):
        updates_for_success(links, datetime(2026, 1, 1))


def test_success_update_includes_expected_salary() -> None:
    links = LinkSet("resume.pdf", "resume.tex", "cover.pdf", "cover.tex")
    updates = updates_for_success(links, datetime(2026, 1, 1), "CA$115,000-CA$125,000")
    assert updates["Expected Salary"] == "CA$115,000-CA$125,000"


def test_changed_spreadsheet_row_before_final_write() -> None:
    original = JobRow(2, {"Job Number": "4", "Status": "Discovered", "Position Title": "Analyst", "Company": "A"})
    current = JobRow(2, {"Job Number": "4", "Status": "Prepared", "Position Title": "Analyst", "Company": "A"})
    with pytest.raises(ChangedRowError):
        changed_row_guard(original, current)
