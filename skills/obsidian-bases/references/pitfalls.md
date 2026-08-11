# Pitfalls

## YAML Quoting

Quote YAML strings that contain special characters such as `:`, `{`, `}`, `[`, `]`, `,`, `&`, `*`, `#`, `?`, `|`, `-`, `<`, `>`, `=`, `!`, `%`, `@`, or backticks.

```yaml
# Wrong
displayName: Status: Active

# Right
displayName: "Status: Active"
```

## Formula Expressions With Quotes

Formula expressions are YAML strings. When the formula contains text literals in double quotes, wrap the whole formula in single quotes.

```yaml
# Wrong
formulas:
  label: "if(done, "Yes", "No")"

# Right
formulas:
  label: 'if(done, "Yes", "No")'
```

If a formula itself needs single quotes, either invert the outer quoting or escape carefully. Validate YAML after editing.

## `formula.*` References

Only use `formula.name` after defining `name` under top-level `formulas`.

```yaml
formulas:
  total: 'price * quantity'

views:
  - type: table
    name: "Prices"
    order:
      - file.name
      - formula.total
```

`properties` display configuration does not create a formula. It only configures how an existing property is shown.

## Note Properties Versus `file.*`

Frontmatter properties are note properties. Use `status`, `note.status`, or `note["status"]`, not `file.status`.

Use `file.*` only for file metadata such as `file.name`, `file.path`, `file.folder`, `file.ext`, `file.size`, `file.ctime`, `file.mtime`, `file.tags`, `file.links`, `file.backlinks`, `file.embeds`, and `file.properties`.

## Date Difference And Duration Operations

Date and duration behavior is a common source of mistakes and version drift. Check https://obsidian.md/help/bases/syntax and https://obsidian.md/help/bases/functions when an expression fails.

Practical guardrails:

- Use duration strings for date offsets: `now() - "1 week"` or `today() + "7d"`.
- Use `duration("1d")` when doing arithmetic with duration values.
- Do not treat `.days` as invalid by default. This vault has a working base at `400_Biblioteca/Bases/Work.todo.base` with `(today() - note["submitted"]).days + 1`.
- Current official syntax describes subtracting dates as returning a millisecond difference. Treat that as a documentation/runtime ambiguity, not as a reason to rewrite working `.days` formulas.
- When creating a new base, prefer the tested vault pattern `if(due, (date(due) - today()).days, "")`; if it fails in Obsidian, test the millisecond conversion `((date(due) - today()) / 86400000).round(0)`.
- Do not call number functions such as `.round()` on an unverified date-difference or duration value; first confirm whether the runtime exposes fields such as `.days` or returns a number.
