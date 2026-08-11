# Common Commands

Use this as a compact reminder for recurring workflows. For complete syntax, run `obsidian help` or `obsidian help <command>`.

## Read and Locate

```bash
obsidian read file="Note Name"
obsidian read path="Folder/Note Name.md"
obsidian file file="Note Name"
obsidian files folder="Folder" ext=md
obsidian folders folder="Folder"
obsidian vault info=path
obsidian vaults verbose
```

Use `file` when Obsidian should resolve a note like a wikilink. Use `path` when there are duplicate names or when exact targeting matters.

## Create and Edit Content

```bash
obsidian create name="New Note" content="# New Note\n\nBody"
obsidian create path="Folder/New Note.md" template="Template Name" open
obsidian append file="Existing Note" content="- [ ] Follow up"
obsidian prepend path="Folder/Existing Note.md" content="Pinned note" inline
```

Before overwriting existing files, inspect the current file and backlinks. For renames or moves, use the link-safe workflow instead of filesystem operations.

## Links and Backlinks

```bash
obsidian backlinks file="Note Name" counts
obsidian backlinks path="Folder/Note Name.md" format=json
obsidian links file="Note Name"
obsidian unresolved verbose
obsidian orphans total
obsidian deadends total
```

Use these before and after operations that may alter link targets.

## Daily Notes and Tasks

```bash
obsidian daily
obsidian daily:read
obsidian daily:append content="- [ ] New task"
obsidian tasks todo verbose
obsidian tasks daily total
obsidian task ref="Folder/Note.md:42" done
obsidian task daily line=3 toggle
```

When updating an existing task, prefer `ref=<path:line>` or `path` plus `line` from `tasks verbose`.

## Tags, Templates, History

```bash
obsidian tags counts sort=count
obsidian tag name="#project" verbose
obsidian templates total
obsidian template:read name="Template Name" resolve title="Draft"
obsidian diff file="Note Name" from=1
obsidian history file="Note Name"
```

Use `diff`, `history`, and Sync commands before risky edits when local recovery context matters.
