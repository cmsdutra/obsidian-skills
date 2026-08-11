# Obsidian Skills for Codex

Agent Skills for use with Obsidian, packaged as a Codex plugin.

This repository is Caio Dutra's fork of [`kepano/obsidian-skills`](https://github.com/kepano/obsidian-skills.git). The upstream project provides Obsidian-focused Agent Skills for multiple skills-compatible agents; this fork adapts that work for local Codex plugin usage.

These skills follow the [Agent Skills specification](https://agentskills.io/specification) so they can be used by any skills-compatible agent, including Claude Code, Codex, and Open Code.

## Installation

### Codex Plugin

This fork includes a Codex plugin manifest at `.codex-plugin/plugin.json` and exposes the skills in `skills/`.

### Original Marketplace

```
/plugin marketplace add kepano/obsidian-skills
/plugin install obsidian@obsidian-skills
```

These commands refer to the original upstream marketplace package.

### npx skills

```
npx skills add git@github.com:cmsdutra/obsidian-skills.git
```

Instead of ssh, if you prefer to use https:

```
npx skills add https://github.com/cmsdutra/obsidian-skills
```

### Manually

#### Claude Code

Add the contents of this repo to a `/.claude` folder in the root of your Obsidian vault (or whichever folder you're using with Claude Code). See more in the [official Claude Skills documentation](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview).

#### Codex

Copy the `skills/` directory into your Codex skills path (typically `~/.codex/skills`). See the [Agent Skills specification](https://agentskills.io/specification) for the standard skill format.

#### OpenCode

Clone this fork into the OpenCode skills directory (`~/.opencode/skills/`):

```sh
git clone https://github.com/cmsdutra/obsidian-skills.git ~/.opencode/skills/obsidian-skills
```

Do not copy only the inner `skills/` folder — clone the full repo so the directory structure is `~/.opencode/skills/obsidian-skills/skills/<skill-name>/SKILL.md`.

OpenCode auto-discovers all `SKILL.md` files under `~/.opencode/skills/`. No changes to `opencode.json` or any config file are needed. Skills become available after restarting OpenCode.

## Skills

| Skill | Description |
|-------|-------------|
| [obsidian-markdown](skills/obsidian-markdown) | Create and edit [Obsidian Flavored Markdown](https://help.obsidian.md/obsidian-flavored-markdown) (`.md`) with wikilinks, embeds, callouts, properties, and other Obsidian-specific syntax |
| [obsidian-bases](skills/obsidian-bases) | Create and edit [Obsidian Bases](https://help.obsidian.md/bases/syntax) (`.base`) with views, filters, formulas, and summaries |
| [json-canvas](skills/json-canvas) | Create and edit [JSON Canvas](https://jsoncanvas.org/) files (`.canvas`) with nodes, edges, groups, and connections |
| [obsidian-cli](skills/obsidian-cli) | Interact with Obsidian vaults via the [Obsidian CLI](https://help.obsidian.md/cli) including plugin and theme development |
| [defuddle](skills/defuddle) | Extract clean markdown from web pages using [Defuddle](https://github.com/kepano/defuddle), removing clutter to save tokens |
