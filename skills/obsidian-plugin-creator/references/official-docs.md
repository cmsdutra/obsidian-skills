# Official Obsidian Plugin References

Use official documentation first when behavior or compatibility matters:

- Developer home: https://docs.obsidian.md/Home
- Plugin docs source tree: https://github.com/obsidianmd/obsidian-developer-docs/tree/main/en/Plugins
- Manifest reference: https://docs.obsidian.md/Reference/Manifest
- Plugin API reference: https://docs.obsidian.md/Reference/TypeScript%2BAPI/Plugin
- Settings guide: https://docs.obsidian.md/plugins/guides/migrate-declarative-settings
- Plugin guidelines: https://docs.obsidian.md/Plugins/Releasing/Plugin%2Bguidelines
- Official sample plugin: https://github.com/obsidianmd/obsidian-sample-plugin

Current stable points to preserve:

- Obsidian plugins extend the app using TypeScript and compile to JavaScript loaded by Obsidian.
- `manifest.json` requires `id`, `name`, `version`, `minAppVersion`, `description`, `author`, and `isDesktopOnly`; common optional fields include `authorUrl` and `fundingUrl`.
- `id` must use lowercase letters and hyphens, must not contain `obsidian`, and must not end with `plugin`. For local development, the folder name should match `id`.
- `version` should use SemVer format `x.y.z`.
- Desktop-only APIs require `isDesktopOnly: true`; mobile-compatible plugins should avoid Node.js and Electron APIs.
- Release/install artifacts are `manifest.json`, `main.js`, and optional `styles.css` at the plugin root.
- Newer settings APIs can require newer `minAppVersion`; verify the relevant docs before choosing `minAppVersion`.
