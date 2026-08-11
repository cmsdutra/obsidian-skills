# Filters

Official source: https://obsidian.md/help/bases/syntax

Filters narrow the vault-wide dataset. There is no SQL-style `from` or Dataview-style source section. Global filters apply to every view; view filters are combined with the global filters using `AND`.

```yaml
filters:
  and:
    - 'file.ext == "md"'
    - file.hasTag("project")
```

## Shapes

```yaml
# Single statement
filters: 'status == "active"'

# All statements must match
filters:
  and:
    - 'status == "active"'
    - 'priority >= 3'

# Any statement may match
filters:
  or:
    - file.hasTag("book")
    - file.hasTag("article")

# Exclude matches
filters:
  not:
    - file.hasTag("archive")

# Nested filter object
filters:
  or:
    - file.hasTag("tag")
    - and:
        - file.hasTag("book")
        - file.hasLink("Textbook")
    - not:
        - file.inFolder("Required Reading")
```

## Operators

| Operator | Meaning |
| --- | --- |
| `==` | equals |
| `!=` | not equal |
| `>` | greater than |
| `<` | less than |
| `>=` | greater than or equal |
| `<=` | less than or equal |
| `&&` | logical and inside an expression |
| `\|\|` | logical or inside an expression |
| `!` | logical not |

Prefer filter objects for multi-condition logic because they are easier to quote and maintain in YAML.
