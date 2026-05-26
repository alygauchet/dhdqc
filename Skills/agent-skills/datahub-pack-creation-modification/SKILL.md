---
name: datahub-pack-creation-modification
description: Builds and modifies DataHub pack files (lists, workflows, event patterns, etc.). Use when creating or editing .pack files, list modifications, workflow packages, package dependencies, or when referencing Knowledge/Model/Templates/ for examples.
---

# DataHub Pack Creation & Modification

## Quick Start

1. **Check templates first**: Always check `Knowledge/Model/Templates/` (or `Implementation/Templates/` in shared projects) for example packages before creating new ones (e.g., `LIST_MODIFICATION_EXAMPLE.pack`, `WORKFLOW_MODIFICATION_EXAMPLE.pack`)
2. **Reference shared rules**: See `{workspace.centralizedFolder}/{workspace.mcpCentralizedFolder}/mcp-datahub-server/.cursorrules` (rules file shipped with **mcp-datahub-server** in SharedTools — filename is upstream convention, not specific to this template) for additional package creation guidelines
3. **Workspace constraint**: Verify event pattern parameters are from WORKFLOW main table only

## Pack File Standards

- **Encoding**: UTF-8
- **Structure**: Preserve XML structure and formatting when editing
- **CDATA**: Be careful with CDATA sections and special characters
- **Testing**: Test pack imports in DataHub after modifications

### Package Code Matching (CRITICAL)

- The `<PACKAGE>` tag MUST always match the filename (without `.pack` extension)
- Example: `WF_RUN_Q_CLASS_2.pack` → `<PACKAGE>WF_RUN_Q_CLASS_2</PACKAGE>`
- Rule: `<PACKAGE>CODE</PACKAGE>` = filename without `.pack`

## Creating and Modifying Pack Files

- Always validate XML structure before saving
- Test imports in DataHub after changes
- Preserve existing field order and structure
- **Never modify packages used as reference** — generate new packages and put them in `Implementation/`
- **Check dependencies**: Split into multiple packages if objects have dependencies (see below)

## Package Dependencies and Import Order

**CRITICAL**: If objects have dependencies (OBJ1 refers to OBJ2), generate separate packages with numbered suffixes:

| Suffix | Content | Example |
|--------|---------|---------|
| `_0` | Objects with no dependencies | Event Patterns |
| `_1` | Objects depending on package 0 | Workflow Templates referencing Event Patterns |
| `_N` | Objects depending on previous packages | Further dependent objects |

**Import order**: Package 0 → Package 1 → Package N. Always document import order in README files.

## Modifying Lists (SMARTLIST) — Adding Items

**CRITICAL** when adding items to an existing list:

1. Use `PARTIAL='1'` attribute on the `<SMARTLIST>` tag
2. When using `PARTIAL='1'`, do NOT include the `<R_SMARTLIST>` section — keep `<T_SMARTLIST>` empty
3. Without `PARTIAL='1'`, DataHub treats it as a full list update and validates all list fields, causing errors

### Adding Items with Custom Display Names (Two-Package Process)

When adding a new list item that needs a custom display name (different from INTERNAL_CODE), use **two separate packages** in this order:

1. **Package 1 — Item only**: Add `R_SMARTLIST_ITEM` in `T_SMARTLIST_ITEM`. Leave `T_SMARTLIST_ITEM_LABEL` empty. Install this package first.
2. **Package 2 — Label only**: Add `R_SMARTLIST_ITEM_LABEL` in `T_SMARTLIST_ITEM_LABEL`. Leave `T_SMARTLIST_ITEM` empty. Install after the item exists.

**Why two packages?** If you include both item and label in the same package, DataHub fails with: *"A reference to SMARTLIST_ITEM of the class MxList is unknown"* — the label references the item before it exists in the database.

For the full XML structure and workflow, see [reference.md](reference.md).

## Package Reinstallation

**CRITICAL**: You cannot install the same package twice. To reinstall:

1. Rename the package file by adding/incrementing an index suffix (e.g., `PACKAGE_NAME.pack` → `PACKAGE_NAME_1.pack`)
2. **MUST UPDATE**: Change the `<PACKAGE>` code inside the XML to match the new filename exactly (without `.pack` extension)
3. Both filename AND internal `<PACKAGE>` XML tag must match exactly

## XML/Pack File Standards

- Preserve XML structure and formatting when editing
- Maintain proper encoding (UTF-8)
- Target package size: < 1MB; maximum: 5MB — split if exceeding limits

## Naming Conventions

| Type | Format | Example |
|------|--------|---------|
| Package | `{ObjectType}_{ObjectCode}.pack` | `MxWorkflow_PriceValidation.pack` |
| With dependencies | `{ObjectType}_{ObjectCode}_{N}.pack` | `WF_RUN_Q_CLASS_0.pack`, `WF_RUN_Q_CLASS_1.pack` |

## File Locations

| Folder | Purpose |
|--------|---------|
| `Knowledge/Model/Templates/` | Project-local example and template packages |
| `Implementation/Templates/` | Shared templates (when using DH SharedTools / centralized folder). When both exist, prefer shared templates for consistency |
| `Implementation/` | Pack files ready for import |
| `Implementation/Installed/` | Archive for successfully installed packages |
| `Knowledge/Model/Objects/` | Object packages retrieved via getObjectPackage (format: `{ClassName}_{ObjectCode}.pack`) |

## Validation Checklist

Before considering a package complete:

- [ ] Package structure is valid XML
- [ ] `<PACKAGE>` tag matches filename
- [ ] All dependencies are included or available
- [ ] References are correct
- [ ] For list modifications: `PARTIAL='1'` used when adding items
- [ ] For list items with custom display names: item and label in separate packages; item installed first
- [ ] Import order documented if multiple dependent packages

## Additional Resources

For detailed examples (pack structure, list modification XML), see [reference.md](reference.md).
