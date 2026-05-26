# Agent guidance (DataHub project template)

This repository holds NeoXam DataHub specifications, pack files, and domain rules. **Canonical skill content** lives under [`Skills/agent-skills/`](Skills/agent-skills/). Cursor also loads the same tree via [`.cursor/skills`](.cursor/skills) (symlink).

## When to read what

| Resource | Purpose |
|----------|---------|
| [`Skills/agent-skills/`](Skills/agent-skills/) | Per-topic `SKILL.md` files (packs, specs, SmartRules, MCP, etc.) |
| [`.cursorrules`](.cursorrules) | Project rules when using **Cursor** (auto-loaded); includes skill index and folder permissions |
| [`.datahub-workspace.json`](.datahub-workspace.json.example) | DataHub URL, credentials, `projectName`, paths to SharedTools / MCP |

## MCP setup

Register the project DataHub MCP from `.datahub-workspace.json` using [`Skills/agent-skills/datahub-mcp-project-setup/SKILL.md`](Skills/agent-skills/datahub-mcp-project-setup/SKILL.md) and, from the repo root, `Scripts/configure_datahub_mcp_from_workspace.py` (see [SETUP.md](SETUP.md)).

## Skills (index)

| Skill folder | Use when |
|--------------|----------|
| `datahub-pack-creation-modification` | Creating or editing pack files, lists, workflows |
| `datahub-specification-writing` | Writing specs in `Specification/` |
| `datahub-business-rules` | SmartRule logic, status management |
| `datahub-pack-installation` | Installing packages via MCP |
| `datahub-object-retrieval` | Fetching objects via getObjectPackage |
| `datahub-object-search` | REST search API, listing objects |
| `datahub-data-model` | MxClassDef, MxList structure |
| `datahub-testing-validation` | IMPACT validation, smoke tests after install |
| `datahub-mcp-project-setup` | Sync DataHub MCP with `.datahub-workspace.json` |

For related combinations: pack creation often needs the data-model skill; object retrieval informs new packs; business rules may use the br-knowledge MCP where configured.
