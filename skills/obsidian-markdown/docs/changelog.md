# Changelog

Maintenance log for the `obsidian-markdown` skill.

## 2026-08-11 - Fix Frontmatter Metadata Type

- Changed files or areas: `SKILL.md`.
- Reason for the change: make `metadata` a YAML mapping instead of a sequence so skill frontmatter consumers do not reject it for invalid type.
- Validation performed: `quick_validate.py`; YAML frontmatter parsed with `metadata` as a dictionary.

## 2026-08-11 - Standardize Changelog Language

- Changed files or areas: `docs/changelog.md`.
- Reason for the change: standardize maintenance log entries in US English.
- Validation performed: `quick_validate.py`.

## 2026-08-11 - Maintenance Hook and Changelog

- Changed files or areas: `SKILL.md`, `docs/changelog.md`.
- Reason for the change: restore the changelog and add the maintenance policy equivalent to the `Maintenance Hook` in `obsidian-bases`.
- Validation performed: `quick_validate.py`.

## 2026-08-11 - Initial Modularization

- Changed files or areas: `SKILL.md`, `references/callouts.md`, `references/embeds.md`, `references/properties.md`, `references/pitfalls.md`.
- Reason for the change: keep `SKILL.md` short, move Obsidian Flavored Markdown details into on-demand references, standardize reference filenames in lowercase, and consolidate recurring pitfalls.
- Validation performed: `quick_validate.py`; prompt tests for note creation, frontmatter, wikilinks, embeds, callouts, and a combined fixture.
