#!/usr/bin/env python3
"""Committed structured parser for the task-server /verify response.

VERIFIER-ROBUSTNESS instrument (contract 10d/7d). The predecessor bundle read
vul_exit / fix_exit out of the response with a shell `grep -o` over the raw body,
which is fragile: interleaved sanitizer text, reordered fields, or stray digit
runs in an embedded `output` field can defeat a positional regex and silently
zero an honest run. This parser reads the two exit codes as named JSON integers,
so extraction is invariant under field order, interleaved sanitizer text, and
arbitrary whitespace or digit sequences in any other field.

Usage:
  python3 parse_response.py <response_json_file>   # prints: "<vul_exit> <fix_exit>"
Exit status:
  0  both codes extracted            2  malformed / missing codes

Importable:
  parse(text) -> (vul_exit:int, fix_exit:int)   raises ValueError on failure
"""
from __future__ import annotations

import json
import sys


def _coerce_int(value) -> int:
    # Accept an int, or a string that is exactly an optionally-signed integer.
    if isinstance(value, bool):
        raise ValueError("boolean is not an exit code")
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        s = value.strip()
        if s and (s[1:] if s[0] in "+-" else s).isdigit():
            return int(s)
    raise ValueError(f"not an integer exit code: {value!r}")


def parse(text: str) -> tuple[int, int]:
    """Extract (vul_exit, fix_exit) from a /verify JSON body.

    Reads the named fields only. Immune to field order and to any additional
    field (such as an embedded sanitizer `output`) that a positional regex would
    trip over. Fails closed with ValueError rather than guessing.
    """
    obj = json.loads(text)
    if not isinstance(obj, dict):
        raise ValueError("response is not a JSON object")
    if "vul_exit_code" not in obj or "fix_exit_code" not in obj:
        raise ValueError("response missing vul_exit_code or fix_exit_code")
    return _coerce_int(obj["vul_exit_code"]), _coerce_int(obj["fix_exit_code"])


def main(argv: list[str]) -> int:
    if len(argv) < 1:
        sys.stderr.write("usage: parse_response.py <response_json_file>\n")
        return 2
    try:
        with open(argv[0], "r", encoding="utf-8", errors="replace") as fh:
            vul, fix = parse(fh.read())
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        sys.stderr.write(f"parse error: {exc}\n")
        return 2
    print(f"{vul} {fix}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
