# Post-Clone Setup Checklist

Complete the [Prerequisites](README.md#prerequisites) in [README.md](README.md) first, including cloning **[nx-datahub-shared-tools](https://github.com/100-m/nx-datahub-shared-tools)** so `mcp-datahub-server/` exists at the path you will reference in `.datahub-workspace.json`.

Then, after creating a new project from this template, complete these steps in order.

## 1. Create a repository from the template

Use GitHub **Use this template** (or your organization’s equivalent) and create the new repository on GitHub. See [README.md](README.md#creating-a-project-from-this-template-github).

## 2. Clone your repository locally

**CLI:** From your machine, clone the repo you created (replace the URL with yours):

```bash
git clone https://github.com/<owner>/<your-repo>.git
cd <your-repo>
```

**Cursor chat:** You can instead ask Cursor to clone the repository for you—for example, paste your GitHub repo URL and ask to clone it to a folder of your choice, or to clone and open the project.

If you already have a local copy from another workflow, open that folder instead.

## 3. Open in your editor

- **Cursor**: Open the cloned project folder. `.cursorrules` and `.cursor/skills/` load automatically (`.cursor/skills` is a symlink to `Skills/agent-skills/`).
- **VS Code / other**: Open the same folder. Read **[AGENTS.md](AGENTS.md)** and use **`Skills/agent-skills/`** for DataHub procedures (see also [.github/copilot-instructions.md](.github/copilot-instructions.md) if you use Copilot).

## 4. Create workspace configuration

```bash
cp .datahub-workspace.json.example .datahub-workspace.json
```

Edit `.datahub-workspace.json` and replace placeholders:

| JSON field | Placeholder | Description | Example |
|------------|-------------|-------------|---------|
| `workspace.projectName` | `YOUR_PROJECT_NAME` | **Project name** – used in specifications, MCP server key, and documentation | `MyProject` |
| `datahub.url` | `YOUR_DATAHUB_URL` | DataHub instance URL | `http://nxdh-docker-product` |
| `datahub.username` | `YOUR_USERNAME` | DataHub API username | `username` |
| `datahub.password` | `YOUR_PASSWORD` | DataHub API password | *(your password)* |
| `workspace.centralizedFolder` | `YOUR_PATH_TO_REPOS` | Absolute path to your repos folder | `/Users/you/Documents/Repositories/` |
| `workspace.mcpCentralizedFolder` | *(optional)* | Path to DH SharedTools from centralizedFolder | `DH SharedTools/DH-SharedTools` |
| `workspace.rootFolder` | `YOUR_PROJECT_FOLDER_NAME` | Path from centralizedFolder to this project folder | `MyProject/MyProject` |

Optional: `datahub.packageInstallEndpoint` and `datahub.getObjectPackageEndpoint` default to standard paths; override only if your DataHub deployment uses different endpoints.

The **project name** is the single source of truth for naming across the project. Specifications will use `{projectName}_SPEC_*.md`, and the DataHub MCP is registered as **`datahub-mcp-dev-{projectName}`** — use a **unique** `projectName` per machine if you use several projects.

## 5. Verify DH SharedTools path

Ensure the MCP DataHub server is available at:

```
{centralizedFolder}/{mcpCentralizedFolder}/mcp-datahub-server/
```

Example: `/Users/you/Documents/Repositories/DH SharedTools/DH-SharedTools/mcp-datahub-server/`

## 6. Register the project DataHub MCP

This template registers a **dedicated** DataHub MCP server per project (`datahub-mcp-dev-{projectName}`) in your MCP client config (default for Cursor: `~/.cursor/mcp.json`), using values from `.datahub-workspace.json`.

**Authoritative guidance** is the **`datahub-mcp-project-setup`** skill: [Skills/agent-skills/datahub-mcp-project-setup/SKILL.md](Skills/agent-skills/datahub-mcp-project-setup/SKILL.md) (workspace fields, `DATAHUB_*` env vars, merging `mcp.json`, reload behavior).

**Recommended (CLI):** From the project root:

```bash
python3 Scripts/configure_datahub_mcp_from_workspace.py --repo .
```

Options: `--dry-run` (print without writing), `--mcp-json ~/.cursor/mcp.json` (or another client’s JSON path), `--python /path/to/python3.11` — see the script’s help (also summarized in the skill).

Then **reload MCP** or **restart your editor** so the server starts.

**Optional (Cursor):** In Cursor chat, ask in plain language—for example **“Start MCP for this project”** or **“Configure the DataHub MCP from `.datahub-workspace.json`.”** The agent can apply the skill and run the script above when needed.

## 7. Test connectivity (optional)

- Use the **datahub-pack-installation** skill to install a pack from `Implementation/`
- Use the **datahub-object-retrieval** skill to fetch an object from DataHub

## Troubleshooting

- **MCP not found**: Check `centralizedFolder` and `mcpCentralizedFolder` paths
- **Authentication failed**: Verify `username` and `password` in `.datahub-workspace.json`
- **Package install fails**: Ensure DataHub URL is reachable and endpoints are correct
- **`.cursor/skills` missing or wrong after clone (Windows)**: The repo uses a **symlink** `.cursor/skills` → `Skills/agent-skills`. If Git checked out a text file instead of a link, enable symlink support (`git config core.symlinks true`) and re-checkout, or create the link manually (e.g. `mklink /J` junction on Windows). Skills are always available under **`Skills/agent-skills/`** regardless.
