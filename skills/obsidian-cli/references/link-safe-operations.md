# Link-Safe Operations

Use this workflow for any operation with meaningful risk of broken links or stale Obsidian graph state.

## Required Cases

Use Obsidian CLI instead of raw filesystem edits for:

- renaming notes
- moving notes or folders containing linked notes
- deleting notes that may have backlinks
- changing aliases used as link targets
- editing headings targeted by `[[Note#Heading]]`
- moving, renaming, or deleting referenced attachments
- reorganizing embedded images, PDFs, media, or other linked assets
- any edit where Obsidian should update links/backlinks automatically

This matches the vault policy in `AGENTS.md`: direct filesystem edits are acceptable for low-risk content edits, but graph-sensitive operations must use Obsidian-aware workflows.

## Preflight

1. Identify the exact target with `obsidian file`, `obsidian read`, `obsidian files`, or `obsidian search`.
2. Prefer `path=` for duplicate note names or attachments.
3. Capture incoming and outgoing references:

```bash
obsidian backlinks path="Folder/Note.md" counts
obsidian links path="Folder/Note.md"
obsidian unresolved verbose
```

4. If changing a heading, inspect heading targets:

```bash
obsidian outline path="Folder/Note.md" format=json
obsidian search:context query="[[Note#Old Heading" limit=50
```

5. If moving or deleting an attachment, search for both wiki embeds and Markdown links:

```bash
obsidian search:context query="attachment.png" limit=50
obsidian backlinks path="Attachments/attachment.png" counts
```

## Rename or Move Notes

Use CLI commands so Obsidian can apply its internal link-update behavior when the vault setting for automatic internal link updates is enabled.

```bash
obsidian rename path="Folder/Old Name.md" name="New Name"
obsidian move path="Folder/Old Name.md" to="Archive/New Name.md"
```

After the operation:

```bash
obsidian backlinks path="Archive/New Name.md" counts
obsidian links path="Archive/New Name.md"
obsidian unresolved verbose
```

If unresolved links increased, inspect the affected sources before making more edits.

## Alias Changes

Aliases live in note properties and can be link targets. Before changing them:

```bash
obsidian aliases path="Folder/Note.md" verbose
obsidian search:context query="[[Old Alias" limit=50
obsidian property:read path="Folder/Note.md" name=aliases
```

Use property commands when possible:

```bash
obsidian property:set path="Folder/Note.md" name=aliases value="New Alias" type=list
```

Afterward, run `obsidian unresolved verbose` and search for the old alias if it should no longer be used.

## Heading Target Changes

Changing a heading can break `[[Note#Heading]]` links because Obsidian does not treat arbitrary heading text like a file rename. Before editing:

```bash
obsidian outline path="Folder/Note.md" format=json
obsidian search:context query="[[Note#Old Heading" limit=50
```

When possible, preserve the old heading or add a stable block ID target near the content:

```markdown
Relevant paragraph. ^stable-target
```

Then update references intentionally to `[[Note#^stable-target]]` if needed. Verify with `obsidian unresolved verbose`.

## Referenced Attachments

Before moving or renaming an attachment:

```bash
obsidian backlinks path="Attachments/file.pdf" counts
obsidian search:context query="file.pdf" limit=50
```

Use `obsidian move` or `obsidian rename` for the attachment path when possible:

```bash
obsidian move path="Attachments/file.pdf" to="Sources/file.pdf"
```

Then verify embeds and links still resolve:

```bash
obsidian unresolved verbose
obsidian search:context query="file.pdf" limit=50
```

## Deletion

Avoid permanent deletion unless explicitly requested.

```bash
obsidian backlinks path="Folder/Note.md" counts
obsidian links path="Folder/Note.md"
obsidian delete path="Folder/Note.md"
```

Only use `permanent` after confirming the target, backlinks, and recovery expectations.
