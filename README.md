# AI Joke Entry

A one-line entry for the make.fun AI Joke competition, written for
professional developers who use AI coding agents.

The program is deterministic, uses only the Python 3.13 standard library,
and makes no network requests.

**Entry:**

> My AI coding agent reviews my PR with the calm confidence of someone who has never been on call.

## What it does

`main.py` writes the joke to `entry.txt` in the output directory:

- Default: `/output/entry.txt`
- Override: set `MAKEFUN_OUTPUT_DIR` to any writable directory

The file is written as UTF-8 with a trailing newline. The joke is validated
to be a single line between 1 and 280 characters.

## Run

```sh
python main.py
```

For local testing without writing to `/output`:

```sh
MAKEFUN_OUTPUT_DIR=./out python main.py
cat out/entry.txt
```

The output directory is created if it does not already exist.

## Test

```sh
python -m unittest -v
```

The tests run `main.py` in a temporary directory and check that the entry
exists, is valid UTF-8, is within the character limit, and is identical
across two runs. No packages need to be installed.

## Files

- `main.py` — entry generator
- `test_main.py` — end-to-end tests
- `LICENSE` — MIT License
- `README.md` — this file
