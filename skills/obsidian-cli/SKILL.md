---
name: obsidian-cli
description: Interact with Obsidian vaults using the Obsidian CLI to read, create, search, and manage notes, tasks, properties, backlinks, and link-safe graph operations. Use when the user asks to search or inspect vault content, query Obsidian metadata, scrape properties/frontmatter, rename or move linked notes and attachments safely, manage tasks, inspect backlinks/outgoing links, or run common vault operations from the command line.
---

# Obsidian CLI

Use the `obsidian` CLI to interact with a running Obsidian app. Prefer it over raw filesystem operations whenever Obsidian's index, link resolution, properties, backlinks, or tasks matter.

## Core Workflow

1. Confirm whether the task touches the graph: note names, paths, aliases, headings used as link targets, embedded or linked attachments, backlinks, outgoing links, tasks, properties, or tags.
2. If link integrity may be affected, load [link-safe-operations.md](references/link-safe-operations.md) before editing.
3. For routine reads and searches, use the CLI first when the answer depends on Obsidian indexing or metadata. Use direct filesystem reads only for narrow content inspection with low link risk.
4. For command syntax, run `obsidian help` or `obsidian help <command>` when available. Keep local examples as workflow reminders, not as a complete command reference.
5. If `obsidian` cannot connect to Obsidian, load [troubleshooting.md](references/troubleshooting.md).

## Essential Syntax

- Parameters use `name=value`; quote values with spaces.
- Flags are boolean switches with no value, such as `open`, `overwrite`, `total`, or `verbose`.
- Multiline content can use `\n`; tabs can use `\t`.
- If the current terminal directory is a vault, that vault is targeted by default. Otherwise the active vault is used.
- To target another vault, put `vault=<name>` or `vault=<id>` before the command.
- Use `file=<name>` for wikilink-style resolution by note name. Use `path=<vault-relative/path.md>` for an exact vault-relative path.
- Add `--copy` to copy command output to the clipboard.

```bash
obsidian vault="My Vault" search query="meeting notes" limit=10
obsidian read file="Project Plan"
obsidian read path="Projects/Project Plan.md"
obsidian create name="New Note" content="# Title\n\nBody" open
```

## References to Load on Demand

- [common-commands.md](references/common-commands.md): recurring command patterns for read, create, append/prepend, backlinks, links, tasks, tags, daily notes, files, and folders.
- [search-operations.md](references/search-operations.md): common text search, context search, property scraping, folder-scoped metadata queries, and structured result extraction.
- [link-safe-operations.md](references/link-safe-operations.md): required workflow for rename, move, delete, alias changes, heading target edits, referenced attachments, and backlink checks.
- [properties-metadata.md](references/properties-metadata.md): properties, aliases, tags, YAML/frontmatter-adjacent CLI workflows, and metadata inspection.
- [troubleshooting.md](references/troubleshooting.md): setup checks, official docs fallback, Linux/Flatpak socket issues, and the `unable to find Obsidian` workaround.

## Official Sources

- Current CLI behavior: <https://obsidian.md/help/cli>
- Obsidian Help for app behavior and Markdown syntax: <https://help.obsidian.md/>

When CLI syntax, command names, or app behavior may have changed, verify with `obsidian help` first. If local help is unavailable or ambiguous, check official Obsidian documentation before giving command-specific guidance.