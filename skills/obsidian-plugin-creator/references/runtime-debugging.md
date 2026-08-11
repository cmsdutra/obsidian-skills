# Runtime Debugging

Use this reference when a plugin must be validated inside a running Obsidian app. These checks complement build/lint/tests and the local validator; they do not replace source-level review.

## Prerequisites

- Obsidian must be open with the target vault loaded.
- The Obsidian CLI must be enabled and reachable as `obsidian`.
- The plugin id should match the development folder and `manifest.json` id.

Check the active vault and CLI before runtime validation:

```bash
obsidian version
obsidian vault
obsidian plugin id=my-plugin
```

## Reload and Error Loop

After code or style changes:

```bash
obsidian plugin:reload id=my-plugin
obsidian dev:errors
```

If errors appear, fix them, rebuild if needed, reload again, then re-check:

```bash
obsidian plugin:reload id=my-plugin
obsidian dev:errors
```

Clear captured errors only after recording the useful output:

```bash
obsidian dev:errors clear
```

## Console Capture

Console capture requires the debugger to be attached:

```bash
obsidian dev:debug on
obsidian dev:console level=error limit=50
obsidian dev:console level=warn limit=50
```

Clear buffers only after recording relevant messages:

```bash
obsidian dev:console clear
```

Detach the debugger when finished so the app is not left in debug capture mode:

```bash
obsidian dev:debug off
```

## Visual and DOM Checks

Use screenshots for layout or rendering checks:

```bash
obsidian dev:screenshot path=screenshot.png
```

Use DOM and CSS inspection for targeted assertions:

```bash
obsidian dev:dom selector=".workspace-leaf" text
obsidian dev:dom selector=".modal" all
obsidian dev:css selector=".workspace-leaf" prop=background-color
```

Prefer selectors owned by the plugin when possible, such as a plugin-specific class or view type container.

## App-Context Eval

Run JavaScript in the Obsidian app context for targeted runtime checks:

```bash
obsidian eval code="app.plugins.enabledPlugins.has('my-plugin')"
obsidian eval code="app.vault.getFiles().length"
```

Keep eval snippets read-only unless the user explicitly requested a mutation and the operation has been reviewed for vault safety.

## Commands and Hotkeys

Inspect command IDs registered by the app and plugins:

```bash
obsidian commands filter="my-plugin"
obsidian hotkeys verbose
```

Execute a command only when it is safe for the vault state:

```bash
obsidian command id="my-plugin:my-command"
```

## Plugins, Themes, and Snippets

Inspect plugin state:

```bash
obsidian plugins filter=community versions
obsidian plugins:enabled filter=community versions
obsidian plugin id=my-plugin
```

Use enable/disable/install/uninstall/restricted-mode commands only when the user clearly requested that state change.

## Mobile and CDP

Use mobile emulation when mobile support is part of the requirement:

```bash
obsidian dev:mobile on
obsidian dev:mobile off
```

Use Chrome DevTools Protocol commands only when ordinary CLI, DOM, CSS, console, or eval checks are insufficient:

```bash
obsidian dev:cdp method="Runtime.evaluate" params='{"expression":"document.title"}'
```
