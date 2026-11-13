"""Tests for the make.fun AI Joke entry generator."""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

MAIN = Path(__file__).resolve().parent / "main.py"
ENTRY_FILENAME = "entry.txt"
MIN_LENGTH = 1
MAX_LENGTH = 280


class EntryTests(unittest.TestCase):
    """End-to-end tests that run main.py in a throwaway output directory."""

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.output_dir = Path(self._tmp.name)

    def run_main(self) -> subprocess.CompletedProcess[bytes]:
        env = os.environ.copy()
        env["MAKEFUN_OUTPUT_DIR"] = str(self.output_dir)
        return subprocess.run(
            [sys.executable, str(MAIN)],
            capture_output=True,
            env=env,
            timeout=60,
        )

    def entry_path(self) -> Path:
        return self.output_dir / ENTRY_FILENAME

    def test_output_exists(self) -> None:
        result = self.run_main()

        self.assertEqual(
            result.returncode,
            0,
            msg=result.stderr.decode("utf-8", "replace"),
        )
        self.assertTrue(
            self.entry_path().is_file(),
            msg=f"expected {self.entry_path()} to be a file",
        )

    def test_output_is_valid_utf8(self) -> None:
        result = self.run_main()
        self.assertEqual(result.returncode, 0)

        raw = self.entry_path().read_bytes()
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError as exc:
            self.fail(f"entry is not valid UTF-8: {exc}")

        self.assertEqual(
            text.encode("utf-8"),
            raw,
            msg="entry does not round-trip through UTF-8",
        )

    def test_output_length_is_between_1_and_280_characters(self) -> None:
        result = self.run_main()
        self.assertEqual(result.returncode, 0)

        text = self.entry_path().read_text(encoding="utf-8")
        entry = text.rstrip("\n")

        self.assertTrue(
            MIN_LENGTH <= len(entry) <= MAX_LENGTH,
            msg=f"entry length {len(entry)} is outside "
            f"{MIN_LENGTH}-{MAX_LENGTH} characters",
        )

    def test_output_is_identical_across_two_runs(self) -> None:
        first = self.run_main()
        self.assertEqual(first.returncode, 0)
        first_bytes = self.entry_path().read_bytes()

        second = self.run_main()
        self.assertEqual(second.returncode, 0)
        second_bytes = self.entry_path().read_bytes()

        self.assertEqual(first_bytes, second_bytes)


if __name__ == "__main__":
    unittest.main()
