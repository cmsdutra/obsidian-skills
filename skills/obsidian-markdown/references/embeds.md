# Embeds Reference

Prefix a wikilink with `!` to embed its rendered content inline. Use embeds for notes, sections, blocks, images, PDFs, audio, video, and query blocks.

## Notes, Headings, and Blocks

```markdown
![[Note Name]]
![[Note Name#Heading]]
![[Note Name#^block-id]]
```

Use heading embeds for stable section-level transclusion. Use block embeds only when the target block ID is deliberate and unlikely to be removed.

## Embed Images

```markdown
![[image.png]]
![[image.png|640x480]]    Width x Height
![[image.png|300]]        Width only (maintains aspect ratio)
```

For vault attachments, prefer wikilink embeds so Obsidian can track file moves and renames.

## External Images

```markdown
![Alt text](https://example.com/image.png)
![Alt text|300](https://example.com/image.png)
```

## Embed Audio

```markdown
![[audio.mp3]]
![[audio.ogg]]
```

## Embed PDF

```markdown
![[document.pdf]]
![[document.pdf#page=3]]
![[document.pdf#height=400]]
```

## Embed Lists

```markdown
![[Note#^list-id]]
```

Where the list has a block ID:

```markdown
- Item 1
- Item 2
- Item 3

^list-id
```

## Embed Search Results

````markdown
```query
tag:#project status:done
```
````

## Canonical Docs

- [Obsidian Embed files](https://help.obsidian.md/embeds)
- [Obsidian Internal links](https://help.obsidian.md/links)
