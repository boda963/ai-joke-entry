"""Write the make.fun AI Joke competition entry.

Standard library only, deterministic, no network access.
"""

from __future__ import annotations

import os
from pathlib import Path

# The entry: one original one-liner about AI coding agents.
JOKE = (
    "My AI coding agent reviews my PR with the calm confidence "
    "of someone who has never been on call."
)

MIN_LENGTH = 1
MAX_LENGTH = 280
DEFAULT_OUTPUT_DIR = "/output"
OUTPUT_FILENAME = "entry.txt"


def resolve_output_dir() -> Path:
    """Return the output directory, honoring MAKEFUN_OUTPUT_DIR."""
    return Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or DEFAULT_OUTPUT_DIR)


def build_entry() -> str:
    """Return the validated entry text, including its trailing newline."""
    if "\n" in JOKE or "\r" in JOKE:
        raise SystemExit("Entry must be a single line.")

    length = len(JOKE)
    if not MIN_LENGTH <= length <= MAX_LENGTH:
        raise SystemExit(
            f"Entry must be {MIN_LENGTH}-{MAX_LENGTH} characters, got {length}."
        )
    return JOKE + "\n"


def main() -> int:
    output_dir = resolve_output_dir()
    output_dir.mkdir(parents=True, exist_ok=True)

    entry_path = output_dir / OUTPUT_FILENAME
    # newline="\n" keeps the bytes identical on every platform.
    entry_path.write_text(build_entry(), encoding="utf-8", newline="\n")

    print(f"Wrote {len(JOKE)} characters to {entry_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
