from __future__ import annotations

from pathlib import Path

from scripts.models import ExistingFolderState, JobRow


REQUIRED_FILES = frozenset({"resume.tex", "resume.pdf", "cover_letter.tex", "cover_letter.pdf"})


def job_folder(repo_root: Path, job_number: str) -> Path:
    return repo_root / "applications" / f"Job_{job_number}"


def classify_existing_folder(path: Path) -> ExistingFolderState:
    if not path.exists():
        return ExistingFolderState(path=path, present_files=frozenset(), classification="missing")
    present = frozenset(child.name for child in path.iterdir() if child.is_file())
    if REQUIRED_FILES.issubset(present):
        classification = "complete"
    elif present & REQUIRED_FILES:
        classification = "partial"
    else:
        classification = "conflicting"
    return ExistingFolderState(path=path, present_files=present, classification=classification)


def expected_paths(repo_root: Path, row: JobRow) -> dict[str, Path]:
    folder = job_folder(repo_root, row.job_number)
    return {
        "resume_tex": folder / "resume.tex",
        "resume_pdf": folder / "resume.pdf",
        "cover_letter_tex": folder / "cover_letter.tex",
        "cover_letter_pdf": folder / "cover_letter.pdf",
    }
