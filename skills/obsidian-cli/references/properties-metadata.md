# Properties and Metadata

Use CLI metadata commands when the task depends on Obsidian's indexed properties, aliases, tags, task state, or active file context.

## Properties

```bash
obsidian properties path="Folder/Note.md" format=yaml
obsidian properties name=status counts
obsidian property:read path="Folder/Note.md" name=status
obsidian property:set path="Folder/Note.md" name=status value=done type=text
obsidian property:set path="Folder/Note.md" name=priority value=2 type=number
obsidian property:set path="Folder/Note.md" name=published value=true type=checkbox
obsidian property:remove path="Folder/Note.md" name=status
```

Use a property `type` when setting values so Obsidian can preserve property semantics. For complex YAML restructuring, inspect the file content before editing and keep Obsidian property conventions valid.

For folder-scoped or cross-file property extraction, load [search-operations.md](search-operations.md) and use the read-only `app.metadataCache` pattern there.

## Aliases

```bash
obsidian aliases total
obsidian aliases path="Folder/Note.md" verbose
obsidian property:read path="Folder/Note.md" name=aliases
obsidian property:set path="Folder/Note.md" name=aliases value="Short Name" type=list
```

Aliases can be link targets. Before removing or renaming an alias, load the link-safe workflow and search for links that use the old alias.

## Tags

```bash
obsidian tags counts sort=count
obsidian tags path="Folder/Note.md"
obsidian tag name="#project" verbose
```

For tag-heavy queries, prefer CLI tag commands or Obsidian search over raw `rg` because Obsidian handles tag semantics across frontmatter and body content.

## Tasks

```bash
obsidian tasks todo verbose
obsidian tasks done format=json
obsidian tasks path="Folder/Note.md" verbose
obsidian task ref="Folder/Note.md:18" toggle
obsidian task path="Folder/Note.md" line=18 done
```

When changing tasks, first get a stable `path:line` with `tasks verbose` unless the user targets the active daily note.

## Bases, Bookmarks, Workspace Context

For Obsidian-managed views and navigation state, prefer CLI inspection:

```bash
obsidian bases
obsidian base:views path="Dashboard.base"
obsidian base:query path="Dashboard.base" view="Open" format=json
obsidian bookmarks verbose
obsidian workspace ids
obsidian tabs ids
obsidian recents
```

Run `obsidian help <command>` for full options before automating these commands.
