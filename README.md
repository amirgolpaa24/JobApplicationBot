# Job Application Bot

This repository contains command-driven infrastructure for preparing one truthful, tailored job application package at a time from the `BotResults` Google Sheet.

The permanent workflow rules live in [AGENTS.md](/Users/amir/Documents/Job%20Application%20Bot/AGENTS.md).

## Commands

Run from the repository root:

```bash
./prepare --dry-run next job
./prepare --dry-run job <Job Number>
./prepare next job
./prepare job <Job Number>
./prepare finalize job <Job Number>
```

Dry-run mode reads and selects a job, attempts job-description discovery, and reports proposed actions without generating final files, committing, pushing, or updating the spreadsheet.

## Google Sheets Authentication

When working through Codex, use the connected Google Drive/Sheets plugin. That is the preferred path for this project: Codex can read and update the spreadsheet through the user's connected Google account, so no local Google credential file is needed for normal Codex-driven preparation.

Before any real write, the workflow should first perform a safe read, re-read the selected row, and then update only the intended row.

Local credentials are only needed if you want to run `./prepare` directly in a terminal outside Codex, or if the Google Drive plugin is unavailable.

Credentials must stay outside Git. For standalone terminal use, use one of these options:

### Service Account

1. Create a Google Cloud service account with Sheets API access.
2. Download the JSON key outside this repository.
3. Share the spreadsheet with the service account email as an editor.
4. Set:

```bash
export JOBBOT_GOOGLE_SERVICE_ACCOUNT_FILE="/absolute/path/to/service-account.json"
```

### OAuth Authorized User

Create OAuth credentials outside this repository and set:

```bash
export JOBBOT_GOOGLE_AUTHORIZED_USER_FILE="/absolute/path/to/authorized-user.json"
export JOBBOT_GOOGLE_TOKEN_FILE="/absolute/path/to/oauth-token.json"
```

The connected Codex Google account or standalone credential identity must have edit permission before any real spreadsheet write.

## Local Requirements

Install runtime dependencies in a virtual environment:

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -e ".[test,google]"
```

For real document preparation, install:

- `latexmk`
- a TeX distribution capable of compiling the master templates
- `pdfinfo` from Poppler for page-count validation
- GitHub CLI `gh` authenticated to `amirgolpaa24/JobApplicationBot`

## Tests

```bash
python3 -m pytest
```

Tests use mocks and temporary folders. They do not modify the real spreadsheet and do not push to GitHub.
