#!/usr/bin/env python3
"""Validate a local Obsidian plugin project."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


REQUIRED_MANIFEST_FIELDS = {
    "id": str,
    "name": str,
    "version": str,
    "minAppVersion": str,
    "description": str,
    "author": str,
    "isDesktopOnly": bool,
}


def load_json(path: Path) -> tuple[dict[str, Any] | None, list[str]]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return None, [f"missing required file: {path.name}"]
    except json.JSONDecodeError as exc:
        return None, [f"{path.name} is not valid JSON: {exc}"]
    if not isinstance(data, dict):
        return None, [f"{path.name} must contain a JSON object"]
    return data, []


def validate_manifest(plugin_dir: Path) -> tuple[dict[str, Any] | None, list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    manifest, manifest_errors = load_json(plugin_dir / "manifest.json")
    errors.extend(manifest_errors)
    if manifest is None:
        return None, errors, warnings

    for field, expected_type in REQUIRED_MANIFEST_FIELDS.items():
        if field not in manifest:
            errors.append(f"manifest.json missing required field: {field}")
            continue
        if not isinstance(manifest[field], expected_type):
            errors.append(f"manifest.json field {field!r} must be {expected_type.__name__}")
        elif expected_type is str and not manifest[field].strip():
            errors.append(f"manifest.json field {field!r} cannot be empty")

    plugin_id = manifest.get("id")
    if isinstance(plugin_id, str):
        if not re.fullmatch(r"[a-z]+(?:-[a-z]+)*", plugin_id):
            errors.append("manifest.json id must contain lowercase letters separated by hyphens")
        if "obsidian" in plugin_id:
            errors.append("manifest.json id must not contain 'obsidian'")
        if plugin_id.endswith("plugin"):
            errors.append("manifest.json id must not end with 'plugin'")
        if plugin_dir.name != plugin_id:
            warnings.append(f"plugin folder name {plugin_dir.name!r} does not match manifest id {plugin_id!r}")

    version = manifest.get("version")
    if isinstance(version, str) and not re.fullmatch(r"\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?", version):
        errors.append("manifest.json version should use SemVer format x.y.z")

    return manifest, errors, warnings


def validate_package(plugin_dir: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    package_path = plugin_dir / "package.json"
    if not package_path.exists():
        warnings.append("package.json not found; TypeScript/build validation may be unavailable")
        return errors, warnings

    package, package_errors = load_json(package_path)
    errors.extend(package_errors)
    if package is None:
        return errors, warnings

    scripts = package.get("scripts")
    if not isinstance(scripts, dict):
        warnings.append("package.json has no scripts object")
        return errors, warnings

    if "build" not in scripts:
        warnings.append("package.json has no build script")
    if "dev" not in scripts:
        warnings.append("package.json has no dev script for watch builds")

    deps = {}
    for key in ("dependencies", "devDependencies"):
        value = package.get(key)
        if isinstance(value, dict):
            deps.update(value)
    if "obsidian" not in deps:
        warnings.append("obsidian package is not listed in dependencies or devDependencies")

    return errors, warnings


def validate_files(plugin_dir: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    if not (plugin_dir / "main.js").exists():
        warnings.append("main.js not found; run the build before installing/enabling the plugin")

    has_source = (plugin_dir / "main.ts").exists() or (plugin_dir / "src" / "main.ts").exists()
    if not has_source:
        warnings.append("no TypeScript entry found at main.ts or src/main.ts")

    if (plugin_dir / "versions.json").exists():
        versions, version_errors = load_json(plugin_dir / "versions.json")
        errors.extend(version_errors)
        if versions is not None and not all(isinstance(k, str) and isinstance(v, str) for k, v in versions.items()):
            errors.append("versions.json must map plugin versions to minimum app versions as strings")

    return errors, warnings


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_obsidian_plugin.py <plugin-dir>", file=sys.stderr)
        return 2

    plugin_dir = Path(sys.argv[1]).expanduser().resolve()
    if not plugin_dir.is_dir():
        print(f"ERROR: not a directory: {plugin_dir}", file=sys.stderr)
        return 2

    manifest, manifest_errors, manifest_warnings = validate_manifest(plugin_dir)
    package_errors, package_warnings = validate_package(plugin_dir)
    file_errors, file_warnings = validate_files(plugin_dir)

    errors = manifest_errors + package_errors + file_errors
    warnings = manifest_warnings + package_warnings + file_warnings

    if manifest:
        print(f"Plugin: {manifest.get('name', '<unnamed>')} ({manifest.get('id', '<no-id>')})")
    else:
        print(f"Plugin directory: {plugin_dir}")

    for warning in warnings:
        print(f"WARN: {warning}")
    for error in errors:
        print(f"ERROR: {error}")

    if errors:
        print(f"Validation failed with {len(errors)} error(s).")
        return 1

    print(f"Validation passed with {len(warnings)} warning(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
