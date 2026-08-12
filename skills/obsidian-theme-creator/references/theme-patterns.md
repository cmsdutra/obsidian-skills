# Obsidian Theme Patterns

Use these patterns when creating or updating `theme.css`.

## Recommended Structure

```css
/*
Theme Name
Design intent: concise description.
*/

/* Foundations */
body {
  --font-text-theme: Inter, var(--font-interface);
  --radius-s: 4px;
  --radius-m: 6px;
}

.theme-light {
  color-scheme: light;
  --background-primary: #fafafa;
  --background-secondary: #f0f2f4;
  --text-normal: #20242a;
  --text-muted: #5c6670;
  --interactive-accent: #2f6fdd;
}

.theme-dark {
  color-scheme: dark;
  --background-primary: #151719;
  --background-secondary: #1d2024;
  --text-normal: #e8eaed;
  --text-muted: #a0a7b0;
  --interactive-accent: #82aaff;
}
```

## Variable-First Targets

Prefer changing variables for:

- Colors: backgrounds, text, accents, borders, highlights.
- Typography: editor fonts, headings, code fonts, font sizes, line heights.
- Editor: headings, inline title, links, tags, tables, code blocks, embeds, callouts.
- Window chrome: ribbon, workspace, tabs, status bar, scrollbars, dividers.
- Components: buttons, toggles, sliders, text inputs, modals, popovers, menus.
- Core plugins: file explorer, search, graph, Canvas.

Inspect Obsidian's `app.css` and the official CSS variables docs when the right variable is not obvious.

## Selector Rules

Use selectors when a variable cannot express the requirement:

```css
.workspace-tab-header.is-active {
  box-shadow: inset 0 -2px 0 var(--interactive-accent);
}
```

Keep them shallow. Avoid selectors like:

```css
.workspace .mod-root .workspace-tabs .workspace-leaf .view-content div:nth-child(2) {
  /* Too fragile */
}
```

## Style Settings Plugin

When the user asks for configurable theme options and the Style Settings plugin is acceptable, add an `/* @settings ... */` YAML block at the top of `theme.css`. Keep configurable values as custom properties on `body`, `.theme-light`, or `.theme-dark`, then reuse those properties throughout the theme.

## Accessibility Checks

- Preserve visible focus states.
- Keep text, link, and code contrast readable in both modes.
- Check selection and search highlight colors against foreground text.
- Do not rely on accent color alone for active/error states.
- Keep editor line height and paragraph spacing comfortable without altering fragile Live Preview vertical margins.

## Release-Oriented CSS

- Keep generated or preprocessed source outside `theme.css` unless the user asks for source setup.
- If using Sass/Less/PostCSS, make `theme.css` the committed output expected by Obsidian.
- Avoid network URLs in `url()` or `@import`.
- Add comments for non-obvious compatibility workarounds, not for every variable assignment.
