# Changelog

## 2026-08-11 - Focus CLI on common vault operations

- Changed files or areas: `SKILL.md`, `references/common-commands.md`, `references/search-operations.md`, `references/plugin-development.md`.
- Reason: remove plugin development overlap with `obsidian-plugin-creator` and add a dedicated common-search reference, including folder-scoped property scraping with `obsidian eval` and `app.metadataCache`.
- Validation performed: read the vault note `400_Biblioteca/Tutoriais/Scraping Properties via Obsidian CLI.md` with Obsidian CLI, tested `search`, `search:context`, and a read-only `eval` metadata scrape, removed remaining plugin-development routing, and prepared final validation.

## 2026-08-11 - Split operational references

- Changed files or areas: `SKILL.md`, `references/common-commands.md`, `references/link-safe-operations.md`, `references/properties-metadata.md`, `references/plugin-development.md`, `references/troubleshooting.md`.
- Reason: keep the main skill as a concise operational guide while separating command reminders, link-safe graph operations, metadata workflows, plugin debugging, and CLI/socket troubleshooting.
- Validation performed: checked official Obsidian CLI documentation, captured the expected `unable to find Obsidian` state while the GUI was closed, then reran with Obsidian open and verified `obsidian version`, `obsidian help`, vault info, search, read, backlinks, properties, tasks, `plugin:reload`, `dev:errors`, and console capture with `dev:debug`; ran quick validation and checked prompt coverage.
