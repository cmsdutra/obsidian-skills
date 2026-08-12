---
name: obsidian-vault-sanitizer
description: Audit, report, and safely clean Obsidian vault hygiene problems. Use when Codex needs to inspect or fix broken wikilinks or Markdown links, unresolved embeds, orphan attachments, duplicate note names, notes with generic filenames such as "Sem título 1.md" or "Untitled.md", empty notes, invalid or risky frontmatter, stale attachment references, unsafe renames or moves, and other Obsidian vault maintenance issues.
---

# Obsidian Vault Sanitizer

Audit an Obsidian vault before changing it, then apply the smallest safe cleanup. Prefer Obsidian-aware operations for anything that can affect links, backlinks, embeds, aliases, headings, or attachment paths.

## Core Workflow

1. Identify the vault root. If the current directory contains `.obsidian/`, use it; otherwise ask for or infer the vault path from the user request.
2. Run an audit first:

```bash
python3 skills/obsidian-vault-sanitizer/scripts/audit_vault.py /path/to/vault --markdown /tmp/obsidian-vault-audit.md
```

3. Review findings by risk:
   - Broken note links, unresolved embeds, duplicate note names, and attachment references can affect graph integrity.
   - Orphan attachments and empty notes are cleanup candidates, but do not delete without user approval.
   - Notes with generic filenames usually need a user-chosen filename, plus backlink/link updates.
4. For deterministic fixes, run the script in dry-run mode first. Add `--apply` only after the proposed actions match the user's intent.
5. For renames, moves, deletes, or alias changes, use the vault's Obsidian CLI link-safe workflow if available. Load the Obsidian CLI skill's `references/link-safe-operations.md` when needed.
6. Make direct filesystem edits only for low-risk content fixes that do not require Obsidian to rewrite backlinks.
7. Re-run the audit after changes and report remaining issues. Prefer report paths outside the vault; if report paths are inside the vault, the script excludes its own `--json` and `--markdown` outputs and Markdown reports headed `# Obsidian Vault Audit`.

## Audit Script

Use [scripts/audit_vault.py](scripts/audit_vault.py) for repeatable checks and controlled fixes. It reports:

- Broken wikilinks and Markdown links to notes or attachments.
- Missing heading or block targets when the linked file can be resolved.
- Orphan attachments not referenced by any Markdown note.
- Duplicate note basenames that make bare wikilinks ambiguous.
- Generic note filenames such as `Untitled.md`, `Sem título 1.md`, or `New Note.md`.
- Empty notes and basic frontmatter parse failures.
- Basic frontmatter parse failures when PyYAML is installed.

By default, the script is read-only. Fix flags produce dry-run actions unless `--apply` is present.

Useful commands:

```bash
python3 skills/obsidian-vault-sanitizer/scripts/audit_vault.py .
python3 skills/obsidian-vault-sanitizer/scripts/audit_vault.py ~/Vault --json /tmp/vault-audit.json
python3 skills/obsidian-vault-sanitizer/scripts/audit_vault.py ~/Vault --include-hidden
```

## Correction Commands

Use correction commands for fixes that are explicit and reversible enough to automate:

```bash
# Dry-run exact link target replacements supplied by the user.
python3 skills/obsidian-vault-sanitizer/scripts/audit_vault.py ~/Vault \
  --fix-link "Old Note=Folder/New Note" \
  --fix-link "Attachments/old.pdf=Resources/new.pdf"

# Apply those replacements after reviewing the dry-run.
python3 skills/obsidian-vault-sanitizer/scripts/audit_vault.py ~/Vault \
  --fix-link "Old Note=Folder/New Note" \
  --apply

# Rename a generic note filename and update links to it.
python3 skills/obsidian-vault-sanitizer/scripts/audit_vault.py ~/Vault \
  --rename-note "Sem título 1=Projetos/Resumo da reunião"

# Move orphan attachments to a review folder, first as dry-run, then with --apply.
python3 skills/obsidian-vault-sanitizer/scripts/audit_vault.py ~/Vault --move-orphans "_review/orphan-attachments"
```

Do not auto-infer replacements for broken note links. Require an explicit `OLD=NEW` mapping or use Obsidian-aware rename/move operations so the user's graph semantics are preserved.

Do not rename generic filenames automatically from note contents unless the user explicitly approves the final filename. Use the generated audit to propose candidates, then apply `--rename-note` with the approved mapping.

## Cleanup Policy

- Do not mass-delete orphan attachments unless the user explicitly approves the exact scope.
- Prefer moving orphan attachments to a review folder before deletion.
- Before deleting an attachment, check whether it is referenced by canvas files, plugin data, published content, or non-Markdown files. Load [references/remediation.md](references/remediation.md) for cleanup details.
- Before renaming notes, inspect duplicate basenames and aliases. Bare wikilinks resolve by note name and can become ambiguous.
- Preserve user-created folder structure unless the user asked for reorganization.
- Prefer adding aliases when a note has many existing inbound link names and the canonical title is being improved.
- Keep a changelog or audit report outside the vault when the user wants a reversible cleanup record.

## References to Load on Demand

- [references/remediation.md](references/remediation.md): safe correction patterns for broken links, orphan attachments, generic note filenames, duplicate note names, empty notes, and frontmatter problems.
- [references/audit-rules.md](references/audit-rules.md): details about link resolution assumptions, limitations, and manual verification points.

## Maintenance Hook

When updating this skill's `SKILL.md`, scripts, references, assets, or validation policy, append a concise entry to [docs/changelog.md](docs/changelog.md), in english (US). Create the file if missing.

Use newest-first entries with:

- date and short title
- changed files or areas
- reason for the change
- validation performed

Do not log ordinary vault audit outputs; log only changes to the skill itself.
