# Views

Official sources:

- https://obsidian.md/help/bases/views
- https://obsidian.md/help/bases/syntax

Each entry under `views` defines one presentation of the same filtered dataset. Built-in view types include `table`, `cards`, `list`, and `map`; community plugins may add more.

## Table

```yaml
views:
  - type: table
    name: "Tasks"
    order:
      - file.name
      - status
      - due
      - formula.days_until_due
    groupBy:
      property: status
      direction: ASC
    summaries:
      formula.days_until_due: Average
```

## Cards

```yaml
views:
  - type: cards
    name: "Library"
    order:
      - cover
      - file.name
      - author
      - formula.status_icon
```

## List

```yaml
views:
  - type: list
    name: "Recent"
    order:
      - file.name
      - file.mtime
```

## Map

```yaml
views:
  - type: map
    name: "Locations"
    order:
      - file.name
      - location
```

Map rendering depends on available location properties and Obsidian/plugin support. Check the current docs or plugin documentation before assuming latitude/longitude key names.
