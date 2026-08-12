# Vault Remediation Patterns

Use these patterns after a read-only audit. Prefer small batches and rerun the audit after each meaningful change.

## Broken Links

1. Resolve the intended target by searching for similar basenames, aliases, and headings.
2. If the target exists under a different path, prefer an Obsidian-aware rename or move command so backlinks are updated.
3. If only the display text is wrong, update the link alias without changing the target.
4. If the target is intentionally missing, create the note only when the user wants the knowledge gap represented in the vault.

For exact user-approved replacements, use the audit script:

```bash
python3 scripts/audit_vault.py /path/to/vault --fix-link "Old Target=New Target"
python3 scripts/audit_vault.py /path/to/vault --fix-link "Old Target=New Target" --apply
```

Do not use guessed replacements for broken links. A filename similarity match is only evidence to present to the user or to verify manually.

## Missing Heading Or Block Targets

- Check whether the heading was renamed, duplicated, or nested differently.
- Avoid changing headings that have many inbound links until backlinks are inspected.
- For durable references to volatile text, add a block ID near the intended paragraph and link to `[[Note#^block-id]]`.

## Orphan Attachments

1. Inspect the file type, name, modified date, and nearby notes before proposing deletion.
2. Search non-Markdown files such as `.canvas`, plugin JSON, templates, and exported pages for the attachment name.
3. Move candidates to a review folder when the user wants a reversible cleanup.
4. Delete only after explicit approval.

Use `--move-orphans "_review/orphan-attachments"` for a dry-run move plan, then add `--apply` after approval.

## Generic Filename Notes

- Treat files named `Untitled.md`, `New Note.md`, `Sem título 1.md`, or similar as candidates, not automatic defects.
- Prefer a filename matching the stable concept of the note.
- Do not infer the final filename without user approval; note content can suggest candidates, but the chosen filename is a semantic decision.
- Use `--rename-note "Sem título 1=Projetos/Resumo da reunião"` for a dry-run rename plan, then add `--apply`.
- When renaming outside Obsidian, update wikilinks and Markdown links that targeted the old filename. The script handles exact filename targets for `--rename-note`.
- Add aliases for previous names only when inbound search habits depend on them; avoid aliases like `Sem título 1` unless the user wants to preserve that lookup.

## Duplicate Note Names

- Duplicate basenames make bare wikilinks ambiguous.
- Resolve by either renaming one note to a more specific name or converting affected bare links to path-qualified links.
- Check aliases before renaming; an alias can also create ambiguous resolution in Obsidian.

## Empty Notes

- Empty notes can be placeholders, daily notes, map-of-content stubs, or accidental files.
- Do not delete empty notes without checking backlinks and folder conventions.
- If retained as a placeholder, add a minimal heading or property that explains its purpose.

## Frontmatter Problems

- Keep YAML between leading `---` fences.
- Quote values with colons, brackets, hashes, or leading special characters.
- Use lists for `tags`, `aliases`, and multi-value properties when the vault conventions expect lists.
- Preserve property ordering when it appears intentional.
