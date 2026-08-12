# Changelog

## 2026-08-11 - Generic filename rename flow

- Changed files or areas: `SKILL.md`, `scripts/audit_vault.py`, `references/remediation.md`, `agents/openai.yaml`.
- Reason for the change: clarify that "untitled notes" means generic filenames such as `Sem título 1.md`, and add explicit note file rename support with link updates.
- Validation performed: AST syntax parse, `quick_validate.py`, manifest JSON validation, and synthetic vault test renaming `Sem título 1.md` while updating a wikilink.

## 2026-08-11 - Controlled correction mode

- Changed files or areas: `SKILL.md`, `scripts/audit_vault.py`, `references/remediation.md`.
- Reason for the change: add user-approved correction support for exact link replacements, missing H1 insertion, and orphan attachment review moves.
- Validation performed: AST syntax parse, `quick_validate.py`, and synthetic vault tests for dry-run and applied fixes with report files inside the vault.

## 2026-08-11 - Initial vault sanitizer skill

- Changed files or areas: `SKILL.md`, `scripts/audit_vault.py`, `references/remediation.md`, `references/audit-rules.md`.
- Reason for the change: add an Obsidian vault hygiene workflow covering broken links, orphan attachments, untitled notes, duplicate names, and safe cleanup policy.
- Validation performed: `python3 -m py_compile scripts/audit_vault.py`, `quick_validate.py`, and synthetic vault audits with clean and intentionally broken links.
