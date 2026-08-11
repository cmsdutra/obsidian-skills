# Recurring Pitfalls Reference

Use this file before editing syntax that often renders incorrectly or breaks Obsidian navigation.

## Wikilinks

```markdown
[[Note Name]]
[[Note Name|Display Text]]
[[Note Name#Heading]]
[[Note Name#^block-id]]
[[#Heading in same note]]
```

- Use wikilinks for vault-internal notes and attachments.
- Use Markdown links only for external URLs.
- If changing note names, aliases, headings, or attachment paths may affect links, switch to the vault's Obsidian CLI workflow.
- Heading links depend on the visible heading text. Avoid casual heading edits when notes link to that heading.

## Aliases

- Put aliases in frontmatter under `aliases`.
- Use aliases for alternative note names, not as replacements for stable note titles.
- When changing aliases on notes that other notes may reference by alias, check backlinks or use Obsidian-aware tooling.

## Embeds

```markdown
![[Note]]
![[Note#Heading]]
![[Note#^block-id]]
![[image.png|300]]
![[document.pdf#page=3]]
```

- A leading `!` embeds; without `!`, it links.
- Prefer vault attachment embeds over external image links when the file lives in the vault.
- Width syntax follows the pipe: `![[image.png|300]]`.

## Block IDs

```markdown
This paragraph can be linked. ^block-id
```

For lists or quotes, put the block ID on its own line after the block:

```markdown
- Item 1
- Item 2

^list-id
```

- Block IDs start with `^` and should be stable, lowercase, and readable.
- Do not attach block IDs to headings; use heading links for headings.

## Foldable Callouts

```markdown
> [!question]- Collapsed by default
> Hidden until opened.

> [!question]+ Expanded by default
> Visible but collapsible.
```

- Put `-` or `+` immediately after the callout type marker.
- Keep every body line inside the blockquote.

## Tags

- Valid tags can contain letters, numbers, underscores, hyphens, and forward slashes.
- Tags cannot start with a number.
- Use `#nested/tag` for hierarchy.
- In frontmatter, omit the leading `#`: use `tags: [project, nested/tag]` or a YAML list.

## Frontmatter YAML

```yaml
---
tags:
  - project
aliases:
  - Alternate Name
related: "[[Other Note]]"
---
```

- Frontmatter must be the first content in the file.
- Use one opening `---` and one closing `---`.
- Use YAML lists for multiple tags, aliases, cssclasses, or related links.
- Quote wikilinks and values with punctuation that YAML may misread.

## Canonical Docs

- [Obsidian Flavored Markdown](https://help.obsidian.md/obsidian-flavored-markdown)
- [Obsidian Internal links](https://help.obsidian.md/links)
- [Obsidian Embed files](https://help.obsidian.md/embeds)
- [Obsidian Callouts](https://help.obsidian.md/callouts)
- [Obsidian Properties](https://help.obsidian.md/properties)
- [Obsidian Tags](https://help.obsidian.md/tags)
