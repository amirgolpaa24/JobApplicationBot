from __future__ import annotations

import pytest

from scripts.job_selector import select_job_number, select_next_job
from scripts.models import JobRow, SelectionError


def row(number: str, score: str = "10", added: str = "2026-01-01", posting: str = "2026-01-01", status: str = "Discovered") -> JobRow:
    return JobRow(
        row_number=int(number),
        values={
            "Job Number": number,
            "Position Title": f"Role {number}",
            "Company": "Acme",
            "Status": status,
            "Priority": "",
            "Fit Score": score,
            "Date Added": added,
            "Posting Date": posting,
        },
    )


def test_selects_highest_fit_score() -> None:
    selected, _ = select_next_job([row("1", "70"), row("2", "95")])
    assert selected.job_number == "2"


def test_priority_outranks_fit_score_for_next_job() -> None:
    low_score_high_priority = row("1", score="70")
    low_score_high_priority.values["Priority"] = "High"
    high_score_mid_priority = row("2", score="95")
    high_score_mid_priority.values["Priority"] = "Mid"
    selected, reason = select_next_job([high_score_mid_priority, low_score_high_priority])
    assert selected.job_number == "1"
    assert "Priority High before Mid before Low" in reason


def test_unknown_priority_sorts_after_low_priority() -> None:
    unknown_priority = row("1", score="99")
    unknown_priority.values["Priority"] = "Urgent"
    low_priority = row("2", score="70")
    low_priority.values["Priority"] = "Low"
    selected, _ = select_next_job([unknown_priority, low_priority])
    assert selected.job_number == "2"


def test_tie_breaks_by_date_added() -> None:
    selected, _ = select_next_job([row("1", added="2026-01-01"), row("2", added="2026-02-01")])
    assert selected.job_number == "2"


def test_tie_breaks_by_posting_date() -> None:
    selected, _ = select_next_job([row("1", posting="2026-01-01"), row("2", posting="2026-01-15")])
    assert selected.job_number == "2"


def test_final_tie_breaks_by_lowest_job_number() -> None:
    selected, _ = select_next_job([row("9"), row("3")])
    assert selected.job_number == "3"


def test_selects_exact_job_number() -> None:
    assert select_job_number([row("7"), row("8")], "8").job_number == "8"


def test_rejects_missing_job_number() -> None:
    with pytest.raises(SelectionError, match="does not exist"):
        select_job_number([row("7")], "8")


def test_refuses_non_discovered_row() -> None:
    with pytest.raises(SelectionError, match="not 'Discovered'"):
        select_job_number([row("7", status="Prepared")], "7")
