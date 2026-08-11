# Summaries

Official source: https://obsidian.md/help/bases/syntax

There are two summary locations:

- Top-level `summaries` defines custom summary formulas.
- A view's `summaries` maps displayed properties to built-in or custom summary names.

```yaml
summaries:
  roundedAverage: 'values.mean().round(2)'

views:
  - type: table
    name: "Invoices"
    order:
      - file.name
      - amount
    summaries:
      amount: roundedAverage
```

In custom summaries, `values` is the list of values for that property across the current result set.

## Built-In Summaries

| Name | Input Type | Description |
| --- | --- | --- |
| `Average` | Number | Mathematical mean |
| `Min` | Number | Smallest number |
| `Max` | Number | Largest number |
| `Sum` | Number | Sum of all numbers |
| `Range` | Number | Max minus min |
| `Median` | Number | Mathematical median |
| `Stddev` | Number | Standard deviation |
| `Earliest` | Date | Earliest date |
| `Latest` | Date | Latest date |
| `Range` | Date | Latest minus earliest |
| `Checked` | Boolean | Count of true values |
| `Unchecked` | Boolean | Count of false values |
| `Empty` | Any | Count of empty values |
| `Filled` | Any | Count of non-empty values |
| `Unique` | Any | Count of unique values |
