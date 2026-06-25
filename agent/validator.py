from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ValidationResult:
    success: bool
    raw_log: str


def validate(flutter_app_dir: str | Path) -> ValidationResult:
    """Run `flutter analyze` inside flutter_app_dir.

    success is True only when the process exits with code 0. raw_log
    contains the combined stdout and stderr of the flutter process.
    """
    result = subprocess.run(
        ["flutter", "analyze"],
        cwd=flutter_app_dir,
        capture_output=True,
        text=True,
        check=False,
    )
    return ValidationResult(
        success=result.returncode == 0,
        raw_log=result.stdout + result.stderr,
    )


def format_file(path: str | Path) -> bool:
    """Run `dart format` on a single Dart file in place.

    Canonicalizes layout (wraps long calls, collapses short ones) so the
    output is readable regardless of source -- the deterministic codegen or
    a whole-file LLM repair response that may arrive minified on one line.

    Returns True if `dart format` exited cleanly. Raises FileNotFoundError
    if the `dart` CLI is not on PATH; the caller decides if that is fatal.
    """
    result = subprocess.run(
        ["dart", "format", str(path)],
        capture_output=True,
        text=True,
        check=False,
    )
    return result.returncode == 0
