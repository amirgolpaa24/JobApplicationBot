from __future__ import annotations

import re
import shutil
import subprocess
from pathlib import Path

from scripts.models import ValidationError


PLACEHOLDER_RE = re.compile(r"(TODO|PLACEHOLDER|\\[Company\\]|\\[Position\\])", re.IGNORECASE)
REQUIRED_RESUME_SECTIONS = ("Education", "Certificates", "Languages", "Achievement")


def reject_em_dash(path: Path) -> None:
    if "—" in path.read_text(encoding="utf-8"):
        raise ValidationError(f"Forbidden em dash found in {path}")


def reject_placeholders(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    if PLACEHOLDER_RE.search(text):
        raise ValidationError(f"Placeholder text remains in {path}")


def require_resume_protected_sections(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    missing = [section for section in REQUIRED_RESUME_SECTIONS if f"\\section*{{{section}}}" not in text]
    if missing:
        raise ValidationError(f"Tailored resume is missing protected sections: {', '.join(missing)}")


def compile_latex(tex_path: Path) -> Path:
    if shutil.which("latexmk") is None:
        raise ValidationError("latexmk is not installed or not on PATH.")
    result = subprocess.run(
        ["latexmk", "-pdf", "-interaction=nonstopmode", "-halt-on-error", tex_path.name],
        cwd=tex_path.parent,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if result.returncode != 0:
        tail = "\n".join(result.stdout.splitlines()[-12:])
        raise ValidationError(f"Local LaTeX compilation failed for {tex_path.name}: {tail}")
    pdf_path = tex_path.with_suffix(".pdf")
    if not pdf_path.exists():
        raise ValidationError(f"Expected PDF was not created: {pdf_path}")
    return pdf_path


def pdf_page_count(pdf_path: Path) -> int:
    if shutil.which("pdfinfo") is None:
        raise ValidationError("pdfinfo is not installed or not on PATH.")
    result = subprocess.run(
        ["pdfinfo", str(pdf_path)],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if result.returncode != 0:
        raise ValidationError(f"Could not inspect PDF page count for {pdf_path}: {result.stdout.strip()}")
    for line in result.stdout.splitlines():
        if line.startswith("Pages:"):
            return int(line.split(":", 1)[1].strip())
    raise ValidationError(f"pdfinfo did not report page count for {pdf_path}")


def require_cover_letter_one_page(pdf_path: Path) -> None:
    pages = pdf_page_count(pdf_path)
    if pages > 1:
        raise ValidationError(f"Cover letter is {pages} pages; it must be one page.")
