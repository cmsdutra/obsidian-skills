# JSON Canvas Pitfalls

## Duplicate IDs

IDs must be unique across both arrays, not just within `nodes` or within `edges`. Reusing a node ID as an edge ID can cause ambiguous behavior.

## Dangling Edge References

Every edge must reference existing node IDs:

- `fromNode` must match a node `id`.
- `toNode` must match a node `id`.
- Edges cannot connect to edge IDs.

After deleting or replacing a node, remove or update its edges.

## Negative Coordinates

Negative `x` and `y` values are valid. Do not "fix" them unless the layout itself is wrong. Obsidian Canvas is an infinite plane.

## Z-Index Is Array Order

Node order controls stacking:

- Earlier node = lower layer.
- Later node = upper layer.
- Put groups before their visual children so groups do not cover cards.

## JSON Newlines

Inside JSON string values, line breaks must be escaped as `\n`.

Correct:

```json
"text": "# Title\n\nBody"
```

Incorrect:

```json
"text": "# Title\\n\\nBody"
```

The incorrect form renders literal backslash-n characters in Obsidian.

Also avoid raw unescaped line breaks inside JSON strings; they make the JSON invalid.

## Vault File Paths

For file nodes, use paths relative to the vault root:

```json
"file": "Notes/Meeting Notes.md"
```

Do not use absolute system paths for normal vault files:

```json
"file": "/home/user/Vault/Notes/Meeting Notes.md"
```

When pointing to a note heading or block, use `subpath`:

```json
"file": "Notes/Meeting Notes.md",
"subpath": "#Decisions"
```

If the task requires renaming or moving referenced notes or attachments, use the vault's Obsidian CLI workflow so links and backlinks can be updated safely.

## Group Misconceptions

Groups are visual rectangles. They do not store child node IDs. Moving a group by changing its `x` and `y` leaves child nodes where they were unless those child nodes are moved too.

## Type-Specific Required Fields

Common invalid nodes:

- `text` node without `text`.
- `file` node without `file`.
- `link` node without `url`.
- `group` node treated as if it owned child IDs.

## Overwriting Existing Canvas Conventions

When editing an existing file, preserve local conventions for:

- ID length and casing, if consistent.
- Spacing and grid.
- Color usage.
- Edge direction and labels.
- Node ordering.
