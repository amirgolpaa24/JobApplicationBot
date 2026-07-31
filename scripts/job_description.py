from __future__ import annotations

import urllib.request

from scripts.models import JobDescription, JobRow


def retrieve_job_description(row: JobRow, timeout_seconds: int = 20) -> JobDescription:
    for field in ("Direct Application Link", "LinkedIn Job Posting Link"):
        url = row[field].strip()
        if not url:
            continue
        try:
            request = urllib.request.Request(url, headers={"User-Agent": "JobApplicationBot/0.1"})
            with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
                raw = response.read(1_000_000)
            text = raw.decode("utf-8", errors="replace")
            verified = row.position_title.lower() in text.lower() and row.company.lower() in text.lower()
            warning = None if verified else "Posting retrieved but title/company were not both verified in page text."
            return JobDescription(source=field, text=text, verified=verified, warning=warning)
        except Exception as exc:  # Network failures should be reported, not crash selection.
            last_error = f"{field} retrieval failed: {exc}"
    notes = row["Notes"].strip()
    reasons = row["Key Reasons for Fit"].strip()
    gaps = row["Main Gaps"].strip()
    fallback = "\n".join(part for part in (notes, reasons, gaps) if part)
    if fallback:
        return JobDescription(source="Spreadsheet row", text=fallback, verified=False, warning="Used spreadsheet text because posting page was not retrieved.")
    return JobDescription(source="Unavailable", text="", verified=False, warning=locals().get("last_error", "No job-description source was available."))
