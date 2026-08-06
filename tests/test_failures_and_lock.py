from __future__ import annotations

import json
import time
from pathlib import Path

import pytest

from scripts.github_workflow import CommandResult, commit_and_push_job
from scripts.lock import JobLock
from scripts.models import ValidationError


def test_handles_git_push_failure(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    import scripts.github_workflow as github_workflow

    job_folder = tmp_path / "applications" / "Job_8"
    job_folder.mkdir(parents=True)
    git_calls: list[list[str]] = []

    def fake_run_git(args: list[str], cwd: Path) -> CommandResult:
        git_calls.append(args)
        if args[0] == "push":
            return CommandResult(1, "simulated push rejection")
        return CommandResult(0, "ok")

    monkeypatch.setattr(github_workflow, "run_git", fake_run_git)
    with pytest.raises(ValidationError, match="Git push failed"):
        commit_and_push_job(tmp_path, job_folder, "message")
    assert git_calls[0] == [
        "add",
        "applications/Job_8/resume.tex",
        "applications/Job_8/resume.pdf",
        "applications/Job_8/cover_letter.tex",
        "applications/Job_8/cover_letter.pdf",
    ]


def test_handles_stale_lock(tmp_path: Path) -> None:
    lock_path = tmp_path / "prepare.lock"
    lock_path.write_text(json.dumps({"pid": 123, "job_number": "9", "created_at": time.time() - 999}), encoding="utf-8")
    with JobLock(lock_path, "10", stale_after_seconds=1):
        assert lock_path.exists()


def test_blocks_active_lock(tmp_path: Path) -> None:
    lock_path = tmp_path / "prepare.lock"
    lock_path.write_text(json.dumps({"pid": 123, "job_number": "9", "created_at": time.time()}), encoding="utf-8")
    with pytest.raises(ValidationError, match="active"):
        with JobLock(lock_path, "10", stale_after_seconds=999):
            pass
