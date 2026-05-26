---
name: datahub-mcp-project-setup
description: >-
  Configures the project DataHub MCP (mcp-datahub-server) from .datahub-workspace.json:
  resolves paths via workspace.centralizedFolder and workspace.mcpCentralizedFolder,
  sets DATAHUB_* env vars from datahub.*, registers the server as
  datahub-mcp-dev-{projectName}. Use when the user asks to start or configure the
  project DataHub MCP, sync MCP with the workspace, or add the package installer MCP
  from shared tools.
---

# DataHub MCP project setup

## When to use

Apply this skill when the user wants to **configure**, **register**, **sync**, or **start** the **DataHub MCP** for the current DH project using **`.datahub-workspace.json`**, including naming the server **`datahub-mcp-dev-{projectName}`**.

**Typical user prompts** (template projects tell users to ask this way): *“Start MCP for this project”*, *“Configure DataHub MCP from my workspace”*, *“Sync MCP with `.datahub-workspace.json`.”*

## Universal configuration

These apply regardless of IDE: they describe the workspace file, server process, and env vars the MCP entry must carry.

### Configuration source

Read **`{projectRoot}/.datahub-workspace.json`** (not committed if it contains secrets; use `.datahub-workspace.json.example` if the file is missing and tell the user to copy it).

| Workspace field | Use |
|-----------------|-----|
| `workspace.centralizedFolder` | Absolute base path to repositories |
| `workspace.mcpCentralizedFolder` | Relative path from that base to the shared-tools repo (contains `mcp-datahub-server/`) |
| `workspace.projectName` | **Server name suffix** — MCP key: `datahub-mcp-dev-{projectName}` |
| `datahub.url` | Base URL (no trailing slash required) |
| `datahub.packageInstallEndpoint` | Path segment for install (e.g. `/smartservicegate/services/Packages/install`) |
| `datahub.getObjectPackageEndpoint` | Path segment for getObjectPackage |
| `datahub.username`, `datahub.password` | `DATAHUB_USERNAME`, `DATAHUB_PASSWORD` |

### Paths

- **MCP root**: `{centralizedFolder}` + `{mcpCentralizedFolder}` (normalize with `pathlib` or equivalent; handle trailing slashes).
- **Server script**: `{MCP root}/mcp-datahub-server/mcp_datahub_server.py`
- **`cwd`**: `{MCP root}/mcp-datahub-server` (so `config/datahub_config.json` resolves if present).

### Environment variables for the server

Set on the MCP server entry (they override `config/datahub_config.json` inside `mcp-datahub-server`):

| Variable | Value |
|----------|--------|
| `DATAHUB_ENDPOINT_INSTALL` | `{datahub.url}` (trim trailing `/`) + `packageInstallEndpoint` |
| `DATAHUB_ENDPOINT_GET_OBJECT` | `{datahub.url}` + `getObjectPackageEndpoint` |
| `DATAHUB_USERNAME` | `datahub.username` |
| `DATAHUB_PASSWORD` | `datahub.password` (use string `""` if empty) |

Optional: `DATAHUB_RELEASE_CODE` — only if the user or team requires a non-default release code (otherwise omit to use server defaults).

### Uniqueness note

`datahub-mcp-dev-{projectName}` is chosen for clarity; `projectName` must stay **unique per project** on the same machine if multiple MCP entries are registered.

## IDE adapters

### Cursor

- **File**: `~/.cursor/mcp.json` (user-level; not in the DH project repo).
- **Merge**: preserve every other `mcpServers` entry. Add or replace only `datahub-mcp-dev-{projectName}`.
- **Python `command`**: prefer the same interpreter as other MCPs in the file (e.g. `python3.11` on Homebrew macOS); else `python3` / `PYTHON_FOR_MCP` if set.
- **Reload**: user must **reload MCP** or **restart Cursor** after writing.

### Claude Code (VSCode extension)

- **File**: `{projectRoot}/.mcp.json` (project-level; loaded automatically by Claude Code when opening this folder).
- **`settings.json` does NOT support `mcpServers`** — always use `.mcp.json`.
- **Merge**: same pattern — preserve other entries, add/replace `datahub-mcp-dev-{projectName}`.
- **Secrets**: `.mcp.json` may be committed to git. If `DATAHUB_PASSWORD` is non-empty, add `.mcp.json` to `.gitignore` before committing.
- **Reload**: user must **start a new Claude Code session** (restart the extension or reopen the folder) for the server to appear.
- **Tool names**: Claude Code exposes MCP tools prefixed with the server key, e.g. `mcp__datahub-mcp-dev-{projectName}__<tool>`.

## Automation (run for the user)

Always run the script — do not hand-edit `mcp.json` files.

**Cursor** (writes to `~/.cursor/mcp.json`):
```bash
python3 Scripts/configure_datahub_mcp_from_workspace.py --repo .
```

**Claude Code / VSCode** (writes to `{repo}/.mcp.json`):
```bash
python3 Scripts/configure_datahub_mcp_from_workspace.py --repo . --claude-code
```

Run **both** if the user works in both IDEs.

Additional options:
- `--workspace /path/to/.datahub-workspace.json` — if not under `--repo`
- `--mcp-json /custom/path/mcp.json` — override output path for any other MCP client
- `--python /path/to/python3.11` — pin interpreter
- `--dry-run` — print server key and JSON without writing

## After configuration

| IDE | What to do after running the script |
|-----|--------------------------------------|
| Cursor | Reload MCP or restart Cursor |
| Claude Code (VSCode) | Start a new Claude Code session (restart extension / reopen folder) |

- If two projects use the **same** `projectName`, MCP keys **collide** — advise using a unique `workspace.projectName` per repository.
- If `.mcp.json` is present and Claude Code still doesn’t show the server, check that the session was fully restarted (not just a new chat).
