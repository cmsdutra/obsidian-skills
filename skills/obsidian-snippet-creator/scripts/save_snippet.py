#!/usr/bin/env python3
"""Save an Obsidian CSS snippet under .obsidian/snippets."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


NAME_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")


def fail(message: str) -> None:
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(1)


def validate_name(name: str) -> str:
    if name.endswith(".css"):
        name = name[:-4]
    normalized = name.strip().lower().replace("_", "-").replace(" ", "-")
    normalized = re.sub(r"-+", "-", normalized)
    if not NAME_RE.match(normalized):
        fail("snippet name must be kebab-case, e.g. compact-editor")
    return normalized


def check_balanced(css: str) -> None:
    pairs = {"{": "}", "(": ")", "[": "]"}
    stack: list[tuple[str, int]] = []
    in_comment = False
    quote: str | None = None
    escape = False

    for index, char in enumerate(css):
        nxt = css[index + 1] if index + 1 < len(css) else ""

        if in_comment:
            if char == "*" and nxt == "/":
                in_comment = False
            continue

        if quote:
            if escape:
                escape = False
            elif char == "\\":
                escape = True
            elif char == quote:
                quote = None
            continue

        if char == "/" and nxt == "*":
            in_comment = True
            continue

        if char in ('"', "'"):
            quote = char
            continue

        if char in pairs:
            stack.append((char, index))
        elif char in pairs.values():
            if not stack:
                fail(f"unmatched closing {char!r} at byte {index}")
            opener, opener_index = stack.pop()
            if pairs[opener] != char:
                fail(
                    f"mismatched {opener!r} at byte {opener_index} "
                    f"closed by {char!r} at byte {index}"
                )

    if in_comment:
        fail("unterminated CSS comment")
    if quote:
        fail(f"unterminated string literal {quote!r}")
    if stack:
        opener, index = stack[-1]
        fail(f"unclosed {opener!r} at byte {index}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--vault", default=".", help="vault root containing .obsidian")
    parser.add_argument("--name", required=True, help="snippet file name, with or without .css")
    parser.add_argument("--overwrite", action="store_true", help="overwrite an existing snippet")
    args = parser.parse_args()

    vault = Path(args.vault).expanduser().resolve()
    obsidian_dir = vault / ".obsidian"
    if not obsidian_dir.is_dir():
        fail(f"{vault} does not look like an Obsidian vault")

    css = sys.stdin.read()
    if not css.strip():
        fail("no CSS received on stdin")
    check_balanced(css)

    name = validate_name(args.name)
    snippets_dir = obsidian_dir / "snippets"
    snippets_dir.mkdir(parents=True, exist_ok=True)
    target = snippets_dir / f"{name}.css"

    if target.exists() and not args.overwrite:
        fail(f"{target} already exists; pass --overwrite to replace it")

    target.write_text(css.rstrip() + "\n", encoding="utf-8")
    print(target)


if __name__ == "__main__":
    main()
