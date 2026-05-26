---
name: datahub-pack-installation
description: >-
  Installs DataHub `.pack` files via MCP `install_datahub_package` or workspace
  `install_package.py`, install order (rule → list → operands → control), duplicate
  partial-list handling, and post-install URLs. Use when installing packages or
  importing packs.
---

# DataHub Pack Installation

## MCP Tools Used

- **install_datahub_package** on the **DataHub MCP** server configured for this project (see **datahub-mcp-project-setup** — server key `datahub-mcp-dev-{projectName}`). The IDE or agent exposes MCP tools with a prefixed name that includes that server key.

## Installation Workflow

1. Use the **install DataHub package** MCP tool from the project’s DataHub server for package installation
2. After successful installation, packages are automatically moved to `Implementation/Installed/` folder
3. Always display DataHub URLs after installation using format: `{datahub.url}/datahub/#/[ClassName]/[ObjectID]`

## Configuration

Read from `.datahub-workspace.json`:

- **DataHub URL**: `{datahub.url}` (used for displaying object URLs after installation)
- **Authentication**: Username `{datahub.username}`, Password `{datahub.password}`

## File Locations

| Folder | Purpose |
|--------|---------|
| `Implementation/` | Pack files ready for import |
| `Implementation/Installed/` | Archive for successfully installed packages (auto-moved after install) |

## Workspace install script (recommended)

From the repo root (with `.datahub-workspace.json`):

```bash
python3 "{workspace.centralizedFolder}/{workspace.mcpCentralizedFolder}/mcp-datahub-server/scripts/install_package.py" "Implementation/Installed/YourPackage.pack"
```

Credentials and **`DATAHUB_ENDPOINT_INSTALL`** resolve from **`.datahub-workspace.json`** and env overrides. Inspect JSON **`PackageResult.Result`** (**`Status`**, **`Comment`**) for success vs merge errors.

## Install order (typical DQC / controls)

1. **`MxRule`** (rule code referenced from **`DATACONTROL_TYPE`** Free1).
2. **`DATACONTROL_TYPE`** partial **only when adding a new list item**; skip if the item already exists (install may fail with **duplicate `INTERNAL_CODE`**).
3. **`MxControlClauseData`** operand bundle(s).
4. **`MxDataControl`**.

After install, **`getObjectPackage`** confirms **object ids** for URLs and correct **clause / name** rows.

### Same package twice (re-deploy / operand hotfix)

The Hub **migration API** often **does not re-apply** content when you import a `.pack` whose **`PACKAGE`** code (and workflow release) was **already imported**: **`Status`** can still show **OK** while fields such as **`MxControlClauseData.DATA_VALUE`** stay unchanged.

**Mitigation:**

1. Bump **`PACKAGE`** inside the `.pack` header **and** the filename together (suffix **`_1`**, **`_2`**, …), per shared **`mcp-datahub-server/.cursorrules`** (“Package Reinstallation”).
2. Ship minimal delta packs when possible (operand-only fixes), e.g. **`YC_DQC_VAR_THRESH_DATAVALUE_FIX_1`** / **`…_FIX_2`** (plain **`DATA_VALUE`** **`10`** for tenor thresholds; bump suffix each apply).

Operand updates that merge by **`LOCAL_ID`** should use ids from **`getObjectPackage`** on the **same** Hub you are targeting.

## Reference

Package creation, modification, and installation rules are maintained centrally. See `{workspace.centralizedFolder}/{workspace.mcpCentralizedFolder}/mcp-datahub-server/.cursorrules` for:
- Package dependencies and import order
- Package code matching and reinstallation

See **`datahub-dqc-datacontrol`** for **operand uniqueness**, **`MxDataControl`** clause **CODEFIELDS**, **display names**, and **numeric `DATA_VALUE`** quirks.
