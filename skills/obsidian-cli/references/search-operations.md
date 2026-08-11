# Search Operations

Use this reference for common vault searches. Prefer Obsidian CLI search when the query depends on Obsidian's index, tags, property cache, link resolution, or folder-scoped vault semantics.

## Text Search

Use `search` for matching file paths:

```bash
obsidian search query="meeting notes" limit=20
obsidian search query="tag:#project" format=json
obsidian search query="term" total
obsidian search query="term" path="300_Trabalho" limit=20
```

Use `search:context` when the answer needs matching lines:

```bash
obsidian search:context query="TODO" limit=20
obsidian search:context query="status:" path="300_Trabalho" limit=50
obsidian search:context query="[[Target Note" limit=50
```

Use `case` only when case-sensitive matching matters. Use `format=json` when another command or script will parse the output.

## Open Search in Obsidian

Use this when the user wants the app view opened rather than command output:

```bash
obsidian search:open query="meeting notes"
```

## Property and Frontmatter Scraping

For simple property counts or single-file reads, use metadata commands:

```bash
obsidian properties name=status counts
obsidian properties path="Folder/Note.md" format=yaml
obsidian property:read path="Folder/Note.md" name=status
```

For structured lists across many files, use read-only `obsidian eval` against `app.metadataCache`. This is faster and cleaner than grepping frontmatter because it uses Obsidian's parsed cache.

List markdown files in a folder with their frontmatter:

```bash
obsidian eval code="app.vault.getMarkdownFiles().filter(f => f.path.startsWith('300_Trabalho/')).map(f => ({ path: f.path, properties: app.metadataCache.getFileCache(f)?.frontmatter ?? {} }))"
```

Filter by property value:

```bash
obsidian eval code="app.vault.getMarkdownFiles().filter(f => f.path.startsWith('300_Trabalho/')).map(f => ({ path: f.path, props: app.metadataCache.getFileCache(f)?.frontmatter })).filter(x => x.props?.status === 'active')"
```

Extract selected fields for a clean result:

```bash
obsidian eval code="app.vault.getMarkdownFiles().filter(f => f.path.startsWith('300_Trabalho/')).map(f => { const fm = app.metadataCache.getFileCache(f)?.frontmatter ?? {}; return { name: f.basename, path: f.path, title: fm.title, due: fm.due, status: fm.status }; })"
```

## Safer Eval Rules

- Use `eval` for read-only metadata extraction unless the user explicitly asks for mutation.
- Filter by `f.path.startsWith('Folder/')` before mapping large vaults when the scope is known.
- Include `path` in structured results so later edits can target exact files.
- Use optional chaining and defaults, such as `?.frontmatter ?? {}`, because not every file has frontmatter.
- Keep eval snippets single-purpose. If the query becomes complex, first inspect a small sample with `limit` logic, then broaden it.

## Link and Target Searches

Use Obsidian's link commands when the target is known:

```bash
obsidian backlinks path="Folder/Target.md" counts
obsidian links path="Folder/Source.md"
obsidian unresolved verbose
```

Use context search for partial aliases, heading links, embeds, or attachment filenames:

```bash
obsidian search:context query="[[Old Alias" limit=50
obsidian search:context query="[[Note#Old Heading" limit=50
obsidian search:context query="attachment.pdf" limit=50
```
