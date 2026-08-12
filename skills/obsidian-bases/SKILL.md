---
name: obsidian-bases
description: Create and edit Obsidian Bases as .base files or inline Markdown base code blocks, with views, filters, formulas, summaries, and YAML validation. Use when working with database-like note views, table/card/list/map views, filters, calculated properties, embedded Bases, or Bases troubleshooting in Obsidian.
metadata:
  info: this skill was adapted from Kaparty's obsidian skills <https://github.com/kepano/obsidian-skills.git>
---

# Obsidian Bases

Use this skill to create, edit, troubleshoot, and validate Obsidian Bases, either as standalone `.base` files or as inline Markdown fenced code blocks with language `base`. Keep this file as the working procedure; load detailed references only for the part of Bases you are touching.

## Provenance

This skill was originally derived from Kepano's `obsidian-skills` repository: https://github.com/kepano/obsidian-skills.git. This local version includes modifications from the original project.

## Workflow

1. Clarify the dataset: identify which notes or files should appear, which note properties exist, and whether attachments should be included. If the user wants only notes, include `file.ext == "md"`.
2. Draft or edit valid Bases YAML in a standalone `.base` file or inside a Markdown fenced code block opened with ```` ```base ````. Do not use ```` ```yaml ```` for inline Bases meant to render in Obsidian.
3. Define global `filters` only for constraints shared by every view. Put view-specific constraints under that view.
4. Add `formulas` only when a displayed or filtered value must be computed. Reference formula outputs as `formula.name` in `order`, `properties`, summaries, filters, and other formulas.
5. Configure `properties` for display metadata and one or more `views` with `type`, `name`, `order`, and optional `filters`, `limit`, `groupBy`, and `summaries`.
6. Validate YAML syntax for every `.base` file you create or modify. Then inspect references: every `formula.x` used outside `formulas` must have a matching `formulas.x`.
7. When behavior is uncertain, suspect stale syntax, or an error conflicts with this skill, check the official Obsidian Bases docs first.

## Reference Routing

- Schema and top-level keys: read [references/schema.md](references/schema.md).
- Filters, nested `and`/`or`/`not`, and operators: read [references/filters.md](references/filters.md).
- Formulas, property namespaces, dates, durations, and common calculations: read [references/formulas.md](references/formulas.md).
- Table, cards, list, and map view configuration: read [references/views.md](references/views.md).
- Built-in and custom summaries: read [references/summaries.md](references/summaries.md).
- Complete function list: read [references/function-reference.md](references/function-reference.md). Do not copy the whole function reference into working answers unless the user asks for it.
- Realistic `.base` examples: read [references/examples.md](references/examples.md).
- Recurrent failure modes and YAML quoting traps: read [references/pitfalls.md](references/pitfalls.md).

## Canonical Docs

Use these official pages when in doubt or when this skill may be stale:

- https://obsidian.md/help/bases
- https://obsidian.md/help/bases/create-base
- https://obsidian.md/help/bases/syntax
- https://obsidian.md/help/bases/functions
- https://obsidian.md/help/bases/views
- https://obsidian.md/help/formulas

## Validation Checklist

- Run a YAML parser on changed `.base` files and on the contents of changed inline ```` ```base ```` blocks.
- Confirm `views` is a list and each view has at least `type` and `name`.
- Confirm filters are either strings or recursive objects using `and`, `or`, or `not`.
- Confirm formula expressions are YAML strings, especially when they contain quotes.
- Confirm `formula.name` references match entries under `formulas`.
- Prefer `note.property` or bare `property` for frontmatter and `file.*` for file metadata; do not invent `file.propertyName` for note properties.
- For date subtraction, do not assume `.days` is invalid: this vault has working Bases that use `(today() - note["submitted"]).days`. Official docs describe millisecond differences, so preserve tested `.days` formulas and verify in Obsidian before replacing them.
- Open or test in Obsidian when YAML is valid but rendering behavior remains uncertain.
