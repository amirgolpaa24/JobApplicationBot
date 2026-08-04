from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


SPREADSHEET_ID = "1FzeWuLeY0fv8uK3lGtNCY4QDfe0HbWq76bXY8moaqJs"
WORKSHEET_NAME = "BotResults"
REPOSITORY = "amirgolpaa24/JobApplicationBot"
DEFAULT_BRANCH = "main"
USER_TIMEZONE = "America/Edmonton"


EXPECTED_HEADERS = [
    "Job Number",
    "Position Title",
    "Company",
    "Location",
    "Priority",
    "Fit Score",
    "Work Arrangement",
    "Job Type",
    "Posting Date",
    "Date Added",
    "Key Reasons for Fit",
    "Main Gaps",
    "Job ID",
    "Salary",
    "Expected Salary",
    "Recruiter or Contact Person",
    "LinkedIn Job Posting Link",
    "Direct Application Link",
    "Status",
    "Notes",
    "Curated Resume PDF Link",
    "Curated Resume LaTeX Link",
    "Cover Letter PDF Link",
    "Cover Letter LaTeX Link",
    "Prepared Date",
    "Errors",
]

LINK_FIELDS = [
    "Curated Resume PDF Link",
    "Curated Resume LaTeX Link",
    "Cover Letter PDF Link",
    "Cover Letter LaTeX Link",
]


@dataclass(frozen=True)
class RuntimeConfig:
    repo_root: Path
    spreadsheet_id: str = SPREADSHEET_ID
    worksheet_name: str = WORKSHEET_NAME
    repository: str = REPOSITORY
    default_branch: str = DEFAULT_BRANCH
    timezone: str = USER_TIMEZONE
    service_account_file: str | None = None
    authorized_user_file: str | None = None
    token_file: str | None = None

    @classmethod
    def from_env(cls, repo_root: Path | None = None) -> "RuntimeConfig":
        root = repo_root or Path.cwd()
        return cls(
            repo_root=root,
            service_account_file=os.getenv("JOBBOT_GOOGLE_SERVICE_ACCOUNT_FILE"),
            authorized_user_file=os.getenv("JOBBOT_GOOGLE_AUTHORIZED_USER_FILE"),
            token_file=os.getenv("JOBBOT_GOOGLE_TOKEN_FILE"),
        )

    @property
    def lock_dir(self) -> Path:
        return self.repo_root / ".jobbot"
