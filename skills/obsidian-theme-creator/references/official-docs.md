# Official Obsidian Theme Docs

Use official Obsidian sources as the primary reference when details may have changed:

- Build a theme: https://docs.obsidian.md/Themes/App+themes/Build+a+theme
- Theme guidelines: https://docs.obsidian.md/Themes/App+themes/Theme+guidelines
- Embed fonts and images: https://docs.obsidian.md/Themes/App+themes/Embed+fonts+and+images+in+your+theme
- Submit your theme: https://docs.obsidian.md/Themes/App+themes/Submit+your+theme
- CSS variables index: https://docs.obsidian.md/Reference/CSS+variables/CSS+variables
- Obsidian October theme checklist: https://docs.obsidian.md/oo/theme
- Stylelint config for Obsidian themes: https://github.com/obsidianmd/stylelint-config
- Sample theme: https://github.com/obsidianmd/obsidian-sample-theme

## Stable Rules To Apply

- Themes are CSS-based and are discovered from the vault's `.obsidian/themes` directory.
- A theme normally has `manifest.json` and `theme.css`.
- For local vault themes, the theme directory name must match `manifest.json` `name`.
- Define shared styling on `body`; define mode-specific colors under `.theme-light` and `.theme-dark`.
- Prefer CSS variables over selectors. Obsidian exposes variables across foundations, components, editor, plugins, and window chrome.
- Keep selectors low-specificity because Obsidian app class names and nesting can change.
- Do not load remote fonts or images for community themes. Bundle resources and use data URLs where assets are required.
- Avoid `!important` because users should be able to override themes with snippets.
- Avoid `:has()` unless necessary because it can harm performance, especially in Canvas.
- Community releases require matching `manifest.json` and GitHub release tag versions in `x.y.z` form; release assets must include `manifest.json` and `theme.css`.

## When To Browse

Browse official docs before relying on:

- Newly added CSS variable names.
- Current manifest fields or submission requirements.
- Community directory review rules.
- Asset, privacy, or network-call policies.
- Any Obsidian behavior that may differ by app version.
