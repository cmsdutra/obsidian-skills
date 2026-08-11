---
name: obsidian-snippet-creator
description: Generate clean, commented Obsidian CSS snippets from user requirements and save them as .css files under .obsidian/snippets in the current vault. Use when the user asks to create, adjust, or install Obsidian CSS snippets, customize Obsidian appearance with CSS variables, or save snippet files for Obsidian's Appearance CSS snippets setting.
---

# Obsidian Snippet Creator

Use this skill to create CSS snippets for an Obsidian vault and save them in `.obsidian/snippets`.

## Source

Use the official Obsidian CSS variables reference as the primary source for variable names and categories:

https://docs.obsidian.md/Reference/CSS+variables/CSS+variables

That page is an index grouped by Foundations, Components, Editor, Plugins, Window, and Obsidian Publish. When a request targets a specific UI area, consult the matching official subpage if current variable names matter.

## Workflow

1. Identify the vault root. Prefer the current working directory when it contains `.obsidian/`.
2. Translate the user's visual requirement into a small snippet. Prefer Obsidian CSS variables over fragile deep selectors when an official variable exists.
3. Read `references/snippet-patterns.md` before writing the snippet unless the change is trivial.
4. Write didactic CSS: a short header comment, grouped sections, comments that explain intent, and conservative selectors.
5. Save with `scripts/save_snippet.py`:

   ```bash
   python3 .codex/skills/obsidian-snippet-creator/scripts/save_snippet.py --vault . --name "snippet-name" < /tmp/snippet.css
   ```

6. Validate:
   - Confirm the file exists in `.obsidian/snippets/<name>.css`.
   - Check braces and parentheses are balanced.
   - If Obsidian is running and visual verification is useful, use the `obsidian-cli` skill to reload/check the UI. Do not use Obsidian CLI to edit `.obsidian/` files.

## CSS Rules

- Scope variables on `body`, `.theme-light`, or `.theme-dark` when customizing global appearance.
- Use `var(--existing-variable)` for fallbacks instead of hard-coded duplicate values.
- Avoid `!important` unless Obsidian or plugin CSS cannot be overridden otherwise; add a comment explaining why.
- Avoid selectors tied to generated IDs, long DOM chains, or plugin internals unless the user explicitly targets that plugin and no variable exists.
- Keep snippets reversible: one concern per file unless the user asks for a combined snippet.

## Naming

Use short kebab-case names, for example `compact-editor`, `callout-colors`, or `daily-note-focus`.

If the user gives a broad theme request, create a descriptive single file. If they ask for unrelated changes, split into multiple snippets and tell them the filenames.
