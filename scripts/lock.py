from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass
from pathlib import Path

from scripts.models import ValidationError


@dataclass
class JobLock:
    lock_path: Path
    job_number: str
    stale_after_seconds: int = 6 * 60 * 60

    def __enter__(self) -> "JobLock":
        self.lock_path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "pid": os.getpid(),
            "job_number": self.job_number,
            "created_at": time.time(),
        }
        try:
            fd = os.open(self.lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        except FileExistsError:
            self._handle_existing_lock()
            fd = os.open(self.lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(payload, handle)
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        try:
            self.lock_path.unlink()
        except FileNotFoundError:
            pass

    def _handle_existing_lock(self) -> None:
        try:
            payload = json.loads(self.lock_path.read_text(encoding="utf-8"))
            created_at = float(payload.get("created_at", 0))
            existing_job = payload.get("job_number", "unknown")
        except (OSError, ValueError, TypeError):
            created_at = 0
            existing_job = "unknown"
        age = time.time() - created_at
        if age > self.stale_after_seconds:
            self.lock_path.unlink(missing_ok=True)
            return
        raise ValidationError(f"Another preparation run is active for Job Number {existing_job}.")
