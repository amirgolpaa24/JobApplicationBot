from __future__ import annotations

from pathlib import Path

from scripts.link_generation import links_for_job
from scripts.pathing import classify_existing_folder, job_folder


def test_generates_correct_job_folder_paths(tmp_path: Path) -> None:
    assert job_folder(tmp_path, "123") == tmp_path / "applications" / "Job_123"


def test_generates_links_for_correct_files() -> None:
    links = links_for_job("owner/repo", "abc123", "123")
    assert links.resume_pdf == "https://raw.githubusercontent.com/owner/repo/abc123/applications/Job_123/resume.pdf"
    assert links.resume_tex == "https://github.com/owner/repo/blob/abc123/applications/Job_123/resume.tex"
    assert links.cover_letter_pdf.endswith("/applications/Job_123/cover_letter.pdf")
    assert links.cover_letter_tex.endswith("/applications/Job_123/cover_letter.tex")


def test_handles_partial_existing_job_folder(tmp_path: Path) -> None:
    folder = tmp_path / "applications" / "Job_5"
    folder.mkdir(parents=True)
    (folder / "resume.tex").write_text("resume", encoding="utf-8")
    state = classify_existing_folder(folder)
    assert state.classification == "partial"
    assert state.present_files == frozenset({"resume.tex"})
