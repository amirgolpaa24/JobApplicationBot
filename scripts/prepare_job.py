from __future__ import annotations

import argparse
import sys
from pathlib import Path

from scripts.config import RuntimeConfig
from scripts.job_intake import AddJobPreflight, normalize_posting_url
from scripts.job_description import retrieve_job_description
from scripts.job_selector import select_job_number, select_next_job
from scripts.lock import JobLock
from scripts.models import JobBotError, JobRow, PreparationReport
from scripts.pathing import classify_existing_folder
from scripts.sheets_client import GoogleSheetsClient


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Prepare one job application package.")
    parser.add_argument("--dry-run", action="store_true", help="Select and inspect without writing, committing, pushing, or updating Sheets.")
    parser.add_argument("command", choices=["next", "job", "finalize", "add"])
    parser.add_argument("rest", nargs="*")
    args = parser.parse_args(argv)
    if args.command == "next" and args.rest != ["job"]:
        parser.error("Use: prepare [--dry-run] next job")
    if args.command == "job" and len(args.rest) != 1:
        parser.error("Use: prepare [--dry-run] job <Job Number>")
    if args.command == "finalize" and (len(args.rest) != 2 or args.rest[0] != "job"):
        parser.error("Use: prepare finalize job <Job Number>")
    if args.command == "add" and (len(args.rest) != 2 or args.rest[0] != "job"):
        parser.error("Use: prepare [--dry-run] add job <posting-url>")
    return args


def _command_text(args: argparse.Namespace) -> str:
    prefix = "prepare --dry-run " if args.dry_run else "prepare "
    return prefix + " ".join([args.command, *args.rest])


def select_job(args: argparse.Namespace, rows: list[JobRow]) -> tuple[JobRow, str]:
    if args.command == "next":
        return select_next_job(rows)
    if args.command == "job":
        return select_job_number(rows, args.rest[0]), "Exact Job Number requested."
    return select_job_number(rows, args.rest[1]), "Finalize existing partial job requested."


def run_add_job_preflight(args: argparse.Namespace, command_text: str) -> int:
    url = args.rest[1]
    normalized_url = normalize_posting_url(url)
    print(AddJobPreflight(command_received=command_text, posting_url=url, normalized_url=normalized_url).render())
    if args.dry_run:
        return 0
    print(
        "Manual action required: inside Codex, use the connected Google Drive/Sheets plugin to "
        "retrieve the posting, de-duplicate BotResults, and append the Discovered row."
    )
    return 2


def run(argv: list[str]) -> int:
    args = parse_args(argv)
    config = RuntimeConfig.from_env(Path.cwd())
    command_text = _command_text(args)
    if args.command == "add":
        try:
            return run_add_job_preflight(args, command_text)
        except JobBotError as exc:
            print(f"Command received: {command_text}\nError: {exc}", file=sys.stderr)
            return 1
    client = GoogleSheetsClient(config)
    try:
        rows = client.read_rows()
        job, reason = select_job(args, rows)
        with JobLock(config.lock_dir / "prepare.lock", job.job_number):
            description = retrieve_job_description(job)
            folder_state = classify_existing_folder(job.application_dir(config.repo_root))
            if args.dry_run:
                report = PreparationReport(
                    command_received=command_text,
                    job=job,
                    selection_reason=reason,
                    hard_blocker_result="Not evaluated in dry-run.",
                    job_description_source=f"{description.source}{' - ' + description.warning if description.warning else ''}",
                    files_created_or_reused=f"Expected folder {folder_state.path} is {folder_state.classification}; present files: {sorted(folder_state.present_files)}",
                    local_compilation_results="Skipped in dry-run.",
                    pdf_workflow_status="Skipped in dry-run.",
                    final_spreadsheet_status=job.status,
                    error="Dry-run only; no files generated and no external writes performed.",
                )
                print(report.render())
                return 0
            report = PreparationReport(
                command_received=command_text,
                job=job,
                selection_reason=reason,
                hard_blocker_result="Pending document generation workflow.",
                job_description_source=f"{description.source}{' - ' + description.warning if description.warning else ''}",
                files_created_or_reused=f"Expected folder {folder_state.path} is {folder_state.classification}.",
                local_compilation_results="Not run because document generation is intentionally agent-reviewed.",
                pdf_workflow_status="Not started.",
                final_spreadsheet_status=job.status,
                error=(
                    "Infrastructure is installed. Generate truthful LaTeX from master files, validate locally, "
                    "then use finalize only after remote files and links are verified."
                ),
            )
            print(report.render())
            return 2
    except JobBotError as exc:
        print(PreparationReport(command_received=command_text, job=None, error=str(exc)).render(), file=sys.stderr)
        return 1


def main() -> None:
    raise SystemExit(run(sys.argv[1:]))


if __name__ == "__main__":
    main()
