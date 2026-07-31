from __future__ import annotations

from pathlib import Path

import pytest

from scripts.latex_validation import reject_em_dash, require_cover_letter_one_page
from scripts.models import ValidationError


def test_detects_em_dash_in_cover_letter(tmp_path: Path) -> None:
    path = tmp_path / "cover_letter.tex"
    path.write_text("Hello — no thanks", encoding="utf-8")
    with pytest.raises(ValidationError, match="em dash"):
        reject_em_dash(path)


def test_detects_cover_letter_longer_than_one_page(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    import scripts.latex_validation as validation

    pdf = tmp_path / "cover_letter.pdf"
    pdf.write_bytes(b"%PDF")
    monkeypatch.setattr(validation, "pdf_page_count", lambda path: 2)
    with pytest.raises(ValidationError, match="must be one page"):
        require_cover_letter_one_page(pdf)
