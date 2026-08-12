---
name: obsidian-markdown
description: Create and edit Obsidian Flavored Markdown with wikilinks, embeds, callouts, properties, and other Obsidian-specific syntax. Use when working with .md files in Obsidian, or when the user mentions wikilinks, callouts, frontmatter, tags, embeds, or Obsidian notes.
---

# Obsidian Flavored Markdown Skill

Create and edit valid Obsidian Flavored Markdown. This skill covers Obsidian-specific syntax only; assume standard Markdown knowledge.

## Core Workflow

1. Confirm the operation is safe for direct file editing. If the task may break links, headings, aliases, attachments, or backlinks, use the vault's Obsidian CLI workflow instead of plain filesystem edits.
2. For new notes, add YAML frontmatter only when useful. Keep properties valid YAML and use Obsidian property conventions.
3. Use wikilinks for vault-internal targets and Markdown links only for external URLs.
4. Use embeds, callouts, block IDs, tags, comments, math, Mermaid, and highlights according to the relevant reference below.
5. After editing, check the affected Markdown for syntax that could fail in Obsidian reading view.

## References to Load on Demand

- [properties.md](references/properties.md): frontmatter, aliases, tags, cssclasses, property types, YAML pitfalls.
- [embeds.md](references/embeds.md): embedded notes, headings, blocks, images, PDFs, media, searches.
- [callouts.md](references/callouts.md): callout types, aliases, custom titles, nested and foldable callouts.
- [pitfalls.md](references/pitfalls.md): recurring mistakes with wikilinks, aliases, embeds, block IDs, foldable callouts, tags, and YAML.

## Fast Syntax Reminders

- Internal note: `[[Note]]`
- Internal note with display text: `[[Note|Text]]`
- Heading target: `[[Note#Heading]]`
- Block target: `[[Note#^block-id]]`
- Embed: `![[Note]]`, `![[image.png|300]]`, `![[document.pdf#page=3]]`
- Callout: `> [!note] Title`
- Foldable callout: `> [!question]- Title` or `> [!question]+ Title`
- Tags: `#tag`, `#nested/tag`, or YAML `tags`
- Hidden comments: `%%comment%%`
- Highlight: `==text==`

## Canonical Docs

- [Obsidian Flavored Markdown](https://help.obsidian.md/obsidian-flavored-markdown)
- [Internal links](https://help.obsidian.md/links)
- [Embed files](https://help.obsidian.md/embeds)
- [Callouts](https://help.obsidian.md/callouts)
- [Properties](https://help.obsidian.md/properties)
