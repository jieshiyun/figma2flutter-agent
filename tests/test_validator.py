from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any

import pytest

from agent import validator
from agent.validator import ValidationResult


def _completed(
    returncode: int, stdout: str = "", stderr: str = ""
) -> subprocess.CompletedProcess[str]:
    return subprocess.CompletedProcess(
        args=["flutter", "analyze"],
        returncode=returncode,
        stdout=stdout,
        stderr=stderr,
    )


def test_success_when_exit_code_zero(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        subprocess,
        "run",
        lambda *a, **kw: _completed(0, "No issues found!\n", ""),
    )
    result = validator.validate("flutter_app")
    assert result.success is True
    assert "No issues found!" in result.raw_log


def test_failure_when_exit_code_nonzero(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        subprocess,
        "run",
        lambda *a, **kw: _completed(1, "error: missing semicolon\n", ""),
    )
    result = validator.validate("flutter_app")
    assert result.success is False
    assert "missing semicolon" in result.raw_log


def test_raw_log_combines_stdout_and_stderr(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        subprocess,
        "run",
        lambda *a, **kw: _completed(2, "stdout line\n", "stderr line\n"),
    )
    result = validator.validate("flutter_app")
    assert "stdout line" in result.raw_log
    assert "stderr line" in result.raw_log
    assert result.success is False


def test_invokes_flutter_analyze_in_given_directory(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured: dict[str, Any] = {}

    def fake_run(cmd: list[str], **kwargs: Any) -> subprocess.CompletedProcess[str]:
        captured["cmd"] = cmd
        captured.update(kwargs)
        return _completed(0)

    monkeypatch.setattr(subprocess, "run", fake_run)
    validator.validate("/tmp/some/flutter_app")
    assert captured["cmd"] == ["flutter", "analyze"]
    assert captured["cwd"] == "/tmp/some/flutter_app"
    assert captured["capture_output"] is True
    assert captured["text"] is True
    assert captured["check"] is False


def test_accepts_path_object(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    captured: dict[str, Any] = {}

    def fake_run(cmd: list[str], **kwargs: Any) -> subprocess.CompletedProcess[str]:
        captured["cwd"] = kwargs.get("cwd")
        return _completed(0)

    monkeypatch.setattr(subprocess, "run", fake_run)
    result = validator.validate(tmp_path)
    assert result.success is True
    assert captured["cwd"] == tmp_path


def test_validation_result_fields() -> None:
    r = ValidationResult(success=True, raw_log="ok")
    assert r.success is True
    assert r.raw_log == "ok"


def test_format_file_invokes_dart_format(monkeypatch: pytest.MonkeyPatch) -> None:
    captured: dict[str, Any] = {}

    def fake_run(cmd: list[str], **kwargs: Any) -> subprocess.CompletedProcess[str]:
        captured["cmd"] = cmd
        return subprocess.CompletedProcess(cmd, 0, "", "")

    monkeypatch.setattr(subprocess, "run", fake_run)
    assert validator.format_file("lib/generated_screen.dart") is True
    assert captured["cmd"] == ["dart", "format", "lib/generated_screen.dart"]


def test_format_file_returns_false_on_error(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        subprocess,
        "run",
        lambda cmd, **kw: subprocess.CompletedProcess(cmd, 65, "", "err"),
    )
    assert validator.format_file("x.dart") is False
