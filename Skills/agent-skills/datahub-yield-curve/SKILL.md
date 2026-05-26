---
name: datahub-yield-curve
description: >-
  Explains NeoXam DataHub yield curve valuation artefacts: MxYieldCurveValu
  (YIELDCURVEVALU), pillar semantics (MATURITY, MATURITY_PROVIDER, mid/bid/ask),
  list YIELD_CURVE_MATURITY_TYPE, YC_* MxBusinessField patterns, REC_SPEC on
  tenor-specific fields, and business class YC_CURVE_VALUATION. Use when
  modelling curves, mids by tenor, DQC on curve pillars, or when the user
  mentions yield curve, MxYieldCurveValu, YC_MID, or curve valuation rows.
---

# DataHub — Yield curves and valuation pillars

## Core technical class

- **`MxYieldCurveValu`**: valuation **rows** (“pillars”) for a curve on a valuation date (main physical table **`YIELDCURVEVALU`** in typical installs).
- **Header / keys** commonly include **`YIELDCURVE`** (curve object), **`CALCULATION_DATE`**, **`MATURITY`**, **`MATURITY_PROVIDER`**.
- Market data fields include **`MATURITY_VALUE_MID`**, **`MATURITY_VALUE_BID`**, **`MATURITY_VALUE_ASK`**, zero-coupon / discount-factor columns, variation, status-related columns, etc. (exact set from **`MxClassDef`** export for **`MxYieldCurveValu`**).

Use **`get_object_package`** with `class_name`: `MxClassDef`, `object_code`: **`MxYieldCurveValu`** for the authoritative field list.

## Tenor list

Pillar tenor is usually the **`MATURITY`** list item for list **`YIELD_CURVE_MATURITY_TYPE`** (name may vary slightly by release). **`INTERNAL_CODE`** examples:

| Meaning (typical FREE metadata) | `INTERNAL_CODE` |
|-------------------------------|-----------------|
| 1 calendar day | `1` |
| 1 week | `7` |
| 1 month | `1M` |
| … | `2M`, `3M`, `6M`, `9M`, `1Y`, … |

**Not** every mnemonic is a valid code (e.g. `1W` may be absent; **`7`** often means **1 week**).

## `MxBusinessField` patterns (`YC_*`)

Environment-specific **`MxBusinessField`** rows expose curve concepts to UI / DQC, e.g.:

- **`YC_CURVE`** — curve reference (**`TECH_FIELD`** / equivalent: yield curve pointer).
- **`YC_DATE`** — valuation date (**`CALCULATION_DATE`**).
- **`YC_LABEL`** — descriptive label (**`YIELDCURVE_LABEL`** or equivalent technical binding).
- **`YC_STATUS`** — status on the pillar row (`STATUS`-like technical binding).
- **`YC_MID_1D`**, **`YC_MID_1W`**, **`YC_MID_1M`**, … **`YC_MID_1Y`** — **`MATURITY_VALUE_MID`** with **`REC_SPEC`** filtering **`MATURITY_PROVIDER`** (often **`REFERENCE`**) and **`MATURITY`** = list **`INTERNAL_CODE`** for that tenor (`S"7"` for 1W, **`S"1M"`**, etc.; **`S"1"`** for 1D).

Export each field with **`get_object_package`** (`MxBusinessField`, object code **`YC_*`**) when reverse-engineering **`REC_SPEC`**.

### Discovering coverage

On a given Hub:

1. **`MxBusinessField`** search **`CODE`** `LIKE` **`YC_%`** (or narrower `YC_MID%`) for quick coverage.
2. Loop **`TECH_FIELD`** `EQUAL` each technical pillar field name only if reliable; some labels differ from internal **`FIELD_NAME`** (e.g. status).

## Business class for valuation scope

Example: **`MxBusinessClass`** **`YC_CURVE_VALUATION`** with **`TECH_CLASS`** **`[CLASS_NAME='MxYieldCurveValu']`**, **`T_BUSINESSCLASS_FIELD`** listing all desired **`YC_*`** `MxBusinessField` refs — used as **`BUSINESS_CLASS`** **`[CODE='YC_CURVE_VALUATION']`** in DQC / clause data where appropriate.

Adding fields after manual class creation: use **append-only** `T_BUSINESSCLASS_FIELD` pack (see **`datahub-business-class`** skill).

## Related skills

- `datahub-business-class` — **`MxBusinessClass`** packs (append-only **`BUSINESSCLASS_FIELD`**).
- `datahub-pack-creation-modification` — pack structure and reinstall naming.
- `datahub-object-retrieval` / `datahub-object-search` — export and shallow queries.
- `datahub-data-model` — **`MxClassDef`** / **`MxList`** fundamentals.
- `datahub-dqc-datacontrol` — **`BUSINESS_FIELD`** + **`BUSINESS_CLASS`** on controls.
