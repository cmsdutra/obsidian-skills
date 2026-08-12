---
name: obsidian-theme-creator
description: Create, update, refactor, debug, or validate Obsidian app themes. Use when the user asks Codex to build a theme, edit theme.css, write or fix an Obsidian theme manifest.json, convert styling ideas or snippets into a full theme, support light/dark modes, prepare a theme for the Community Themes directory, or validate theme CSS against Obsidian theming guidelines.
---

# Obsidian Theme Creator

Use this skill to create and maintain Obsidian app themes, usually in `.obsidian/themes/<Theme Name>/` or a standalone theme repository.

## Workflow

1. Identify the target. Determine whether the user wants a local vault theme, an existing theme update, or a release-ready community theme.
2. Inspect the current files. Look for `.obsidian/themes`, `manifest.json`, `theme.css`, screenshots, README/license files, package tooling, and any preprocessors.
3. Clarify only risky unknowns. Ask for design direction, theme name, author, or release intent only when not inferable and material to the result.
4. Read `references/theme-patterns.md` before writing nontrivial CSS.
5. Consult `references/official-docs.md` when manifest fields, submission rules, asset handling, CSS variables, or current Obsidian guidance matter.
6. Implement the theme. Prefer CSS variables over fragile selectors, support both `.theme-light` and `.theme-dark` unless the user wants one mode, and keep selectors low-specificity.
7. Validate with:

   ```bash
   python3 .codex/skills/obsidian-theme-creator/scripts/validate_obsidian_theme.py <theme-dir>
   ```

   If this repository skill path is not available inside the target workspace, run the script from this skill folder directly.
8. If Obsidian runtime behavior matters, use the `obsidian-cli` skill to reload/check the UI, capture screenshots, inspect console errors, or evaluate DOM/CSS. Do not use Obsidian CLI to directly edit `.obsidian/` files.
9. Report changed files, validation results, and any manual Obsidian checks still needed.

## File Layout

For a local vault theme:

```text
<vault>/.obsidian/themes/<Theme Name>/
├── manifest.json
└── theme.css
```

For a release-ready repository, also expect:

```text
<theme-repo>/
├── manifest.json
├── theme.css
├── README.md
├── LICENSE
└── screenshot.png
```

## Manifest Rules

Use `manifest.json` for theme metadata. Required fields:

```json
{
  "name": "Theme Name",
  "version": "1.0.0",
  "minAppVersion": "1.5.0",
  "author": "Author Name"
}
```

Optional fields commonly include `authorUrl`, `fundingUrl`, and `modes`.

- Keep `name` human-facing; for local vault themes, the theme folder name must exactly match `manifest.json` `name`.
- Use semantic versions in `x.y.z` form.
- Include `modes` only when intentionally limiting support, for example `["dark"]`, `["light"]`, or `["light", "dark"]`.
- Restart Obsidian after changing `manifest.json`; CSS-only changes usually do not require a full restart.

## CSS Rules

- Define shared variables on `body`.
- Define mode-specific colors under `.theme-light` and `.theme-dark`.
- Use `:root` sparingly for values that truly need root scope.
- Prefer official Obsidian CSS variables before styling internal DOM classes.
- Avoid long descendant selectors, generated IDs, and plugin internals unless the user explicitly targets them.
- Avoid `!important`; if unavoidable, explain why in a nearby comment.
- Avoid `:has()` unless there is no practical alternative, especially for Canvas-heavy vaults.
- Do not load remote assets. Embed fonts/images as data URLs or keep release assets bundled according to Obsidian's current theme rules.
- Keep CSS readable: group by foundations, app chrome, navigation, editor, components, plugins, and print/mobile adjustments when relevant.

## Design Process

When creating a theme from a broad aesthetic request:

1. Translate the aesthetic into a concise design brief: mood, contrast, typography, accent behavior, density, and light/dark approach.
2. Start with foundations: background, foreground, accent, surfaces, borders, radii, typography, spacing.
3. Cover core Obsidian surfaces: workspace, ribbon, sidebars, tabs, file explorer, editor, reading view, links, headings, tables, code, callouts, modals, menus, search, graph, Canvas, and status bar when relevant.
4. Preserve usability. Check contrast, active states, focus outlines, readable code blocks, selection colors, and mobile-friendly touch targets.
5. Add custom selectors only after variables cannot express the requirement.

## Community Release Checklist

For a theme intended for the Community Themes directory:

- Ensure repository root includes `manifest.json`, `theme.css`, `README.md`, `LICENSE`, and a current screenshot.
- Keep the screenshot small; Obsidian documentation recommends 512 x 288 pixels.
- Confirm no remote network assets or calls.
- Confirm release assets include `manifest.json` and `theme.css`.
- Ensure the GitHub release tag exactly matches the version in `manifest.json`.
- Increment `manifest.json` `version` for each published fix.

## Bundled Resources

- `references/official-docs.md`: official Obsidian theming documentation map and source-grounded rules.
- `references/theme-patterns.md`: practical CSS architecture and variable patterns for Obsidian themes.
- `scripts/validate_obsidian_theme.py`: local validator for theme structure, manifest fields, CSS file presence, remote assets, and risky CSS patterns.
