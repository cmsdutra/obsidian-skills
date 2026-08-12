#!/usr/bin/env python3
"""Validate basic Obsidian theme structure and common review risks."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
REMOTE_RE = re.compile(r"(?:@import\s+)?url\(\s*['\"]?https?://|@import\s+['\"]https?://", re.I)


def fail(message: str) -> None:
    print(f"ERROR: {message}")


def warn(message: str) -> None:
    print(f"WARN: {message}")


def validate_manifest(theme_dir: Path) -> int:
    errors = 0
    manifest_path = theme_dir / "manifest.json"
    if not manifest_path.is_file():
        fail("manifest.json is missing")
        return 1

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"manifest.json is invalid JSON: {exc}")
        return 1

    if not isinstance(manifest, dict):
        fail("manifest.json must contain an object")
        return 1

    for field in ("name", "version", "minAppVersion", "author"):
        value = manifest.get(field)
        if not isinstance(value, str) or not value.strip():
            fail(f"manifest.json field '{field}' must be a non-empty string")
            errors += 1

    for field in ("version", "minAppVersion"):
        value = manifest.get(field)
        if isinstance(value, str) and not SEMVER_RE.match(value):
            fail(f"manifest.json field '{field}' must use x.y.z format")
            errors += 1

    name = manifest.get("name")
    if isinstance(name, str) and theme_dir.name != name:
        warn(f"theme directory name '{theme_dir.name}' does not match manifest name '{name}'")

    modes = manifest.get("modes")
    if modes is not None:
        valid_modes = {"light", "dark"}
        if (
            not isinstance(modes, list)
            or not modes
            or any(mode not in valid_modes for mode in modes)
            or len(set(modes)) != len(modes)
        ):
            fail("manifest.json field 'modes' must be a non-empty unique list containing only 'light' and/or 'dark'")
            errors += 1

    for field in ("authorUrl", "fundingUrl"):
        value = manifest.get(field)
        if isinstance(value, str) and value and not value.startswith(("https://", "http://")):
            warn(f"manifest.json field '{field}' should be a URL")

    return errors


def validate_css(theme_dir: Path) -> int:
    errors = 0
    css_path = theme_dir / "theme.css"
    if not css_path.is_file():
        fail("theme.css is missing")
        return 1

    css = css_path.read_text(encoding="utf-8", errors="replace")
    if not css.strip():
        fail("theme.css is empty")
        return 1

    if REMOTE_RE.search(css):
        fail("theme.css loads remote assets; embed or bundle assets instead")
        errors += 1

    if "!important" in css:
        warn("theme.css uses !important; avoid it unless necessary")

    if ":has(" in css:
        warn("theme.css uses :has(); confirm performance is acceptable, especially in Canvas")

    if ".theme-light" not in css and ".theme-dark" not in css:
        warn("theme.css does not define .theme-light or .theme-dark blocks")

    if css.count("{") != css.count("}"):
        fail("theme.css has unbalanced braces")
        errors += 1

    if css.count("(") != css.count(")"):
        fail("theme.css has unbalanced parentheses")
        errors += 1

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate an Obsidian theme directory.")
    parser.add_argument("theme_dir", help="Path to a theme directory containing manifest.json and theme.css")
    args = parser.parse_args()

    theme_dir = Path(args.theme_dir).expanduser().resolve()
    if not theme_dir.is_dir():
        fail(f"{theme_dir} is not a directory")
        return 1

    errors = validate_manifest(theme_dir) + validate_css(theme_dir)
    if errors:
        print(f"Validation failed with {errors} error(s).")
        return 1

    print("Validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
