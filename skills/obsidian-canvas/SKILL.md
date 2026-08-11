---
name: obsidian-canvas
description: Create and edit JSON Canvas files (.canvas) for Obsidian with nodes, edges, groups, file/link/text cards, layout, and validation. Use when Codex works with .canvas files, JSON Canvas structure, visual maps, mind maps, flowcharts, project boards, or Canvas files inside an Obsidian vault.
---

# JSON Canvas

Use this skill to create or edit `.canvas` files that follow the JSON Canvas format used by Obsidian.

Canonical sources:

- JSON Canvas specification: https://jsoncanvas.org/spec/1.0/
- JSON Canvas repository: https://github.com/obsidianmd/jsoncanvas
- Obsidian Canvas documentation: https://help.obsidian.md/plugins/canvas

Keep repository instructions practical and tested. Prefer the canonical sources when exact schema behavior is in doubt.

## Core Workflow

1. Parse the existing `.canvas` file as JSON, or start a new file with:

```json
{
  "nodes": [],
  "edges": []
}
```

2. Build or modify nodes first. Every node needs `id`, `type`, `x`, `y`, `width`, and `height`.
3. Build or modify edges only after node IDs are known. Every edge must point to existing node IDs through `fromNode` and `toNode`.
4. Choose a layout intentionally: avoid overlaps unless the user requested stacking, leave spacing, and use groups as visual containers rather than ownership metadata.
5. Write valid JSON. Escape line breaks in text values as `\n`.
6. Validate JSON syntax, unique IDs, node required fields, enum values, and edge integrity before finishing.

## When To Read References

- For exact object fields and allowed values, read [references/SCHEMA.md](references/SCHEMA.md).
- For concrete full-file examples, read [references/EXAMPLES.md](references/EXAMPLES.md).
- For spatial planning, groups, spacing, and z-index behavior, read [references/LAYOUT.md](references/LAYOUT.md).
- For deterministic checks and example validation, read [references/VALIDATION.md](references/VALIDATION.md).
- For recurring mistakes that break rendering or links, read [references/PITFALLS.md](references/PITFALLS.md).

## Common Tasks

### Create a Canvas

1. Choose a structure that matches the request: map, flow, board, timeline, comparison, or grouped workspace.
2. Generate unique lowercase hex IDs, preferably 16 characters.
3. Add nodes in bottom-to-top visual order. Put group nodes before the nodes that sit inside them.
4. Add edges after all connected nodes exist.
5. Validate the finished file.

### Add Nodes

1. Read the current nodes and edges.
2. Generate IDs that do not collide with any existing node or edge ID.
3. Place new nodes near related content with 50-100 px spacing.
4. If placing a node inside a group, make its rectangle fall inside the group bounds with visible padding.
5. Append or insert the node at the desired z-index position, then validate.

### Connect Nodes

1. Identify the exact source and target node IDs.
2. Create a unique edge ID.
3. Set `fromNode` and `toNode`; use `fromSide` and `toSide` when it improves routing clarity.
4. Add `label`, `color`, `fromEnd`, or `toEnd` only when useful.
5. Validate that every edge endpoint exists.

### Edit Layout

1. Preserve node IDs unless the user explicitly asks to replace nodes.
2. Move connected nodes together when needed so edges remain readable.
3. Keep coordinates as integers; negative coordinates are valid.
4. Remember that array order controls z-index: later nodes render above earlier nodes.
5. Validate after moving groups, because group containment is visual and can become inconsistent.

## Practical Defaults

- Text node: 260-450 px wide, 100-260 px high.
- File node: 300-500 px wide, 200-400 px high.
- Link node: 250-400 px wide, 100-200 px high.
- Group node: add 20-50 px padding around contained nodes.
- Horizontal spacing: 50-100 px between related nodes.
- Grid: align positions and sizes to 10 or 20 px increments unless matching an existing canvas.

## Obsidian Vault Notes

- For `file` nodes, use vault-relative paths such as `Notes/Example.md` or `Attachments/diagram.png`.
- For headings or block targets, use `subpath` values like `#Heading` or `#^block-id`.
- If changing real note names, attachment paths, aliases, headings used as link targets, or other graph-sensitive content in the vault, use the Obsidian CLI workflow required by the vault instructions.
- Editing a `.canvas` JSON file directly is acceptable when the edit only changes canvas structure, coordinates, labels, colors, text-node content, or existing valid file-node references.

## Final Checks

Before answering the user:

1. Confirm the file parses as JSON.
2. Confirm all node and edge IDs are unique.
3. Confirm all edge `fromNode` and `toNode` references resolve to existing node IDs.
4. Confirm required fields are present for each node type.
5. Confirm `type`, side, end, and color values are valid.
6. For changed examples or bundled resources, run the validation approach in [references/VALIDATION.md](references/VALIDATION.md).
