---
name: obsidian-plugin-creator
description: Create, implement, modify, debug, or validate local Obsidian community plugins in a vault or plugin repository. Use when the user asks Codex to build an Obsidian plugin, scaffold plugin files, plan plugin behavior, inspect installed plugins for examples, follow Obsidian developer documentation, reload or debug a running plugin, or validate manifest/build compatibility for files such as manifest.json, main.ts, main.js, styles.css, package.json, or versions.json.
---

# Obsidian Plugin Creator

## Workflow

1. Clarify intent before coding. Identify the user's real workflow goal, target users, expected commands/views/settings/ribbon actions, persistence needs, mobile/desktop support, and whether the plugin is local-only or intended for community release.
2. Inspect context. Read the current repo layout, existing plugin files if present, and relevant installed plugin examples under `.obsidian/plugins` when examples would reduce uncertainty.
3. Consult official docs when API behavior, manifest fields, release requirements, settings APIs, or platform support matter. Start with `references/official-docs.md`, then open the linked official pages as needed.
4. Produce a concise development plan. Include plugin id/name, file structure, Obsidian API surfaces, data model/settings, build tooling, validation steps, and manual Obsidian checks.
5. Execute the plan. Prefer TypeScript source with a bundler that emits a root-level `main.js`; keep `main.ts` focused on lifecycle, command registration, and setup.
6. Validate with scripts. Run the plugin's own checks (`npm run build`, `npm run lint`, tests when present) and run `scripts/validate_obsidian_plugin.py <plugin-dir>`. Fix failures and rerun.
7. Validate in Obsidian when runtime behavior matters. Load `references/runtime-debugging.md` for reload, error, console, screenshot, DOM, CSS, and eval checks through Obsidian CLI.
8. Report outcome. State created/changed files, validation commands, runtime checks, and any manual Obsidian checks still required.

## Clarification

Ask only for information that cannot be safely inferred. If the user gives a broad request, clarify enough to avoid building the wrong plugin:

- Primary job: what should the plugin do inside Obsidian?
- Activation surface: command palette, ribbon icon, editor action, file menu, view, settings tab, background event, or status bar?
- Vault impact: should it read notes only, edit active files, create/move/delete notes, update metadata, or manage attachments?
- Persistence: does it need `loadData()`/`saveData()` settings or per-note data?
- Compatibility: desktop-only features, mobile support, minimum Obsidian version, or local-only expectations?

Proceed without further questions when intent is clear enough and the remaining choices are ordinary implementation details.

## Implementation Rules

- Use official Obsidian APIs from the `obsidian` package. Avoid undocumented internals unless the user explicitly accepts the maintenance risk.
- Set `manifest.json` carefully: `id`, `name`, `version`, `minAppVersion`, `description`, `author`, and `isDesktopOnly` are required for plugins. Keep `id` lowercase hyphen-case, matching the local folder name during development.
- Set `isDesktopOnly: true` when using Node.js, Electron, filesystem APIs outside Obsidian abstractions, or other desktop-only capabilities.
- Bundle runtime dependencies into `main.js`. Do not rely on unbundled `node_modules` at plugin runtime.
- Use `this.registerEvent(...)`, `this.registerDomEvent(...)`, intervals registered through the plugin API, and `addCommand(...)` so unload cleanup is reliable.
- Store user preferences with `loadData()` and `saveData()`. Add a settings tab when configuration is user-facing.
- Keep destructive vault operations explicit and reversible where practical. In this vault, use Obsidian CLI for operations that risk broken links or need Obsidian to update backlinks automatically.
- Keep release artifacts at plugin root: `manifest.json`, `main.js`, and optional `styles.css`. Source may live in `src/`.

## Planning Template

Use this shape when presenting the plan:

```markdown
Plugin plan
- Intent:
- Plugin id/name:
- User surfaces:
- Files:
- Data/settings:
- Obsidian APIs:
- Desktop/mobile:
- Validation:
- Manual Obsidian check:
```

## Bundled Resources

- `references/official-docs.md`: official Obsidian documentation map and stable rules to check before implementation.
- `references/runtime-debugging.md`: Obsidian CLI workflow for reloading plugins, capturing errors, inspecting console output, screenshots, DOM/CSS, mobile emulation, and app-context eval.
- `scripts/validate_obsidian_plugin.py`: local validator for plugin project structure, manifest fields, id rules, build metadata, and expected release artifacts.
