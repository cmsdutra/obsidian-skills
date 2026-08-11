# Troubleshooting

Load this when `obsidian` fails to run, cannot connect to the app, or command syntax appears stale.

## First Checks

```bash
command -v obsidian
obsidian version
obsidian help
```

If help works, prefer `obsidian help <command>` as the current command reference. If help fails, use the official CLI documentation as the fallback: <https://obsidian.md/help/cli>.

Official setup requirements include:

- Obsidian must be running for CLI commands to connect to the app.
- Obsidian CLI requires a recent Obsidian 1.12 installer.
- The CLI must be enabled in Obsidian settings under General.
- On Linux, `~/.local/bin` should be on `PATH` and the CLI binary is commonly registered at `~/.local/bin/obsidian`.

## `unable to find Obsidian`

If a command returns:

```text
The CLI is unable to find Obsidian. Please make sure Obsidian is running and try again.
```

Check:

1. Obsidian is open.
2. The correct vault is open or targetable with `vault=<name>`.
3. CLI is enabled in Obsidian settings.
4. The socket path is available for the installation method.

## Flatpak Socket Workaround

Known Linux Flatpak issue: the Obsidian CLI socket may exist under the Flatpak runtime path instead of `$XDG_RUNTIME_DIR/.obsidian-cli.sock`.

When Obsidian is running and `obsidian` still reports `unable to find Obsidian`, check:

```bash
ls -l /run/user/1000/.flatpak/md.obsidian.Obsidian/xdg-run/.obsidian-cli.sock
ls -l /run/user/1000/.obsidian-cli.sock
```

If the Flatpak socket exists and the standard socket path is missing or points to a missing target, recreate the symlink:

```bash
ln -s /run/user/1000/.flatpak/md.obsidian.Obsidian/xdg-run/.obsidian-cli.sock /run/user/1000/.obsidian-cli.sock
```

This symlink is in tmpfs and may need to be recreated after rebooting or restarting Obsidian.

## Linux PATH or Binary Issues

```bash
echo "$PATH"
ls -l ~/.local/bin/obsidian
```

If the binary is missing, re-enable CLI registration in Obsidian settings. For manual repair, follow the official Linux instructions for copying the bundled `obsidian-cli` binary to `~/.local/bin/obsidian` and making it executable.

## When Documentation Seems Stale

1. Try `obsidian help <command>`.
2. Check <https://obsidian.md/help/cli>.
3. If local behavior differs from docs, trust local `obsidian help` for this machine and mention the version or setup uncertainty.
