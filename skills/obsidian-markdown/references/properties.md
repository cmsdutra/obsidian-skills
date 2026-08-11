# Properties (Frontmatter) Reference

Properties use YAML frontmatter at the start of a note. Add frontmatter only at the top of the file, between `---` delimiters.

```yaml
---
title: My Note Title
date: 2024-01-15
tags:
  - project
  - important
aliases:
  - My Note
  - Alternative Name
cssclasses:
  - custom-class
status: in-progress
rating: 4.5
completed: false
due: 2024-02-01T14:30:00
---
```

## Property Types

| Type | Example |
|------|---------|
| Text | `title: My Title` |
| Number | `rating: 4.5` |
| Checkbox | `completed: true` |
| Date | `date: 2024-01-15` |
| Date & Time | `due: 2024-01-15T14:30:00` |
| List | `tags: [one, two]` or YAML list |
| Links | `related: "[[Other Note]]"` |

Quote wikilinks in YAML values unless the value is a plain list item that Obsidian already handles correctly.

## Default Properties

- `tags` - Note tags (searchable, shown in graph view)
- `aliases` - Alternative names for the note (used in link suggestions)
- `cssclasses` - CSS classes applied to the note in reading/editing view

## Tags

```markdown
#tag
#nested/tag
#tag-with-dashes
#tag_with_underscores
```

Tags can contain: letters (any language), numbers (not first character), underscores `_`, hyphens `-`, forward slashes `/` (for nesting).

In frontmatter:

```yaml
---
tags:
  - tag1
  - nested/tag2
---
```

## YAML Pitfalls

- Keep indentation consistent with spaces, not tabs.
- Quote values containing `:`, `#`, `{}`, `[]`, leading `*`, or wikilinks when YAML parsing is ambiguous.
- Store multi-value properties as YAML lists when the user expects Obsidian to treat them as multiple values.
- Do not duplicate a property key in the same frontmatter block.

## Canonical Docs

- [Obsidian Properties](https://help.obsidian.md/properties)
- [Obsidian Tags](https://help.obsidian.md/tags)
