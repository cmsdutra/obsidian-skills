# Examples

Use these as starting points, then adapt property names to the user's vault.

Official source for embedding: https://obsidian.md/help/bases/create-base

## Task Table

```yaml
filters:
  and:
    - file.hasTag("task")
    - 'file.ext == "md"'

formulas:
  days_until_due: 'if(due, (date(due) - today()).days, "")'
  is_overdue: 'if(due, date(due) < today() && status != "done", false)'
  priority_label: 'if(priority == 1, "High", if(priority == 2, "Medium", "Low"))'

properties:
  formula.days_until_due:
    displayName: "Days Until Due"
  formula.priority_label:
    displayName: "Priority"

views:
  - type: table
    name: "Active Tasks"
    filters:
      and:
        - 'status != "done"'
    order:
      - file.name
      - status
      - formula.priority_label
      - due
      - formula.days_until_due
    groupBy:
      property: status
      direction: ASC
    summaries:
      formula.days_until_due: Average
```

## Reading Cards And Table

```yaml
filters:
  or:
    - file.hasTag("book")
    - file.hasTag("article")

formulas:
  reading_time: 'if(pages, (pages * 2).toString() + " min", "")'
  status_icon: 'if(status == "reading", "Reading", if(status == "done", "Done", "Queued"))'
  year_read: 'if(finished_date, date(finished_date).year, "")'

properties:
  formula.status_icon:
    displayName: "Status"
  formula.reading_time:
    displayName: "Est. Time"

views:
  - type: cards
    name: "Library"
    order:
      - cover
      - file.name
      - author
      - formula.status_icon
    filters:
      not:
        - 'status == "dropped"'

  - type: table
    name: "To Read"
    filters:
      and:
        - 'status == "to-read"'
    order:
      - file.name
      - author
      - pages
      - formula.reading_time
```

## Daily Notes With Date Formula

```yaml
filters:
  and:
    - file.inFolder("Daily Notes")
    - '/^\d{4}-\d{2}-\d{2}/.matches(file.name)'

formulas:
  word_estimate: '(file.size / 5).round(0)'
  day_of_week: 'date(file.name.replace(".md", "")).format("dddd")'

properties:
  formula.day_of_week:
    displayName: "Day"
  formula.word_estimate:
    displayName: "~Words"

views:
  - type: table
    name: "Recent Notes"
    limit: 30
    order:
      - file.name
      - formula.day_of_week
      - formula.word_estimate
      - file.mtime
```

## Custom Link Text From File Name

Use `file.asLink(display?)` when a table should keep Obsidian link behavior but show a shorter or derived label instead of the full file name. Combine it with `file.basename.replace(...)` when the display text should be extracted from the file name.

This pattern is useful for notes whose names include a process number, date, code, or other prefix plus a longer description.

```yaml
formulas:
  process_link: 'file.asLink(file.basename.replace(/^.*?(\d{7}-\d{2}\.\d{4}).*$/, "$1"))'

properties:
  formula.process_link:
    displayName: "Process"

views:
  - type: table
    name: "Cases"
    order:
      - formula.process_link
      - status
      - due
    columnSize:
      formula.process_link: 138
```

When adapting this pattern:

- Replace the regular expression with the portion of the file name that should be displayed.
- Keep the formula expression quoted as a YAML string, especially because it contains quotes and regex punctuation.
- If replacing `file.name` in an existing view, update related display configuration such as `properties`, `order`, `summaries`, and `columnSize` to use `formula.<name>`.
- If the regex does not match, `replace()` leaves the basename unchanged, so the table still shows a usable link label.

## Embedding

```markdown
![[MyBase.base]]
![[MyBase.base#View Name]]
```

## Inline Base Code Block

Use a `base` fence, not a `yaml` fence, when the Base should render inline in a Markdown note.

````markdown
```base
filters:
  and:
    - file.hasTag("example")
views:
  - type: table
    name: Table
    order:
      - file.name
```
````
