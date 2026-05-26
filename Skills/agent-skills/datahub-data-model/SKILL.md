---
name: datahub-data-model
description: Explains how DH data models are defined with MxClassDef and MxList. Use when understanding data model structure, class definitions, list definitions, schema documentation, or when referencing Knowledge/Model/Objects/ for class metadata.
---

# DataHub Data Model

## Overview

DataHub data models are defined by two core structures: **MxClassDef** (class/table definitions) and **MxList** (list definitions). Both are stored as SMARTCLASS records in MxClassDef and exported as pack files.

## MxClassDef — Class Definitions

**Purpose**: Defines tables, fields, and metadata for all DataHub classes (MxSecurity, MxAgent, MxList, etc.).

**Java class**: `lib.system.dictionnary.MxClassDef`

**Pack structure**: Root tag `<SMARTCLASS>` with `FIND="CLASS_NAME='ClassName'"`

**Key sections** (from `Knowledge/Model/Objects/MxClassDef_MxClassDef.pack`):

| Section | Purpose |
|---------|---------|
| `T_SMARTCLASS` / `R_SMARTCLASS` | Class metadata: `CLASS_NAME`, `CLASS_FULL_NAME`, `TABLE_NAME`, `BASIC_SAVE_ACTION`, `BASIC_DELETE_ACTION`, `CACHE_MODE`, `IS_SYSTEM_CLASS` |
| `T_SMARTCLASS_FIELD` / `R_SMARTCLASS_FIELD` | Field definitions: `FIELD_NAME`, `FIELD_TABLE_NAME`, `FIELD_TYPE`, `REF_LIST`, `REF_TABLE` |
| `T_SMARTCLASS_TABLE` | Table structure (main and linked tables) |
| `T_SMARTCLASS_CACHE` | Cache configuration |

**Important field attributes**:
- `FIELD_TYPE`: Data type (1=INT, 3=STRING, 5=TEXT, etc.)
- `REF_LIST`: `[LIST_CODE='LIST_NAME']` — references an MxList
- `REF_TABLE`: References another table (e.g., `SMARTLIST_ITEM`)
- `FIELD_TABLE_NAME`: Table containing the field (e.g., `SMARTCLASS_FIELD`, `SMARTCLASS_TABLE`)

## MxList — List Definitions

**Purpose**: Defines reference lists (statuses, types, currencies) with items and labels.

**Java class**: `lib.system.MxList`

**Pack structure**: Root tag `<SMARTCLASS>` with `FIND="CLASS_NAME='MxList'"`

**Key tables** (from `Knowledge/Model/Objects/MxClassDef_MxList.pack`):

| Table | Purpose |
|-------|---------|
| `SMARTLIST` | List header: `LIST_CODE`, main list metadata |
| `SMARTLIST_ITEM` | List items: `INTERNAL_CODE`, item properties |
| `SMARTLIST_ITEM_LABEL` | Item labels by language: `IL_ITEM_ID`, `IL_LANGUAGE` |
| `SMARTLIST_CATEGORY` | Categories for hierarchical lists |
| `SMARTLIST_NAME` | List names by language |
| `SMARTLIST_HISTO` | History/versioning |

**Pack XML for list instances**: Root tag `<SMARTLIST>` (see `datahub-pack-creation-modification` for list modification patterns).

## Retrieving Class Definitions

To fetch MxClassDef or MxList definitions via getObjectPackage:

| Object | class_name | object_code |
|--------|------------|-------------|
| MxClassDef definition | `MxClassDef` | `MxClassDef` |
| MxList definition | `MxClassDef` | `MxList` |

Request shapes (SOAP XML and JSON `ObjectPackage.Package[]`) are documented in **datahub-object-retrieval**.

**Example** (standalone script):
```bash
python3 get_object_package.py MxClassDef MxClassDef
python3 get_object_package.py MxClassDef MxList
```

## Reference Files

| File | Content |
|------|---------|
| `Knowledge/Model/Objects/MxClassDef_MxClassDef.pack` | Full MxClassDef class definition (~11K lines) |
| `Knowledge/Model/Objects/MxClassDef_MxList.pack` | Full MxList class definition (~4.4K lines) |

## Relations

- **MxClassDef** defines all classes, including **MxList**
- **MxClassDef** fields can reference **MxList** via `REF_LIST`
- **MxClassDef** fields can reference other tables via `REF_TABLE`
- List instances (e.g., WF_STATUS) are retrieved with `class_name="SMARTLIST"` or `"MxList"`, `object_code="WF_STATUS"`

## Additional Resources

- **Data Dictionary concepts**: See [reference.md](reference.md) for main concepts extracted from the NeoXam Data Dictionary Customization Guide (object representation, table types, field types, constraints, historicization).
- **Full guide**: `NeoXam DataHub - Data Dictionary Customization Guide.pdf` in this skill folder.

## Related Skills

- `datahub-object-retrieval` — Fetching objects from DataHub
- `datahub-pack-creation-modification` — Creating/modifying SMARTLIST packs
