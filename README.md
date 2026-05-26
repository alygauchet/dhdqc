# DH Project Template

A Git repository template for NeoXam DataHub projects. Use this template to kickstart feature development with specifications, implementations, models, and documentation—optimized for use with Cursor or another MCP-capable editor and DataHub MCP tools.

## Prerequisites

- **DataHub**: Access to a NeoXam DataHub instance
- **Editor**: Cursor or another IDE with MCP support (see [AGENTS.md](AGENTS.md) for tool-neutral guidance)
- **DH SharedTools (shared tools)**: Clone **[nx-datahub-shared-tools](https://github.com/100-m/nx-datahub-shared-tools)** locally before you configure this project. It holds the **reference knowledge base** and **MCP servers** (including the DataHub MCP under `mcp-datahub-server/`). Place the clone so that `workspace.centralizedFolder` and `workspace.mcpCentralizedFolder` in `.datahub-workspace.json` resolve to it (default example: `DH SharedTools/DH-SharedTools` — see `.datahub-workspace.json.example` and [SETUP.md](SETUP.md)).

## Creating a project from this template (GitHub)

1. Open this **DH Project Template** repository on GitHub.
2. Click **Use this template**, then **Create a new repository**.
3. Set the owner, repository name, description, and visibility (public or private), then click **Create repository**. GitHub creates a new repository with the template files; it is your project—develop and push there as usual.
4. **Clone your new repository** to your machine (`git clone` using the URL from GitHub **Code**).
5. **Open the cloned folder** in your editor (e.g. Cursor or VS Code).

If you cannot use the template button (for example on a fork or mirror), clone this template repository and push it to an empty repository you own, or duplicate the repo using your organization’s usual process.

## Quick Start

Meet the [Prerequisites](#prerequisites) first (including cloning [nx-datahub-shared-tools](https://github.com/100-m/nx-datahub-shared-tools)).

1. **Create your repo** – Use [Creating a project from this template (GitHub)](#creating-a-project-from-this-template-github) above (or use an existing project created from the template).
2. **Open the project** – Open the folder in your editor. See [AGENTS.md](AGENTS.md) for where skills live. **Cursor** loads `.cursorrules` and `.cursor/skills/` automatically (`.cursor/skills` points at `Skills/agent-skills/`).
3. **Configure workspace** – Copy `.datahub-workspace.json.example` to `.datahub-workspace.json` and fill in your values (see [SETUP.md](SETUP.md)).
4. **Register the project DataHub MCP** – Prefer the CLI in [SETUP.md](SETUP.md), or in **Cursor** chat ask for example: **“Start MCP for this project”** or **“Configure DataHub MCP from my workspace.”** The **`datahub-mcp-project-setup`** skill and `Scripts/configure_datahub_mcp_from_workspace.py` apply. Then reload MCP or restart the editor when prompted. See [Skills/agent-skills/datahub-mcp-project-setup/SKILL.md](Skills/agent-skills/datahub-mcp-project-setup/SKILL.md).
5. **Start developing** – Write specs in `Specification/`, create pack files in `Implementation/`, and use the skills under `Skills/agent-skills/` for guidance

## Project Structure

| Folder | Purpose |
|--------|---------|
| `Skills/agent-skills/` | Tool-neutral agent skills (`SKILL.md` per topic); symlinked as `.cursor/skills/` for Cursor |
| `Specification/` | Functional specifications and user stories (`{projectName}_SPEC_*.md`) |
| `Implementation/` | Pack files (.pack) ready for import into DataHub |
| `Implementation/Installed/` | Archive for successfully installed packages |
| `Implementation/Temp/` | Temporary storage for getObjectPackage; clean after moving to Knowledge/Model/Objects |
| `Knowledge/Model/` | Data model definitions, class structures (MxClassDef, MxList definitions), schemas |
| `Knowledge/Model/Objects/` | Retrieved object packages from getObjectPackage — instance data (`{ClassName}_{ObjectCode}.pack`) |
| `Knowledge/Model/Templates/` | Example and template packages for reference |
| `Knowledge/Reference/` | Reference documents, presentations, examples |
| `Scripts/` | Python, PowerShell, and automation scripts |
| `User Documentation/` | End-user guides |
| `Images/` | Diagrams and screenshots |

## Agent skills

Domain-specific guidance lives in **`Skills/agent-skills/`** (also linked as `.cursor/skills/`). See **[AGENTS.md](AGENTS.md)** for a portable index. Each skill is a folder with `SKILL.md`; some include `reference.md` or `README.md` for extra context. In Cursor, skills apply automatically when relevant; you can also reference them explicitly:

| Skill | Use when | Example |
|-------|----------|---------|
| `datahub-pack-creation-modification` | Creating or editing pack files, lists, workflows | "Create a list modification pack for X" |
| `datahub-specification-writing` | Writing specs in Specification/ | "Write a spec for feature Y" |
| `datahub-business-rules` | SmartRule logic, status management, validation | "Write a business rule that validates Z" |
| `datahub-pack-installation` | Installing packages via MCP | "Install the pack from Implementation/" |
| `datahub-object-retrieval` | Fetching objects from DataHub | "Get object MxList_WF_STATUS from DataHub" |
| `datahub-object-search` | Querying DataHub via REST search API, listing objects | "Search for controls with code X" |
| `datahub-data-model` | Understanding data model (MxClassDef, MxList) | "How is the MxList structure defined?" |
| `datahub-testing-validation` | Testing packs, validating IMPACT, smoke tests | "Validate this IMPACT code" or "Test the pack after install" |
| `datahub-mcp-project-setup` | Registering DataHub MCP from `.datahub-workspace.json`, `mcp.json` merge | "Start MCP for this project" or "Configure DataHub MCP from my workspace" |

For pack file standards and creation guidelines, see the **datahub-pack-creation-modification** skill. For SmartRule patterns and spec structure, see **datahub-business-rules** and **datahub-specification-writing**.

## Technology Stack

- **DataHub**: NeoXam DataHub platform with XML-based pack files (.pack)
- **Python**: Scripts for automation and pack file manipulation
- **PowerShell**: Windows automation scripts (for Windows users)
- **Business Rules**: DataHub SmartRule language (IMPACT)
- **Mermaid**: For embedding schemas in specifications

## Configuration

All configuration is read from `.datahub-workspace.json` (not committed; use `.datahub-workspace.json.example` as reference):

- **Project Name**: `{workspace.projectName}` – used for specification naming (`{projectName}_SPEC_*.md`), the MCP server key **`datahub-mcp-dev-{projectName}`**, and elsewhere
- **MCP Server Path**: `{workspace.centralizedFolder}/{workspace.mcpCentralizedFolder}/mcp-datahub-server/`
- **DataHub URL**: `{datahub.url}`
- **Authentication**: `{datahub.username}`, `{datahub.password}` for DataHub API
- **Project Root**: `{workspace.rootFolder}` – path from centralizedFolder to this project (used by MCP)

After editing `.datahub-workspace.json`, run the CLI from [SETUP.md](SETUP.md) or ask your assistant (e.g. **“Sync DataHub MCP with my workspace”**) so your MCP config (e.g. `~/.cursor/mcp.json` for Cursor) matches your credentials and URLs.

