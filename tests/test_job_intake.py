from __future__ import annotations

from datetime import datetime

import pytest

from scripts.config import EXPECTED_HEADERS
from scripts.job_intake import build_added_row, find_duplicate_job, next_job_number, normalize_posting_url
from scripts.models import JobRow, ValidationError
from scripts.prepare_job import parse_args, run


def row(number: str, linkedin: str = "", direct: str = "", job_id: str = "", title: str = "Data Scientist", company: str = "Acme") -> JobRow:
    return JobRow(
        row_number=1,
        values={
            "Job Number": number,
            "Position Title": title,
            "Company": company,
            "LinkedIn Job Posting Link": linkedin,
            "Direct Application Link": direct,
            "Job ID": job_id,
        },
    )


def test_normalizes_supported_posting_url() -> None:
    assert (
        normalize_posting_url("HTTPS://Example.com/jobs/42/?utm_source=linkedin&b=2&a=1#details")
        == "https://example.com/jobs/42?a=1&b=2"
    )


def test_rejects_non_absolute_posting_url() -> None:
    with pytest.raises(ValidationError, match="absolute http"):
        normalize_posting_url("example.com/jobs/42")


def test_detects_duplicate_by_normalized_url() -> None:
    duplicate = find_duplicate_job(
        [row("7", direct="https://example.com/jobs/42?utm_campaign=x")],
        "https://example.com/jobs/42/",
    )
    assert duplicate is not None
    assert duplicate.job_number == "7"


def test_detects_duplicate_by_job_id() -> None:
    duplicate = find_duplicate_job([row("8", job_id="abc-123")], "https://example.com/jobs/new", job_id="ABC-123")
    assert duplicate is not None
    assert duplicate.job_number == "8"


def test_next_job_number_ignores_non_numeric_values() -> None:
    assert next_job_number([row("2"), row("bad"), row("10")]) == "11"


def test_build_added_row_blanks_preparation_columns() -> None:
    values = {
        "Job Number": "11",
        "Position Title": "Data Scientist",
        "Company": "Acme",
        "Curated Resume PDF Link": "stale",
        "Status": "Prepared",
    }
    added = build_added_row(EXPECTED_HEADERS, values, datetime(2026, 8, 1, 9, 30))
    mapped = dict(zip(EXPECTED_HEADERS, added, strict=True))
    assert mapped["Date Added"] == "2026-08-01 09:30"
    assert mapped["Status"] == "Discovered"
    assert mapped["Curated Resume PDF Link"] == ""
    assert mapped["Prepared Date"] == ""
    assert mapped["Errors"] == ""


def test_parse_add_job_command() -> None:
    args = parse_args(["--dry-run", "add", "job", "https://example.com/jobs/42"])
    assert args.dry_run is True
    assert args.command == "add"
    assert args.rest == ["job", "https://example.com/jobs/42"]


def test_dry_run_add_job_preflight_does_not_require_google(capsys) -> None:
    exit_code = run(["--dry-run", "add", "job", "https://example.com/jobs/42?utm_source=linkedin"])
    output = capsys.readouterr().out
    assert exit_code == 0
    assert "Command received: prepare --dry-run add job https://example.com/jobs/42?utm_source=linkedin" in output
    assert "Normalized URL: https://example.com/jobs/42" in output
    assert "Use the connected Google Drive/Sheets plugin" in output
