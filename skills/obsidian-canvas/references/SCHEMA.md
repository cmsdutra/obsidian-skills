# JSON Canvas Schema Notes

Use the JSON Canvas specification as the canonical source: https://jsoncanvas.org/spec/1.0/

This file records practical fields and values used by Obsidian-compatible `.canvas` files.

## Top Level

```json
{
  "nodes": [],
  "edges": []
}
```

- `nodes`: array of node objects.
- `edges`: array of edge objects.
- Unknown extra fields may be tolerated by some apps, but avoid them unless preserving an existing file.

## Shared Node Fields

| Field | Required | Type | Notes |
| --- | --- | --- | --- |
| `id` | Yes | string | Unique across nodes and edges. Prefer 16 lowercase hex characters. |
| `type` | Yes | string | `text`, `file`, `link`, or `group`. |
| `x` | Yes | integer | Top-left X coordinate in pixels. |
| `y` | Yes | integer | Top-left Y coordinate in pixels. |
| `width` | Yes | integer | Width in pixels. |
| `height` | Yes | integer | Height in pixels. |
| `color` | No | string | Preset `"1"` through `"6"` or hex color such as `"#ff0000"`. |

## Text Nodes

Required extra field:

- `text`: Markdown-capable plain string.

```json
{
  "id": "6f0ad84f44ce9c17",
  "type": "text",
  "x": 0,
  "y": 0,
  "width": 400,
  "height": 180,
  "text": "# Topic\n\nBody text."
}
```

## File Nodes

Required extra field:

- `file`: vault-relative path or a path already used by the canvas.

Optional field:

- `subpath`: heading or block target, for example `#Heading` or `#^block-id`.

```json
{
  "id": "a1b2c3d4e5f67890",
  "type": "file",
  "x": 500,
  "y": 0,
  "width": 400,
  "height": 300,
  "file": "Attachments/diagram.png"
}
```

## Link Nodes

Required extra field:

- `url`: external URL.

```json
{
  "id": "c3d4e5f678901234",
  "type": "link",
  "x": 1000,
  "y": 0,
  "width": 360,
  "height": 160,
  "url": "https://obsidian.md"
}
```

## Group Nodes

Optional extra fields:

- `label`: group title.
- `background`: vault-relative image path.
- `backgroundStyle`: `cover`, `ratio`, or `repeat`.

Groups are visual containers. They do not own child nodes in JSON.

```json
{
  "id": "d4e5f6789012345a",
  "type": "group",
  "x": -50,
  "y": -50,
  "width": 1000,
  "height": 600,
  "label": "Project Overview",
  "color": "4"
}
```

## Edges

| Field | Required | Type | Notes |
| --- | --- | --- | --- |
| `id` | Yes | string | Unique across nodes and edges. |
| `fromNode` | Yes | string | Source node ID. |
| `toNode` | Yes | string | Target node ID. |
| `fromSide` | No | string | `top`, `right`, `bottom`, or `left`. |
| `toSide` | No | string | `top`, `right`, `bottom`, or `left`. |
| `fromEnd` | No | string | `none` or `arrow`; default is usually no arrow. |
| `toEnd` | No | string | `none` or `arrow`; default is usually arrow. |
| `color` | No | string | Preset `"1"` through `"6"` or hex color. |
| `label` | No | string | Edge label. |

```json
{
  "id": "0123456789abcdef",
  "fromNode": "6f0ad84f44ce9c17",
  "fromSide": "right",
  "toNode": "a1b2c3d4e5f67890",
  "toSide": "left",
  "toEnd": "arrow",
  "label": "leads to"
}
```

## Color Presets

Preset values are strings. Applications choose their own exact colors.

| Preset | Common meaning |
| --- | --- |
| `"1"` | Red |
| `"2"` | Orange |
| `"3"` | Yellow |
| `"4"` | Green |
| `"5"` | Cyan |
| `"6"` | Purple |
