---
name: datahub-business-class
description: >-
  Explains NeoXam DataHub MxBusinessClass modelling (TECH_CLASS, TECH_CONDITION,
  T_BUSINESSCLASS_FIELD links to MxBusinessField), pack patterns for merges vs
  append-only field updates, Packages/install pitfalls, and how BUSINESS_CLASS
  scopes DQC / clause data. Use when creating or extending business classes,
  adding BUSINESSCLASS_FIELD rows, or when the user mentions MxBusinessClass,
  business class, BUSINESS_CLASS, TECH_CONDITION, or Curve Valuation scopes.
  Inheritance: SEC_EQUITY vs SEC_CASH_INSTRUMENT and finding inherited QUOTE_* fields for DQC.
---

# DataHub — Business class (`MxBusinessClass`)

## What it is

A **business class** is a named **view** over a **technical SmartClass** (`TECH_CLASS`). It groups **`MxBusinessField`** definitions for UI, search, and runtime resolution (e.g. DQC **`BUSINESS_CLASS`** on `MxControlClauseData`).

Key ideas:

- **`CODE`**: stable internal identifier (e.g. `YC_CURVE_VALUATION`).
- **`TECH_CLASS`**: reference to the backing class, e.g. `[CLASS_NAME='MxYieldCurveValu']`.
- **`TECH_CONDITION`**: optional embedded **condition** (stringpack + `RF CLASS="Condition"` in full exports) narrowing which **technical** rows match the business class. May be empty while the class is still usable for field binding.
- **`T_BUSINESSCLASS_FIELD`**: rows linking **`BUSINESS_FIELD`** → each value is a composite ref like `[TECH_CLASS^CODE='[CLASS_NAME='MxYieldCurveValu']^YC_CURVE']`.
- **`T_BUSINESSCLASS_LABEL`**: per-language labels (`LANGUAGE` `0`/`1`, etc.).

## Authoritative workflow

1. **Export** the class after UI or server changes: **`get_object_package`** — `class_name`: `MxBusinessClass`, `object_code`: `<CODE>` (e.g. `YC_CURVE_VALUATION`).
2. **Inspect** `TECH_CLASS`, `TECH_CONDITION`, and every `R_BUSINESSCLASS_FIELD` / `BUSINESS_FIELD` ref.
3. **Search** which `MxBusinessField` rows exist for a technical class: filter by `CODE` prefix (e.g. `YC_%`) or **`TECH_FIELD`** / resolved technical field on `MxBusinessField` (environment-specific).
4. **Edit** packs following `datahub-pack-creation-modification` (HEAD/BODY, `<PACKAGE>` = filename without `.pack` for project convention).

## Adding fields to an existing business class (pack pattern)

**Do not** resend the full `T_BUSINESSCLASS_FIELD` including rows that already exist with the same **`BUSINESS_FIELD`** ref: the installer treats that as a **duplicate** (`Record value … already exists … BUSINESSCLASS_FIELD`).

**Append-only pack** (validated on this project):

- **`<HEAD>`**: new filename-aligned `<PACKAGE>` / `<NAME>` (e.g. `MxBusinessClass_YC_CURVE_VALUATION_add_fields_2`) so reinstall rules are satisfied.
- **`<BODY>`**: one `<BUSINESSCLASS FIND="CODE='<CLASS_CODE>'" LABEL='…'>` **without** repeating `T_BUSINESSCLASS` / `R_BUSINESSCLASS`, containing only:

```xml
<T_BUSINESSCLASS_FIELD CODEFIELDS="BUSINESS_FIELD" >
  <!-- New R_BUSINESSCLASS_FIELD rows only; omit LOCAL_ID for inserts -->
</T_BUSINESSCLASS_FIELD>
```

- Close `</BUSINESSCLASS>` → `</RESULT>` → `</BODY>`.

After install, re-export **`MxBusinessClass`** to refresh `Knowledge/Model/Objects/` reference packs.

### Full merge (when appropriate)

Replacing **all** links in one shot requires a consistent snapshot (all `R_BUSINESSCLASS_FIELD` rows, correct `LOCAL_ID`s if updating in place). If the installer errors on duplicates, prefer **append-only** packages or strip conflicting rows.

## Packages/install caveat (new vs update)

Creating a **brand new** business class with a **new** **`TECH_CONDITION`** embedded condition via `Packages/install` may fail with **Exception `226`** (*missing technical definition of a stringpack*) on some setups. **Manual** Data Dictionary creation (or migration tooling used by your team) may be required once; afterward, **append-only field** packs normally work.

## DQC linkage

Clause operands and controls often carry **`BUSINESS_CLASS`** refs such as **`[CODE='YC_CURVE_VALUATION']`**. That scope must agree with **`BUSINESS_FIELD`** refs that point at `MxBusinessField` rows whose **`TECH_CLASS`** matches the controlled object's technical projection.

## Inherited fields (Equity vs Cash Instrument)

Child business classes **inherit** links from **`SUPER_CLASS`**. Example: **`SEC_EQUITY`** extends **`SEC_CASH_INSTRUMENT`** (both map to **`MxSecurity`** with different **`TECH_CONDITION`**). Exports of the **child** may emphasize class-specific **`T_BUSINESSCLASS_FIELD`** rows (e.g. analytics) while **shared market data** such as **`QUOTE_LAST`**, **`QUOTE_MID`**, **`QUOTE_BID`**, … appears on the **parent** export. When choosing **DQC `BUSINESS_FIELD`** points for “equity price”, **export `SEC_CASH_INSTRUMENT`** (or grep parent + child) to enumerate **`QUOTE_*`** candidates, then **`get_object_package(MxBusinessField, …)`** to confirm **`REC_SPEC`** / **`PROVIDER`** for **`REFERENCE`**.

## Related skills

- `datahub-pack-creation-modification` — pack naming, reinstall suffixes.
- `datahub-pack-installation` — MCP `install_datahub_package`, `Implementation/Installed/`.
- `datahub-object-retrieval` — **`get_object_package`**.
- `datahub-object-search` — quick listing / smoke checks (`MxBusinessField`, etc.).
- `datahub-yield-curve` — **`MxYieldCurveValu`** and **`YC_*`** fields.
- `datahub-dqc-datacontrol` — **`BUSINESS_CLASS`** on **`MxControlClauseData`** / **`MxDataControl`**.
