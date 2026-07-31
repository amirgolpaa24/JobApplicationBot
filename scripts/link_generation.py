from __future__ import annotations

from scripts.models import LinkSet


def github_blob_url(repository: str, commit_sha: str, path: str) -> str:
    clean_path = path.lstrip("/")
    return f"https://github.com/{repository}/blob/{commit_sha}/{clean_path}"


def github_raw_url(repository: str, commit_sha: str, path: str) -> str:
    clean_path = path.lstrip("/")
    return f"https://raw.githubusercontent.com/{repository}/{commit_sha}/{clean_path}"


def links_for_job(repository: str, commit_sha: str, job_number: str) -> LinkSet:
    base = f"applications/Job_{job_number}"
    return LinkSet(
        resume_pdf=github_raw_url(repository, commit_sha, f"{base}/resume.pdf"),
        resume_tex=github_blob_url(repository, commit_sha, f"{base}/resume.tex"),
        cover_letter_pdf=github_raw_url(repository, commit_sha, f"{base}/cover_letter.pdf"),
        cover_letter_tex=github_blob_url(repository, commit_sha, f"{base}/cover_letter.tex"),
    )
