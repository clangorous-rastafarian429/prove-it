from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import pathlib
import re
import shlex
import subprocess
import sys
import time
from typing import Any


BUILTIN_REDACTIONS = (
    (re.compile(r"(?i)(authorization\s*:\s*bearer\s+)[^\s]+"), r"\1[REDACTED]"),
    (re.compile(r"(?i)((?:api[_-]?key|access[_-]?token|auth[_-]?token|password|secret)\s*[=:]\s*)[^\s,;\"')]+"), r"\1[REDACTED]"),
    (re.compile(r"\b(?:sk|rk)-[A-Za-z0-9_-]{16,}\b"), "[REDACTED]"),
    (re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b"), "[REDACTED]"),
    (re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}\b"), "[REDACTED]"),
)


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def redact(value: str, extra_patterns: list[str]) -> str:
    result = value
    for pattern, replacement in BUILTIN_REDACTIONS:
        result = pattern.sub(replacement, result)
    for raw_pattern in extra_patterns:
        result = re.sub(raw_pattern, "[REDACTED]", result)
    return result


def clipped(value: str, limit: int) -> tuple[str, bool]:
    if len(value) <= limit:
        return value, False
    return "[...truncated...]\n" + value[-limit:], True


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8", errors="replace")).hexdigest()


def git_state(cwd: pathlib.Path) -> dict[str, Any]:
    state: dict[str, Any] = {}
    try:
        head = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
        if head.returncode == 0:
            state["head"] = head.stdout.strip()
        status = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
        if status.returncode == 0:
            lines = [line for line in status.stdout.splitlines() if line.strip()]
            state["dirty"] = bool(lines)
            state["changed_paths"] = len(lines)
    except (OSError, subprocess.SubprocessError):
        pass
    return state


def append_record(path: pathlib.Path, record: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")


def load_records(path: pathlib.Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    if not path.exists():
        return records
    with path.open(encoding="utf-8") as stream:
        for number, line in enumerate(stream, start=1):
            if not line.strip():
                continue
            try:
                item = json.loads(line)
            except json.JSONDecodeError as error:
                raise ValueError(f"Invalid JSON on line {number}: {error.msg}") from error
            if not isinstance(item, dict):
                raise ValueError(f"Invalid record on line {number}: expected an object")
            records.append(item)
    return records


def overall_status(records: list[dict[str, Any]]) -> str:
    if not records:
        return "BLOCKED"
    if any(record.get("status") != "pass" for record in records):
        return "FAILED"
    return "VERIFIED"


def markdown_fence(value: str) -> str:
    longest = max((len(match.group(0)) for match in re.finditer(r"`+", value)), default=0)
    return "`" * max(3, longest + 1)


def render_markdown(records: list[dict[str, Any]], title: str) -> str:
    status = overall_status(records)
    passed = sum(record.get("status") == "pass" for record in records)
    lines = [f"# {title}", "", f"Status: **{status}**", "", f"Checks: {passed} passed, {len(records) - passed} not passed.", ""]
    if not records:
        lines.extend(["No evidence records were found.", ""])
        return "\n".join(lines)
    lines.extend(["| Check | Command | Result | Duration |", "| --- | --- | --- | ---: |"])
    for record in records:
        label = str(record.get("label", "Unnamed check")).replace("|", "\\|")
        command = str(record.get("command_display", "")).replace("|", "\\|")
        result = str(record.get("status", "unknown")).upper()
        duration = f"{int(record.get('duration_ms', 0))} ms"
        lines.append(f"| {label} | `{command}` | {result} | {duration} |")
    lines.append("")
    for index, record in enumerate(records, start=1):
        lines.extend(
            [
                f"## {index}. {record.get('label', 'Unnamed check')}",
                "",
                f"- Result: `{str(record.get('status', 'unknown')).upper()}`",
                f"- Exit code: `{record.get('exit_code', 'n/a')}`",
                f"- Recorded: `{record.get('recorded_at', 'unknown')}`",
                f"- Working directory: `{record.get('cwd', 'unknown')}`",
                f"- Command: `{record.get('command_display', '')}`",
            ]
        )
        git = record.get("git") or {}
        if git.get("head"):
            lines.append(f"- Git revision: `{git['head']}`")
        for key, heading in (("stdout_tail", "Standard output"), ("stderr_tail", "Standard error")):
            output = str(record.get(key, "")).strip()
            if not output:
                continue
            fence = markdown_fence(output)
            lines.extend(["", f"### {heading}", "", fence + "text", output, fence])
        lines.append("")
    return "\n".join(lines)


def run_check(args: argparse.Namespace) -> int:
    command = list(args.command)
    if command and command[0] == "--":
        command = command[1:]
    if not command:
        print("No command supplied. Place it after --.", file=sys.stderr)
        return 2
    cwd = pathlib.Path(args.cwd).expanduser().resolve()
    if not cwd.is_dir():
        print(f"Working directory does not exist: {cwd}", file=sys.stderr)
        return 2
    extra_patterns = list(args.redact or [])
    env_pattern = os.environ.get("PROVEIT_REDACT")
    if env_pattern:
        extra_patterns.append(env_pattern)
    started = time.monotonic()
    raw_stdout = ""
    raw_stderr = ""
    exit_code: int | None = None
    status = "error"
    error_message = ""
    try:
        completed = subprocess.run(
            command,
            cwd=cwd,
            capture_output=True,
            text=True,
            errors="replace",
            timeout=args.timeout if args.timeout > 0 else None,
            check=False,
        )
        raw_stdout = completed.stdout
        raw_stderr = completed.stderr
        exit_code = completed.returncode
        status = "pass" if completed.returncode == 0 else "fail"
    except subprocess.TimeoutExpired as error:
        raw_stdout = error.stdout.decode(errors="replace") if isinstance(error.stdout, bytes) else error.stdout or ""
        raw_stderr = error.stderr.decode(errors="replace") if isinstance(error.stderr, bytes) else error.stderr or ""
        exit_code = 124
        status = "timeout"
        error_message = f"Command exceeded {args.timeout} seconds"
    except OSError as error:
        exit_code = 127
        status = "error"
        error_message = str(error)
    duration_ms = round((time.monotonic() - started) * 1000)
    if raw_stdout:
        print(raw_stdout, end="" if raw_stdout.endswith("\n") else "\n")
    if raw_stderr:
        print(raw_stderr, end="" if raw_stderr.endswith("\n") else "\n", file=sys.stderr)
    safe_stdout = redact(raw_stdout, extra_patterns)
    safe_stderr = redact(raw_stderr, extra_patterns)
    if error_message:
        safe_stderr = (safe_stderr + "\n" + redact(error_message, extra_patterns)).strip()
    stdout_tail, stdout_truncated = clipped(safe_stdout, args.max_output)
    stderr_tail, stderr_truncated = clipped(safe_stderr, args.max_output)
    safe_command = [redact(part, extra_patterns) for part in command]
    safe_command_display = redact(shlex.join(command), extra_patterns)
    record = {
        "schema_version": 1,
        "recorded_at": utc_now(),
        "label": args.label,
        "command": safe_command,
        "command_display": safe_command_display,
        "cwd": str(cwd),
        "status": status,
        "exit_code": exit_code,
        "duration_ms": duration_ms,
        "stdout_tail": stdout_tail,
        "stderr_tail": stderr_tail,
        "stdout_truncated": stdout_truncated,
        "stderr_truncated": stderr_truncated,
        "stdout_sha256": sha256_text(raw_stdout),
        "stderr_sha256": sha256_text(raw_stderr),
        "git": git_state(cwd),
    }
    append_record(pathlib.Path(args.log).expanduser(), record)
    return int(exit_code or 0)


def render_report(args: argparse.Namespace) -> int:
    try:
        records = load_records(pathlib.Path(args.log).expanduser())
    except ValueError as error:
        print(str(error), file=sys.stderr)
        return 2
    report = render_markdown(records, args.title)
    if args.output == "-":
        print(report)
    else:
        output = pathlib.Path(args.output).expanduser()
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(report, encoding="utf-8")
        print(output)
    return 0 if records else 1


def show_status(args: argparse.Namespace) -> int:
    try:
        records = load_records(pathlib.Path(args.log).expanduser())
    except ValueError as error:
        print(str(error), file=sys.stderr)
        return 2
    status = overall_status(records)
    passed = sum(record.get("status") == "pass" for record in records)
    summary = {"status": status, "checks": len(records), "passed": passed, "not_passed": len(records) - passed}
    if args.format == "json":
        print(json.dumps(summary, sort_keys=True))
    else:
        print(f"{status}: {passed}/{len(records)} checks passed")
    return 0 if status == "VERIFIED" else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="evidence.py", description="Capture and render verification evidence.")
    subparsers = parser.add_subparsers(dest="action", required=True)

    run_parser = subparsers.add_parser("run", help="Run a command and append a redacted evidence record.")
    run_parser.add_argument("--label", required=True)
    run_parser.add_argument("--log", default=".proveit/evidence.jsonl")
    run_parser.add_argument("--cwd", default=".")
    run_parser.add_argument("--timeout", type=float, default=0)
    run_parser.add_argument("--max-output", type=int, default=12000)
    run_parser.add_argument("--redact", action="append")
    run_parser.add_argument("command", nargs=argparse.REMAINDER)
    run_parser.set_defaults(handler=run_check)

    render_parser = subparsers.add_parser("render", help="Render a Markdown report from an evidence log.")
    render_parser.add_argument("--log", default=".proveit/evidence.jsonl")
    render_parser.add_argument("--output", default="-")
    render_parser.add_argument("--title", default="ProveIt verification report")
    render_parser.set_defaults(handler=render_report)

    status_parser = subparsers.add_parser("status", help="Return a summary and fail unless all recorded checks passed.")
    status_parser.add_argument("--log", default=".proveit/evidence.jsonl")
    status_parser.add_argument("--format", choices=("text", "json"), default="text")
    status_parser.set_defaults(handler=show_status)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return int(args.handler(args))


if __name__ == "__main__":
    raise SystemExit(main())
