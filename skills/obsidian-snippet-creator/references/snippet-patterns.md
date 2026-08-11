# Snippet Patterns

Use these patterns when generating Obsidian CSS snippets. Keep the final CSS tailored to the user's request; do not copy every section by default.

## Variable-first snippet

```css
/*
  Snippet: readable-headings
  Purpose: Adjust note headings using Obsidian CSS variables.
  Enable in Obsidian: Settings -> Appearance -> CSS snippets.
*/

body {
  /* H1: stronger page anchors without changing every text element. */
  --h1-size: 1.8em;
  --h1-weight: 700;

  /* H2: keep hierarchy visible while staying close to the theme. */
  --h2-size: 1.45em;
  --h2-weight: 650;
}
```

## Light and dark variants

```css
/*
  Snippet: subtle-workspace-colors
  Purpose: Tune workspace surfaces separately for light and dark themes.
*/

.theme-light {
  --background-primary: #fafafa;
  --background-secondary: #f0f2f4;
}

.theme-dark {
  --background-primary: #151719;
  --background-secondary: #202327;
}
```

## Component selector with variable fallback

```css
/*
  Snippet: calmer-tags
  Purpose: Make tags quieter while preserving the active theme's accent color.
*/

.tag {
  color: var(--text-accent);
  background-color: color-mix(in srgb, var(--text-accent) 12%, transparent);
  border-radius: var(--radius-s);
  padding: 0.1em 0.45em;
}
```

## Didactic comment style

- Start with a short block comment containing the snippet name, purpose, and where to enable it.
- Comment groups of related declarations, not every line.
- Explain non-obvious selectors, fallbacks, or `!important`.
- Keep comments useful for a vault owner who may edit the snippet later.

## Safety checklist

- Prefer official CSS variables from the Obsidian documentation.
- Use readable formatting: one selector block per concern.
- Keep selectors short and stable.
- Do not hide core navigation or controls unless the user explicitly asked.
- Do not fetch remote fonts or images unless the user explicitly asked and understands the dependency.
