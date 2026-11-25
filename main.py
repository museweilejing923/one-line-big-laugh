"""One-line big-laugh writer.

Writes one fixed joke about scheduling a meeting to relax to
/output/entry.txt. Deterministic output: no input, no clock,
no network, no randomness.
"""

import os
import string
import sys

LINE = "My calendar reminded me to relax, so I scheduled a meeting about it for next Tuesday at 9 a.m."
LIMIT = 200


def fail(msg):
    print("error: " + msg, file=sys.stderr)
    raise SystemExit(1)


def is_all_caps(line):
    """True when every letter in the line is uppercase.

    An all-caps joke reads as shouting, so it is turned away.
    """
    letters = [c for c in line if c.isalpha()]
    if not letters:
        return False
    for c in letters:
        if not c.isupper():
            return False
    return True


def validate(line):
    rules = [
        (lambda: not line.strip(), "blank line"),
        (lambda: len(line) > LIMIT, "over the 200-character limit"),
        (lambda: any(ord(c) < 32 or ord(c) == 127 for c in line), "control character present"),
        (lambda: line != line.strip() or "  " in line or "\n" in line, "bad spacing or a line break"),
        (lambda: line[-1] not in ".!?", "no closing punctuation"),
        (lambda: all(c in string.punctuation for c in line), "punctuation only"),
        (lambda: line.isdigit(), "digits only"),
        (lambda: not any(c.isalpha() for c in line), "no letters"),
        (lambda: "meeting" not in line.lower() and "calendar" not in line.lower(), "no calendar or meeting mentioned"),
        (lambda: is_all_caps(line), "the line is all uppercase"),
    ]
    for broken, message in rules:
        if broken():
            fail(message)


def main():
    validate(LINE)
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as out:
        out.write(LINE + "\n")


if __name__ == "__main__":
    main()
