#!/usr/bin/env python3
"""Obsidian vault hygiene audit with explicit, opt-in fixes."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable
from urllib.parse import unquote

try:
    import yaml  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    yaml = None


IGNORED_DIRS = {
    ".git",
    ".hg",
    ".obsidian",
    ".trash",
    ".sync",
    "node_modules",
    "__pycache__",
}

GENERIC_NOTE_RE = re.compile(
    r"^(untitled|new note|sem titulo|sem título|nota sem titulo|nota sem título)([-_ ]?\d+)?$",
    re.IGNORECASE,
)
WIKILINK_RE = re.compile(r"(!)?\[\[([^\]\n]+)\]\]")
MARKDOWN_LINK_RE = re.compile(r"(!)?\[[^\]\n]*\]\(([^)\n]+)\)")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$", re.MULTILINE)
BLOCK_RE = re.compile(r"(?:^|\s)\^([A-Za-z0-9-]+)(?=\s|$)")
FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*(?:\n|\Z)", re.DOTALL)
REPORT_TITLE = "# Obsidian Vault Audit"


@dataclass
class LinkFinding:
    source: str
    raw: str
    target: str
    kind: str
    line: int
    reason: str


@dataclass
class NoteFinding:
    path: str
    reason: str


@dataclass
class DuplicateFinding:
    basename: str
    paths: list[str]


@dataclass
class FixAction:
    path: str
    action: str
    detail: str
    applied: bool


def is_ignored(path: Path, include_hidden: bool) -> bool:
    for part in path.parts:
        if part in IGNORED_DIRS:
            return True
        if not include_hidden and part.startswith("."):
            return True
    return False


def iter_files(root: Path, include_hidden: bool, exclude: set[Path] | None = None) -> Iterable[Path]:
    exclude = exclude or set()
    for path in root.rglob("*"):
        resolved = path.resolve()
        if path.is_file() and resolved not in exclude and not is_ignored(path.relative_to(root), include_hidden):
            yield path


def rel(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_text(path: Path, text: str, apply: bool) -> bool:
    if apply:
        path.write_text(text, encoding="utf-8")
    return apply


def line_number(text: str, index: int) -> int:
    return text.count("\n", 0, index) + 1


def strip_target(raw: str) -> str:
    target = raw.strip()
    if "|" in target:
        target = target.split("|", 1)[0]
    return unquote(target).strip()


def target_display_suffix(raw_target: str) -> str:
    return raw_target.split("|", 1)[1] if "|" in raw_target else ""


def replace_wikilink_target(raw_body: str, new_target: str) -> str:
    alias = target_display_suffix(raw_body)
    return f"{new_target}|{alias}" if alias else new_target


def strip_markdown_target(raw: str) -> str:
    target = raw.strip()
    if " " in target and not target.startswith("<"):
        target = target.split(" ", 1)[0]
    return unquote(target.strip("<>"))


def split_fragment(target: str) -> tuple[str, str]:
    if "#" not in target:
        return target, ""
    base, fragment = target.split("#", 1)
    return base, fragment


def normalize_heading(value: str) -> str:
    value = re.sub(r"\s+#*$", "", value.strip())
    value = re.sub(r"[^\w\s-]", "", value, flags=re.UNICODE)
    return re.sub(r"\s+", " ", value).strip().lower()


def is_external(target: str) -> bool:
    lower = target.lower()
    return (
        "://" in lower
        or lower.startswith("mailto:")
        or lower.startswith("obsidian://")
        or lower.startswith("tel:")
        or lower.startswith("data:")
    )


def build_indexes(root: Path, files: list[Path]) -> dict:
    notes = [p for p in files if p.suffix.lower() == ".md" and not is_generated_report(p)]
    attachments = [p for p in files if p.suffix.lower() != ".md"]

    notes_by_rel_no_ext = {rel(p.with_suffix(""), root).lower(): p for p in notes}
    notes_by_rel = {rel(p, root).lower(): p for p in notes}
    notes_by_stem: dict[str, list[Path]] = defaultdict(list)
    attachments_by_rel = {rel(p, root).lower(): p for p in attachments}
    attachments_by_name: dict[str, list[Path]] = defaultdict(list)

    headings: dict[Path, set[str]] = {}
    blocks: dict[Path, set[str]] = {}

    for note in notes:
        notes_by_stem[note.stem.lower()].append(note)
        text = read_text(note)
        headings[note] = {normalize_heading(m.group(2)) for m in HEADING_RE.finditer(text)}
        blocks[note] = set(BLOCK_RE.findall(text))

    for attachment in attachments:
        attachments_by_name[attachment.name.lower()].append(attachment)

    return {
        "notes": notes,
        "attachments": attachments,
        "notes_by_rel_no_ext": notes_by_rel_no_ext,
        "notes_by_rel": notes_by_rel,
        "notes_by_stem": notes_by_stem,
        "attachments_by_rel": attachments_by_rel,
        "attachments_by_name": attachments_by_name,
        "headings": headings,
        "blocks": blocks,
    }


def is_generated_report(path: Path) -> bool:
    if path.suffix.lower() != ".md":
        return False
    try:
        with path.open("r", encoding="utf-8", errors="replace") as handle:
            return handle.readline().strip() == REPORT_TITLE
    except OSError:
        return False


def resolve_target(root: Path, source: Path, target: str, indexes: dict) -> tuple[Path | None, str]:
    base, _fragment = split_fragment(target)
    base = base.strip()
    if not base:
        return source, "local"

    suffix = Path(base).suffix.lower()
    source_parent = source.parent

    if suffix == ".md":
        candidates = [
            root / base,
            source_parent / base,
        ]
        for candidate in candidates:
            if candidate.exists() and candidate.is_file():
                return candidate.resolve(), "note"
        hit = indexes["notes_by_rel"].get(base.lower())
        return (hit.resolve(), "note") if hit else (None, "note")

    if suffix:
        candidates = [
            source_parent / base,
            root / base,
        ]
        for candidate in candidates:
            if candidate.exists() and candidate.is_file():
                return candidate.resolve(), "attachment"
        by_rel = indexes["attachments_by_rel"].get(base.lower())
        if by_rel:
            return by_rel.resolve(), "attachment"
        by_name = indexes["attachments_by_name"].get(Path(base).name.lower(), [])
        if len(by_name) == 1:
            return by_name[0].resolve(), "attachment"
        return None, "attachment"

    if "/" in base:
        hit = indexes["notes_by_rel_no_ext"].get(base.lower())
        if hit:
            return hit.resolve(), "note"
        candidate = root / (base + ".md")
        if candidate.exists():
            return candidate.resolve(), "note"
        return None, "note"

    stem_hits = indexes["notes_by_stem"].get(base.lower(), [])
    if len(stem_hits) == 1:
        return stem_hits[0].resolve(), "note"
    if len(stem_hits) > 1:
        return None, "ambiguous-note"
    return None, "note"


def check_fragment(target_path: Path, fragment: str, indexes: dict) -> str | None:
    if not fragment:
        return None
    fragment = fragment.strip()
    if not fragment:
        return None
    if fragment.startswith("^"):
        block_id = fragment[1:]
        if block_id not in indexes["blocks"].get(target_path, set()):
            return f"missing block target ^{block_id}"
        return None
    heading = normalize_heading(fragment)
    if heading and heading not in indexes["headings"].get(target_path, set()):
        return f"missing heading target #{fragment}"
    return None


def audit_links(root: Path, indexes: dict) -> tuple[list[LinkFinding], set[str]]:
    findings: list[LinkFinding] = []
    referenced_files: set[str] = set()

    for note in indexes["notes"]:
        text = read_text(note)
        for match in WIKILINK_RE.finditer(text):
            raw = match.group(0)
            target = strip_target(match.group(2))
            if is_external(target):
                continue
            base, fragment = split_fragment(target)
            resolved, kind = resolve_target(root, note, target, indexes)
            if resolved is None:
                reason = "ambiguous bare note link" if kind == "ambiguous-note" else "target not found"
                findings.append(LinkFinding(rel(note, root), raw, target, kind, line_number(text, match.start()), reason))
                continue
            referenced_files.add(rel(resolved, root))
            fragment_problem = check_fragment(resolved, fragment, indexes)
            if fragment_problem:
                findings.append(LinkFinding(rel(note, root), raw, target, kind, line_number(text, match.start()), fragment_problem))

        for match in MARKDOWN_LINK_RE.finditer(text):
            raw = match.group(0)
            target = strip_markdown_target(match.group(2))
            if not target or target.startswith("#") or is_external(target):
                continue
            resolved, kind = resolve_target(root, note, target, indexes)
            base, fragment = split_fragment(target)
            if resolved is None:
                findings.append(LinkFinding(rel(note, root), raw, target, kind, line_number(text, match.start()), "target not found"))
                continue
            referenced_files.add(rel(resolved, root))
            fragment_problem = check_fragment(resolved, fragment, indexes)
            if fragment_problem:
                findings.append(LinkFinding(rel(note, root), raw, target, kind, line_number(text, match.start()), fragment_problem))

    return findings, referenced_files


def audit_notes(root: Path, indexes: dict) -> tuple[list[NoteFinding], list[DuplicateFinding], list[NoteFinding]]:
    generic_names: list[NoteFinding] = []
    empty: list[NoteFinding] = []
    frontmatter: list[NoteFinding] = []

    for note in indexes["notes"]:
        text = read_text(note)
        body = FRONTMATTER_RE.sub("", text, count=1).strip()
        frontmatter_match = FRONTMATTER_RE.match(text)
        if frontmatter_match:
            if yaml is None:
                pass
            else:
                try:
                    yaml.safe_load(frontmatter_match.group(1)) or {}
                except Exception as exc:
                    frontmatter.append(NoteFinding(rel(note, root), f"frontmatter parse error: {exc}"))

        if not body:
            empty.append(NoteFinding(rel(note, root), "empty note body"))
        if GENERIC_NOTE_RE.match(note.stem):
            generic_names.append(NoteFinding(rel(note, root), "generic filename"))

    duplicates = [
        DuplicateFinding(stem, sorted(rel(p, root) for p in paths))
        for stem, paths in indexes["notes_by_stem"].items()
        if len(paths) > 1
    ]
    duplicates.sort(key=lambda item: item.basename)
    return generic_names, duplicates, empty + frontmatter


def render_markdown(report: dict) -> str:
    lines = ["# Obsidian Vault Audit", ""]
    summary = report["summary"]
    for key, value in summary.items():
        lines.append(f"- {key.replace('_', ' ').title()}: {value}")
    lines.append("")

    def section(title: str, items: list[dict], formatter) -> None:
        lines.append(f"## {title}")
        if not items:
            lines.append("")
            lines.append("No findings.")
            lines.append("")
            return
        lines.append("")
        for item in items:
            lines.append(formatter(item))
        lines.append("")

    section(
        "Broken Or Risky Links",
        report["broken_links"],
        lambda i: f"- `{i['source']}:{i['line']}` `{i['raw']}` -> `{i['target']}` ({i['reason']})",
    )
    section("Orphan Attachments", report["orphan_attachments"], lambda i: f"- `{i}`")
    section("Generic Filename Notes", report["generic_filename_notes"], lambda i: f"- `{i['path']}` ({i['reason']})")
    section("Duplicate Note Basenames", report["duplicate_note_names"], lambda i: f"- `{i['basename']}`: " + ", ".join(f"`{p}`" for p in i["paths"]))
    section("Empty Or Frontmatter Issues", report["note_issues"], lambda i: f"- `{i['path']}` ({i['reason']})")
    section("Fix Actions", report["fix_actions"], lambda i: f"- `{i['path']}` {i['action']}: {i['detail']} ({'applied' if i['applied'] else 'dry-run'})")
    return "\n".join(lines).rstrip() + "\n"


def parse_link_map(values: list[str]) -> dict[str, str]:
    mapping: dict[str, str] = {}
    for value in values:
        if "=" not in value:
            raise ValueError(f"Invalid --fix-link value, expected old=new: {value}")
        old, new = value.split("=", 1)
        old = old.strip()
        new = new.strip()
        if not old or not new:
            raise ValueError(f"Invalid --fix-link value, expected non-empty old=new: {value}")
        mapping[old] = new
    return mapping


def parse_rename_map(values: list[str]) -> dict[str, str]:
    return parse_link_map(values)


def apply_link_fixes(root: Path, indexes: dict, link_map: dict[str, str], apply: bool) -> list[FixAction]:
    actions: list[FixAction] = []
    if not link_map:
        return actions

    for note in indexes["notes"]:
        original = read_text(note)
        changed = original

        def replace_wiki(match: re.Match) -> str:
            embed = match.group(1) or ""
            body = match.group(2)
            target = strip_target(body)
            if target not in link_map:
                return match.group(0)
            replacement = replace_wikilink_target(body, link_map[target])
            actions.append(FixAction(rel(note, root), "replace wikilink target", f"{target} -> {link_map[target]}", apply))
            return f"{embed}[[{replacement}]]"

        def replace_markdown(match: re.Match) -> str:
            raw_target = strip_markdown_target(match.group(2))
            if raw_target not in link_map:
                return match.group(0)
            actions.append(FixAction(rel(note, root), "replace markdown link target", f"{raw_target} -> {link_map[raw_target]}", apply))
            return match.group(0).replace(match.group(2), link_map[raw_target], 1)

        changed = WIKILINK_RE.sub(replace_wiki, changed)
        changed = MARKDOWN_LINK_RE.sub(replace_markdown, changed)
        if changed != original:
            write_text(note, changed, apply)

    return actions


def note_target_variants(path: Path, root: Path) -> set[str]:
    rel_md = rel(path, root)
    rel_no_ext = rel(path.with_suffix(""), root)
    return {path.stem, rel_no_ext, rel_md}


def note_link_target(path: Path, root: Path) -> str:
    return rel(path.with_suffix(""), root)


def resolve_note_for_rename(root: Path, indexes: dict, spec: str) -> Path:
    target = spec.strip()
    if not target:
        raise ValueError("Empty note rename source")

    exact = root / target
    if exact.suffix.lower() != ".md":
        exact = exact.with_suffix(".md")
    if exact.exists() and exact.is_file():
        return exact.resolve()

    rel_hit = indexes["notes_by_rel"].get(target.lower())
    if rel_hit:
        return rel_hit.resolve()
    if not target.lower().endswith(".md"):
        rel_hit = indexes["notes_by_rel"].get(f"{target}.md".lower())
        if rel_hit:
            return rel_hit.resolve()

    stem = Path(target).stem.lower()
    hits = indexes["notes_by_stem"].get(stem, [])
    if len(hits) == 1:
        return hits[0].resolve()
    if len(hits) > 1:
        raise ValueError(f"Ambiguous note rename source '{spec}': " + ", ".join(rel(p, root) for p in hits))
    raise ValueError(f"Note rename source not found: {spec}")


def destination_note_path(root: Path, spec: str) -> Path:
    target = spec.strip()
    if not target:
        raise ValueError("Empty note rename destination")
    path = root / target
    if path.suffix.lower() != ".md":
        path = path.with_suffix(".md")
    resolved = path.resolve()
    resolved.relative_to(root)
    return resolved


def replace_note_links_for_rename(root: Path, indexes: dict, source: Path, destination: Path, apply: bool) -> list[FixAction]:
    actions: list[FixAction] = []
    old_variants = note_target_variants(source, root)
    new_wiki_target = note_link_target(destination, root)
    new_markdown_target = rel(destination, root)

    for note in indexes["notes"]:
        text = read_text(note)
        changed = text

        def replace_wiki(match: re.Match) -> str:
            embed = match.group(1) or ""
            body = match.group(2)
            target = strip_target(body)
            base, fragment = split_fragment(target)
            if base not in old_variants:
                return match.group(0)
            replacement_target = new_wiki_target + (f"#{fragment}" if fragment else "")
            replacement = replace_wikilink_target(body.replace(target, replacement_target, 1), replacement_target)
            actions.append(FixAction(rel(note, root), "update note link for rename", f"{target} -> {replacement_target}", apply))
            return f"{embed}[[{replacement}]]"

        def replace_markdown(match: re.Match) -> str:
            raw_target = strip_markdown_target(match.group(2))
            base, fragment = split_fragment(raw_target)
            if base not in old_variants:
                return match.group(0)
            replacement_target = new_markdown_target + (f"#{fragment}" if fragment else "")
            actions.append(FixAction(rel(note, root), "update markdown link for rename", f"{raw_target} -> {replacement_target}", apply))
            return match.group(0).replace(match.group(2), replacement_target, 1)

        changed = WIKILINK_RE.sub(replace_wiki, changed)
        changed = MARKDOWN_LINK_RE.sub(replace_markdown, changed)
        if changed != text:
            write_text(note, changed, apply)

    return actions


def rename_notes(root: Path, indexes: dict, rename_map: dict[str, str], apply: bool) -> list[FixAction]:
    actions: list[FixAction] = []
    for old, new in rename_map.items():
        source = resolve_note_for_rename(root, indexes, old)
        destination = destination_note_path(root, new)
        if destination.exists() and destination.resolve() != source:
            raise ValueError(f"Rename destination already exists: {rel(destination, root)}")

        actions.extend(replace_note_links_for_rename(root, indexes, source, destination, apply))
        if apply:
            destination.parent.mkdir(parents=True, exist_ok=True)
            source.rename(destination)
        actions.append(FixAction(rel(source, root), "rename note file", f"to {rel(destination, root)}", apply))
    return actions


def move_orphans(root: Path, orphan_attachments: list[str], destination: str, apply: bool) -> list[FixAction]:
    actions: list[FixAction] = []
    dest_root = root / destination
    for orphan in orphan_attachments:
        source = root / orphan
        target = dest_root / orphan
        suffix = 1
        while target.exists() and target.resolve() != source.resolve():
            target = dest_root / f"{source.stem}-{suffix}{source.suffix}"
            suffix += 1
        if apply:
            target.parent.mkdir(parents=True, exist_ok=True)
            source.rename(target)
        actions.append(FixAction(orphan, "move orphan attachment", f"to {rel(target, root)}", apply))
    return actions


def output_excludes(root: Path, paths: Iterable[str | None]) -> set[Path]:
    excludes: set[Path] = set()
    for raw in paths:
        if not raw:
            continue
        path = Path(raw).expanduser().resolve()
        try:
            path.relative_to(root)
        except ValueError:
            continue
        excludes.add(path)
    return excludes


def main() -> int:
    parser = argparse.ArgumentParser(description="Obsidian vault hygiene audit with explicit, opt-in fixes.")
    parser.add_argument("vault", nargs="?", default=".", help="Vault root path. Defaults to current directory.")
    parser.add_argument("--json", dest="json_path", help="Write JSON report to this path.")
    parser.add_argument("--markdown", dest="markdown_path", help="Write Markdown report to this path.")
    parser.add_argument("--include-hidden", action="store_true", help="Include hidden files except known ignored folders.")
    parser.add_argument("--apply", action="store_true", help="Apply requested fixes. Without this flag, fixes are reported as dry-run actions.")
    parser.add_argument("--fix-link", action="append", default=[], metavar="OLD=NEW", help="Replace exact link target OLD with NEW in wikilinks and Markdown links. Can be repeated.")
    parser.add_argument("--rename-note", action="append", default=[], metavar="OLD=NEW", help="Rename a note file and update links that target OLD. Can be repeated.")
    parser.add_argument("--move-orphans", metavar="FOLDER", help="Move orphan attachments into the given vault-relative folder.")
    args = parser.parse_args()

    root = Path(args.vault).expanduser().resolve()
    if not root.exists() or not root.is_dir():
        print(f"Vault path is not a directory: {root}", file=sys.stderr)
        return 2

    excludes = output_excludes(root, [args.json_path, args.markdown_path])
    files = sorted(iter_files(root, args.include_hidden, excludes))
    indexes = build_indexes(root, files)
    link_map = parse_link_map(args.fix_link)
    rename_map = parse_rename_map(args.rename_note)
    fix_actions: list[FixAction] = []
    broken_links, referenced_files = audit_links(root, indexes)
    generic_names, duplicates, note_issues = audit_notes(root, indexes)

    attachment_rels = {rel(p.resolve(), root) for p in indexes["attachments"]}
    orphan_attachments = sorted(attachment_rels - referenced_files)

    if link_map:
        fix_actions.extend(apply_link_fixes(root, indexes, link_map, args.apply))
    if rename_map:
        fix_actions.extend(rename_notes(root, indexes, rename_map, args.apply))
    if args.move_orphans:
        fix_actions.extend(move_orphans(root, orphan_attachments, args.move_orphans, args.apply))

    if args.apply and fix_actions:
        files = sorted(iter_files(root, args.include_hidden, excludes))
        indexes = build_indexes(root, files)
        broken_links, referenced_files = audit_links(root, indexes)
        generic_names, duplicates, note_issues = audit_notes(root, indexes)
        attachment_rels = {rel(p.resolve(), root) for p in indexes["attachments"]}
        orphan_attachments = sorted(attachment_rels - referenced_files)

    report = {
        "vault": str(root),
        "summary": {
            "markdown_notes": len(indexes["notes"]),
            "attachments": len(indexes["attachments"]),
            "broken_or_risky_links": len(broken_links),
            "orphan_attachments": len(orphan_attachments),
            "generic_filename_notes": len(generic_names),
            "duplicate_note_basenames": len(duplicates),
            "empty_or_frontmatter_issues": len(note_issues),
            "yaml_validation": "available" if yaml is not None else "unavailable",
            "fix_actions": len(fix_actions),
            "fix_mode": "applied" if args.apply else "dry-run",
        },
        "broken_links": [asdict(item) for item in broken_links],
        "orphan_attachments": orphan_attachments,
        "generic_filename_notes": [asdict(item) for item in generic_names],
        "duplicate_note_names": [asdict(item) for item in duplicates],
        "note_issues": [asdict(item) for item in note_issues],
        "fix_actions": [asdict(item) for item in fix_actions],
    }

    markdown = render_markdown(report)
    if args.json_path:
        Path(args.json_path).write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if args.markdown_path:
        Path(args.markdown_path).write_text(markdown, encoding="utf-8")
    if not args.json_path and not args.markdown_path:
        print(markdown)

    return 1 if broken_links else 0


if __name__ == "__main__":
    raise SystemExit(main())
