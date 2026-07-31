from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path

from scripts.models import ValidationError


@dataclass(frozen=True)
class CommandResult:
    returncode: int
    stdout: str


def run_git(args: list[str], cwd: Path) -> CommandResult:
    result = subprocess.run(["git", *args], cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
    return CommandResult(result.returncode, result.stdout.strip())


def require_clean_worktree(cwd: Path) -> None:
    result = run_git(["status", "--porcelain"], cwd)
    if result.returncode != 0:
        raise ValidationError(f"Git status failed: {result.stdout}")
    if result.stdout:
        raise ValidationError(f"Unrelated uncommitted changes exist; stop before job preparation:\n{result.stdout}")


def commit_and_push_job(cwd: Path, job_folder: Path, message: str) -> str:
    rel = job_folder.relative_to(cwd)
    add = run_git(["add", str(rel / "resume.tex"), str(rel / "cover_letter.tex")], cwd)
    if add.returncode != 0:
        raise ValidationError(f"Git add failed: {add.stdout}")
    commit = run_git(["commit", "-m", message], cwd)
    if commit.returncode != 0:
        raise ValidationError(f"Git commit failed: {commit.stdout}")
    push = run_git(["push", "origin", "main"], cwd)
    if push.returncode != 0:
        raise ValidationError(f"Git push failed: {push.stdout}")
    sha = run_git(["rev-parse", "HEAD"], cwd)
    if sha.returncode != 0:
        raise ValidationError(f"Could not determine application commit SHA: {sha.stdout}")
    return sha.stdout


def workflow_failure(message: str) -> None:
    raise ValidationError(f"GitHub Actions failed while compiling application files: {message}")
