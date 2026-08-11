# Formulas

Official sources:

- https://obsidian.md/help/formulas
- https://obsidian.md/help/bases/functions
- https://obsidian.md/help/bases/syntax

Formulas define computed properties under the top-level `formulas` key. They are stored as YAML strings and referenced elsewhere as `formula.name`.

```yaml
formulas:
  days_until_due: 'if(due, (date(due) - today()).days, "")'
  label: 'if(status == "done", "Done", "Open")'
  updated: 'file.mtime.format("YYYY-MM-DD")'
```

## Property Access

- Bare names such as `status` refer to note properties.
- `note.status` and `note["status"]` also refer to note properties.
- `file.ext`, `file.path`, `file.mtime`, and related names refer to file metadata.
- `formula.other_formula` references another formula. Avoid circular formula references.

## Dates And Durations

Use `date()` to parse date-like properties, `today()` for the current date at midnight, and `now()` for the current date and time.

```yaml
formulas:
  due_day: 'if(due, date(due).format("YYYY-MM-DD"), "")'
  modified_recently: 'file.mtime > now() - "1 week"'
  days_until_due: 'if(due, (date(due) - today()).days, "")'
```

Duration arithmetic is a common source of drift between examples and Obsidian versions. This vault has a working base at `400_Biblioteca/Bases/Work.todo.base` using `(today() - note["submitted"]).days + 1`, while current official syntax describes date subtraction as a millisecond difference. Preserve tested `.days` formulas unless they fail in Obsidian; if creating a new base and `.days` fails, test a numeric conversion such as `((date(due) - today()) / 86400000).round(0)`.

## Null Guards

Properties may be absent on many notes. Guard formulas that parse, format, or do arithmetic on optional values.

```yaml
formulas:
  finished_year: 'if(finished, date(finished).year, "")'
  estimate: 'if(pages, (pages * 2).toString() + " min", "")'
```
