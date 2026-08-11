# Canvas Layout Patterns

Coordinates are an infinite 2D plane:

- `x` increases to the right.
- `y` increases downward.
- `x` and `y` identify the top-left corner.
- Negative coordinates are valid.

## Z-Index

Node array order controls stacking. Earlier nodes render below later nodes.

Practical ordering:

1. Groups first.
2. Background or overview nodes next.
3. Primary content nodes after that.
4. Emphasis, annotations, and small overlay nodes last.

## Spacing

- Keep 50-100 px between related cards.
- Keep 20-50 px between a group boundary and its contained nodes.
- Align positions and dimensions to 10 or 20 px increments.
- Preserve existing spacing conventions when editing a canvas.

## Suggested Sizes

| Node type | Width | Height |
| --- | --- | --- |
| Small text | 200-300 | 80-150 |
| Medium text | 300-450 | 150-300 |
| Large text | 400-600 | 300-500 |
| File preview | 300-500 | 200-400 |
| Link preview | 250-400 | 100-200 |
| Group | Fit contained nodes plus padding | Fit contained nodes plus padding |

## Common Patterns

### Mind Map

- Put the central concept near `(0, 0)`.
- Place branches left/right or radially around it.
- Use sides that match direction: central `right` to branch `left`, central `left` to branch `right`.

### Flowchart

- Use a single dominant direction, usually top-to-bottom.
- Align steps on one axis.
- Put alternate branches beside the decision node and label edges.

### Project Board

- Use group nodes as columns.
- Put group nodes before task nodes in the node array.
- Give each column identical width and height unless content clearly requires otherwise.
- Keep task nodes fully inside their column group.

### Research Canvas

- Put the synthesis or question node in the center.
- Place source file/link nodes around it.
- Use labels on edges to capture evidence roles such as `supports`, `contradicts`, or `source`.

## Group Containment

Groups do not contain child IDs. Containment is visual only:

- A node is "inside" a group when its rectangle falls inside the group's bounds.
- Moving a group in JSON does not automatically move nodes inside it.
- When resizing a group, keep all intended child nodes inside its bounds.
