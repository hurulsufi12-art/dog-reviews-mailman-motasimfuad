"""The Dog Reviews the Mailman — a dog's five-star review, one line.

Writes the locked review to /output/entry.txt (or $ENTRY_OUTPUT).
Sealed gate: UTF-8 text, 1-200 characters, not whitespace-only.
Single-line, no-control-char and BMP-only rules below are brief
compliance / defensive hygiene, not the sealed gate.
Python 3.13 stdlib only: no network, no model calls, no wallet /
market / betting code. os.environ is read only as a data path.
"""

import os
import re
import sys

TEXT = ("Five stars for the mailman: he brings the letters, "
        "I sniff them first \u2014 no biscuit, no mail. "
        "He paid, I let him live another day.")

MAX_CHARS = 200

_BLANK = re.compile(r"[\s\ufeff]*")


def check_length(text):
    """1-200 characters (Python len counts code points, as the gate)."""
    if not 1 <= len(text) <= MAX_CHARS:
        return "length: text must be 1-200 characters"
    return None


def check_not_blank(text):
    """Reject whitespace-only text.

    Plain strip() is not enough: it leaves a lone BOM (U+FEFF) behind
    while the Node scorer treats it as whitespace, so match the full
    whitespace-plus-BOM set explicitly.
    """
    if _BLANK.fullmatch(text) is not None:
        return "not_blank: text must not be whitespace-only"
    return None


def check_single_line(text):
    """One line: no LF, CR, VT, FF, U+2028 or U+2029."""
    if any(c in text for c in ("\n", "\r", "\x0b", "\x0c",
                               "\u2028", "\u2029")):
        return "single_line: text must be a single line"
    return None


def check_no_control(text):
    """No C0 controls, DEL, or C1 controls."""
    if any(ord(c) < 0x20 or 0x7F <= ord(c) <= 0x9F for c in text):
        return "no_control: text must not contain control characters"
    return None


def check_bmp(text):
    """Reject astral characters (emoji and friends).

    The scorer is TypeScript and can count string length in UTF-16
    code units, where one astral character counts as two. Keeping the
    text inside the Basic Multilingual Plane makes every way of
    counting agree with the gate.
    """
    if any(ord(c) >= 0x10000 for c in text):
        return "bmp: text must not contain astral characters"
    return None


def validate(text):
    """Return a list of error strings; [] means the text passes."""
    if not isinstance(text, str):
        return ["type error: text must be str, got "
                + type(text).__name__]
    errors = []
    for fn in (check_length, check_not_blank, check_single_line,
               check_no_control, check_bmp):
        problem = fn(text)
        if problem is not None:
            errors.append(problem)
    return errors


def output_path():
    """Entry output path; an empty ENTRY_OUTPUT falls back to default."""
    return os.environ.get("ENTRY_OUTPUT") or "/output/entry.txt"


def check_written(path):
    """Read the written file back; None means byte-identical to TEXT.

    Catches a BOM, a stray CR or a trailing newline that validate()
    on the constant alone could never see.
    """
    try:
        raw = open(path, "rb").read()
    except OSError as exc:
        return "unreadable output: " + str(exc)
    if raw != TEXT.encode("utf-8"):
        return "written: output bytes differ from TEXT"
    if raw.startswith(b"\xef\xbb\xbf"):
        return "written: output starts with a BOM"
    if raw.endswith(b"\n") or b"\r" in raw:
        return "written: output has a newline or carriage return"
    try:
        if raw.decode("utf-8") != TEXT:
            return "written: output does not decode to TEXT"
    except UnicodeDecodeError:
        return "written: output is not valid UTF-8"
    return None


def main():
    errors = validate(TEXT)
    if errors:
        print("invalid entry:", "; ".join(errors), file=sys.stderr)
        return 1
    path = output_path()
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(TEXT)
    problem = check_written(path)
    if problem is not None:
        print("output verification failed:", problem, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
