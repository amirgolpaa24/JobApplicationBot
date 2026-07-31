from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Mapping

from scripts.config import EXPECTED_HEADERS, LINK_FIELDS


class JobBotError(RuntimeError):
    """Base exception for expected workflow failures."""


class ValidationError(JobBotError):
    """Raised when user-controlled data fails explicit validation."""


class SelectionError(JobBotError):
    """Raised when no safe job selection can be made."""


class ChangedRowError(JobBotError):
    """Raised when a spreadsheet row changed between read and write."""


@dataclass(frozen=True)
class JobRow:
    row_number: int
    values: Mapping[str, str]

    def __getitem__(self, key: str) -> str:
        return self.values.get(key, "")

    @property
    def job_number(self) -> str:
        return self["Job Number"]

    @property
    def status(self) -> str:
        return self["Status"]

    @property
    def position_title(self) -> str:
        return self["Position Title"]

    @property
    def company(self) -> str:
        return self["Company"]

    def application_dir(self, repo_root: Path) -> Path:
        return repo_root / "applications" / f"Job_{self.job_number}"


@dataclass(frozen=True)
class JobDescription:
    source: str
    text: str
    verified: bool
    warning: str | None = None


@dataclass(frozen=True)
class ExistingFolderState:
    path: Path
    present_files: frozenset[str]
    classification: str


@dataclass(frozen=True)
class LinkSet:
    resume_pdf: str
    resume_tex: str
    cover_letter_pdf: str
    cover_letter_tex: str

    def as_sheet_updates(self) -> dict[str, str]:
        return {
            "Curated Resume PDF Link": self.resume_pdf,
            "Curated Resume LaTeX Link": self.resume_tex,
            "Cover Letter PDF Link": self.cover_letter_pdf,
            "Cover Letter LaTeX Link": self.cover_letter_tex,
        }

    def require_complete(self) -> None:
        missing = [field for field, value in self.as_sheet_updates().items() if not value]
        if missing:
            raise ValidationError(f"Cannot mark Prepared without links: {', '.join(missing)}")


@dataclass(frozen=True)
class PreparationReport:
    command_received: str
    job: JobRow | None
    selection_reason: str = ""
    hard_blocker_result: str = "Not evaluated"
    job_description_source: str = ""
    files_created_or_reused: str = ""
    local_compilation_results: str = ""
    resume_page_count: int | None = None
    cover_letter_page_count: int | None = None
    application_commit_sha: str = ""
    pdf_workflow_status: str = ""
    pdf_commit_sha: str = ""
    links: LinkSet | None = None
    final_spreadsheet_status: str = ""
    prepared_date: str = ""
    error: str = ""

    def render(self) -> str:
        if self.job is None:
            return f"Command received: {self.command_received}\nError: {self.error or 'No job selected.'}"
        link_updates = self.links.as_sheet_updates() if self.links else {}
        lines = [
            f"Command received: {self.command_received}",
            f"Job Number: {self.job.job_number}",
            f"Position Title: {self.job.position_title}",
            f"Company name: {self.job.company}",
            f"Location: {self.job['Location']}",
            f"Work Arrangement: {self.job['Work Arrangement']}",
            f"Referral / Contact Person: {self.job['Recruiter or Contact Person']}",
            f"Job Type: {self.job['Job Type']}",
            f"Selection reason: {self.selection_reason}",
            f"Hard-blocker result: {self.hard_blocker_result}",
            f"Job-description source: {self.job_description_source}",
            f"Files created or reused: {self.files_created_or_reused}",
            f"Local compilation results: {self.local_compilation_results}",
            f"Resume page count: {self.resume_page_count if self.resume_page_count is not None else ''}",
            f"Cover-letter page count: {self.cover_letter_page_count if self.cover_letter_page_count is not None else ''}",
            f"Application commit SHA: {self.application_commit_sha}",
            f"PDF workflow status: {self.pdf_workflow_status}",
            f"PDF commit SHA: {self.pdf_commit_sha}",
            f"Curated Resume PDF Link: {link_updates.get('Curated Resume PDF Link', '')}",
            f"Curated Resume LaTeX Link: {link_updates.get('Curated Resume LaTeX Link', '')}",
            f"Cover Letter PDF Link: {link_updates.get('Cover Letter PDF Link', '')}",
            f"Cover Letter LaTeX Link: {link_updates.get('Cover Letter LaTeX Link', '')}",
            f"Final spreadsheet Status: {self.final_spreadsheet_status}",
            f"Prepared Date: {self.prepared_date}",
            f"Remaining error or manual action: {self.error}",
        ]
        return "\n".join(lines)


def validate_headers(headers: list[str]) -> None:
    missing = [header for header in EXPECTED_HEADERS if header not in headers]
    if missing:
        raise ValidationError(f"Missing required spreadsheet headers: {', '.join(missing)}")


def updates_for_success(links: LinkSet, prepared_at: datetime) -> dict[str, str]:
    links.require_complete()
    updates = links.as_sheet_updates()
    updates["Prepared Date"] = prepared_at.isoformat(timespec="seconds")
    updates["Errors"] = ""
    updates["Status"] = "Prepared"
    return updates


def ensure_prepared_update_is_safe(updates: Mapping[str, str]) -> None:
    if updates.get("Status") == "Prepared":
        for field in LINK_FIELDS:
            if not updates.get(field):
                raise ValidationError(f"Cannot mark Prepared without {field}")
