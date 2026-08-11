# Changelog

Newest entries first. Record changes to this skill's instructions, references, scripts, assets, or validation policy.

## 2026-08-11 - Provenance note

- Changed: Added a `Provenance` section to `SKILL.md`.
- Reason: Record that the skill was originally derived from Kepano's `obsidian-skills` repository and that this local version includes modifications from the original project.
- Validation: Run `quick_validate.py` for `.codex/skills/obsidian-bases`.

## 2026-08-11 - Custom link text example

- Changed: Added a reusable `file.asLink(file.basename.replace(...))` example to `references/examples.md`.
- Reason: Preserve the documented vault pattern for displaying shortened, regex-derived link labels in Bases table columns.
- Validation: Parsed all YAML fenced blocks in `references/examples.md`.

## 2026-08-11 - Changelog maintenance hook

- Changed: Added a `Maintenance Hook` to `SKILL.md` requiring changelog entries when `SKILL.md` or `references/` files change.
- Reason: Preserve a lightweight audit trail for future updates to Bases guidance and reference material.
- Validation: Run `quick_validate.py` for `.claude` and `.codex`; parse relevant `yaml` and `base` fenced blocks where present.
