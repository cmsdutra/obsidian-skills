# Canvas Validation

Always validate `.canvas` files and changed examples before finishing.

## Required Checks

1. JSON parses successfully.
2. Top level is an object.
3. `nodes` and `edges`, when present, are arrays.
4. All node and edge IDs are unique.
5. Every node has `id`, `type`, `x`, `y`, `width`, and `height`.
6. Text nodes have `text`.
7. File nodes have `file`.
8. Link nodes have `url`.
9. Group nodes do not require extra fields.
10. Edge `fromNode` and `toNode` values reference existing node IDs.
11. Side values are `top`, `right`, `bottom`, or `left`.
12. End values are `none` or `arrow`.
13. Color values are preset strings `"1"` through `"6"` or hex colors like `"#ff0000"`.

## One-Off Python Validator

Use this pattern for files or extracted examples:

```python
import json
import re
from pathlib import Path

SIDES = {"top", "right", "bottom", "left"}
ENDS = {"none", "arrow"}
TYPES = {"text", "file", "link", "group"}
HEX_COLOR = re.compile(r"^#[0-9a-fA-F]{6}$")

def valid_color(value):
    return value in {"1", "2", "3", "4", "5", "6"} or bool(HEX_COLOR.match(value))

def validate_canvas(data, label="<canvas>"):
    assert isinstance(data, dict), f"{label}: top level must be object"
    nodes = data.get("nodes", [])
    edges = data.get("edges", [])
    assert isinstance(nodes, list), f"{label}: nodes must be array"
    assert isinstance(edges, list), f"{label}: edges must be array"

    ids = []
    node_ids = set()
    for node in nodes:
        for field in ("id", "type", "x", "y", "width", "height"):
            assert field in node, f"{label}: node missing {field}: {node}"
        assert node["type"] in TYPES, f"{label}: invalid node type {node['type']}"
        if node["type"] == "text":
            assert "text" in node, f"{label}: text node missing text"
        if node["type"] == "file":
            assert "file" in node, f"{label}: file node missing file"
        if node["type"] == "link":
            assert "url" in node, f"{label}: link node missing url"
        if "color" in node:
            assert valid_color(node["color"]), f"{label}: invalid node color {node['color']}"
        ids.append(node["id"])
        node_ids.add(node["id"])

    for edge in edges:
        for field in ("id", "fromNode", "toNode"):
            assert field in edge, f"{label}: edge missing {field}: {edge}"
        assert edge["fromNode"] in node_ids, f"{label}: dangling fromNode {edge['fromNode']}"
        assert edge["toNode"] in node_ids, f"{label}: dangling toNode {edge['toNode']}"
        if "fromSide" in edge:
            assert edge["fromSide"] in SIDES, f"{label}: invalid fromSide {edge['fromSide']}"
        if "toSide" in edge:
            assert edge["toSide"] in SIDES, f"{label}: invalid toSide {edge['toSide']}"
        if "fromEnd" in edge:
            assert edge["fromEnd"] in ENDS, f"{label}: invalid fromEnd {edge['fromEnd']}"
        if "toEnd" in edge:
            assert edge["toEnd"] in ENDS, f"{label}: invalid toEnd {edge['toEnd']}"
        if "color" in edge:
            assert valid_color(edge["color"]), f"{label}: invalid edge color {edge['color']}"
        ids.append(edge["id"])

    assert len(ids) == len(set(ids)), f"{label}: duplicate IDs"

validate_canvas(json.loads(Path("example.canvas").read_text()))
```

## Skill Folder Validation

After editing this skill, run:

```bash
python3 /home/caio/.codex/skills/.system/skill-creator/scripts/quick_validate.py /home/caio/Chaos/.codex/skills/obsidian-canvas
```
