from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "prove-it" / "scripts" / "evidence.py"


class EvidenceTests(unittest.TestCase):
    def run_tool(self, *args: str, cwd: pathlib.Path | None = None) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), *args],
            cwd=cwd or ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_passing_command_and_status(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            log = pathlib.Path(directory) / "evidence.jsonl"
            result = self.run_tool("run", "--label", "pass", "--log", str(log), "--", sys.executable, "-c", "print('ok')")
            self.assertEqual(result.returncode, 0)
            status = self.run_tool("status", "--log", str(log), "--format", "json")
            self.assertEqual(status.returncode, 0)
            self.assertEqual(json.loads(status.stdout)["status"], "VERIFIED")

    def test_failing_command_preserves_exit_code(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            log = pathlib.Path(directory) / "evidence.jsonl"
            result = self.run_tool("run", "--label", "fail", "--log", str(log), "--", sys.executable, "-c", "raise SystemExit(7)")
            self.assertEqual(result.returncode, 7)
            record = json.loads(log.read_text(encoding="utf-8"))
            self.assertEqual(record["status"], "fail")
            self.assertEqual(record["exit_code"], 7)

    def test_redacts_output_and_command(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            log = pathlib.Path(directory) / "evidence.jsonl"
            secret = "api_key=super-secret-value"
            result = self.run_tool("run", "--label", "redact", "--log", str(log), "--", sys.executable, "-c", f"print('{secret}')")
            self.assertEqual(result.returncode, 0)
            stored = log.read_text(encoding="utf-8")
            self.assertNotIn("super-secret-value", stored)
            self.assertIn("[REDACTED]", stored)

    def test_custom_redaction(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            log = pathlib.Path(directory) / "evidence.jsonl"
            result = self.run_tool(
                "run",
                "--label",
                "custom",
                "--log",
                str(log),
                "--redact",
                "customer-[0-9]+",
                "--",
                sys.executable,
                "-c",
                "print('customer-4815')",
            )
            self.assertEqual(result.returncode, 0)
            stored = log.read_text(encoding="utf-8")
            self.assertNotIn("customer-4815", stored)

    def test_render_report(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = pathlib.Path(directory)
            log = base / "evidence.jsonl"
            report = base / "report.md"
            run = self.run_tool("run", "--label", "unit tests", "--log", str(log), "--", sys.executable, "-c", "print('12 passed')")
            self.assertEqual(run.returncode, 0)
            render = self.run_tool("render", "--log", str(log), "--output", str(report))
            self.assertEqual(render.returncode, 0)
            content = report.read_text(encoding="utf-8")
            self.assertIn("Status: **VERIFIED**", content)
            self.assertIn("unit tests", content)
            self.assertIn("12 passed", content)

    def test_output_truncation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            log = pathlib.Path(directory) / "evidence.jsonl"
            result = self.run_tool(
                "run",
                "--label",
                "large",
                "--log",
                str(log),
                "--max-output",
                "20",
                "--",
                sys.executable,
                "-c",
                "print('x' * 100)",
            )
            self.assertEqual(result.returncode, 0)
            record = json.loads(log.read_text(encoding="utf-8"))
            self.assertTrue(record["stdout_truncated"])
            self.assertIn("[...truncated...]", record["stdout_tail"])

    def test_timeout(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            log = pathlib.Path(directory) / "evidence.jsonl"
            result = self.run_tool(
                "run",
                "--label",
                "timeout",
                "--log",
                str(log),
                "--timeout",
                "0.05",
                "--",
                sys.executable,
                "-c",
                "import time; time.sleep(1)",
            )
            self.assertEqual(result.returncode, 124)
            record = json.loads(log.read_text(encoding="utf-8"))
            self.assertEqual(record["status"], "timeout")

    def test_missing_log_is_blocked(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            log = pathlib.Path(directory) / "missing.jsonl"
            status = self.run_tool("status", "--log", str(log), "--format", "json")
            self.assertEqual(status.returncode, 1)
            self.assertEqual(json.loads(status.stdout)["status"], "BLOCKED")


if __name__ == "__main__":
    unittest.main()
