# Bases Schema

Official sources:

- https://obsidian.md/help/bases/syntax
- https://obsidian.md/help/bases/create-base

Bases can be stored as standalone `.base` files or embedded directly in Markdown notes as fenced code blocks using the `base` language. In both forms, the Base contents must be valid YAML. A base can include global filters, formulas, property display configuration, custom summaries, and one or more views.

```yaml
filters:
  and:
    - 'file.ext == "md"'

formulas:
  formula_name: 'expression'

properties:
  property_name:
    displayName: "Display Name"
  formula.formula_name:
    displayName: "Formula Display Name"
  file.ext:
    displayName: "Extension"

summaries:
  custom_summary_name: 'values.mean().round(3)'

views:
  - type: table
    name: "View Name"
    limit: 10
    groupBy:
      property: property_name
      direction: ASC
    filters:
      and:
        - 'status != "done"'
    order:
      - file.name
      - property_name
      - formula.formula_name
    summaries:
      property_name: Average
```

Inline Markdown form:

````markdown
```base
filters:
  and:
    - 'file.ext == "md"'
views:
  - type: table
    name: "View Name"
    order:
      - file.name
```
````

## Property Namespaces

- Note properties come from Markdown frontmatter and can be referenced as `note.author`, `note["author"]`, or bare `author`.
- File properties describe the evaluated file and use `file.*`, such as `file.name`, `file.path`, `file.ext`, `file.mtime`, and `file.tags`.
- Formula properties are defined under `formulas` and referenced elsewhere as `formula.name`.

Use `this.file.*` for context-dependent comparisons. In a main pane it refers to the base file; when embedded it refers to the embedding note or Canvas; in a sidebar it refers to the active file.
