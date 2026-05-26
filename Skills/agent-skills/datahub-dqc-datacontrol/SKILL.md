---
name: datahub-dqc-datacontrol
description: >-
  Models NeoXam DataHub DQC data controls (MxDataControl): comparison clauses,
  MxControlClauseData operands, DATACONTROL_TYPE semantics (including rule-based
  types), MxBusinessField as data point, pack/install conventions (partial lists,
  DATACONTROL XML refs, IMPACT pitfalls), and a repeatable workflow to trace or
  author behaviour. Defect-oriented clause authoring (this workspace): unary NULL
  (Is Null) for anomaly on missing assessed VALUE_OF fields; GREATER (>) assessed
  vs numeric target for anomalies above a cap—plus traditional NOTNULL /
  LOWER_OR_EQUAL tolerance style. Use when designing, explaining, reverse-engineering, or
  packaging controls; when the user mentions DQC, MxDataControl,
  MxControlClauseData, DATACONTROL_TYPE, STRING_REGEX, DQC_CHANGE, rule-based
  clause types, NULL, NOTNULL, GREATER, LOWER_OR_EQUAL, numeric thresholds, operand reuse, MxDataControl merge keys,
  DATA_VALUE fixed literals, CONTROLCLAUSEDATA Value field, control/operand display names; Series Jump, Stale, execution rules, Data Quality Screening Report, MxControlExecResult,
  quality level / quality indicator, golden copy, Business Dictionary inheritance, or DQC system parameters. YC curve
  valuation naming: ASCII CV - titles; unary clause LABEL '{Field} Is Null'; tenor variation LABEL 'Variation Mid {pillar} > 10%'.
  Equity reference quotes: unary VALUE_OF on QUOTE_LAST / QUOTE_MID (REFERENCE); discover QUOTE_* via SEC_CASH_INSTRUMENT inheritance when SEC_EQUITY export is thin.
---

# DataHub DQC — Data controls (mental model)

Use this skill when reasoning about **data quality controls** in DataHub, not generic “validation rules” elsewhere in the platform.

## Official overview (NeoXam — “Data Quality Control New Design”)

Workspace reference: `Knowledge/Reference/NeoXam DataHub - Data Quality Control New Design.pdf` (NeoXam, 2026). Use it for **screen flows**, **business semantics** (quality fields, inheritance, PASS/FAIL wording), and **built-in control types** (**Value Of**, **Series Jump**, **Stale**). Continue to use **this skill’s** `DATACONTROL_TYPE` / Java factory / **rule-backed** sections for packaging, **operand reuse**, and IMPACT contracts—the PDF is product-guide level and does not cover those migration details.

### Module shape

- **Data control** — verifications grouped as **comparison clauses** (assessed vs operator vs target).
- **Control execution rules** — **when** controls run (condition + scope) and **effects** when issues are found.

### Factory navigation (documentation)

| Topic | Datahub Factory path |
|--------|----------------------|
| Data controls | **Data Administration → Data Quality → DQC → Data Controls** |
| Execution rules | **Data Administration → Data Quality → DQC → Data Control Execution Rules** |
| Screening / results | **Data Administration → Data Quality → DQC → Data Quality Screening Report** |

### Control scope

- **Applicability** selects **Data Dictionary**, **Business Dictionary**, or **Scopes**; the PDF notes **only Business Dictionary** at documentation time.
- Control **business class** scopes clause authoring: **only fields from that class** appear for clauses.

### Identification fields (control header)

- **Active** — inactive controls are **not** run during quality screening.
- **Quality level** — qualifies data at issue origin; feeds **golden copy calculation rules**.
- **Quality indicator** — indicator impacted when an issue is found.
- **Comment** — human-readable scope.

### Operators vs assessed result type (UX)

The UI filters operators from **`DATACONTROL_CLAUSE_OPERATORS`** based on the **evaluated type** of assessed data:

| Assessed result type | Operators offered |
|----------------------|-------------------|
| **Numeric**, **Date** | Full set (including inequalities). |
| **List**, **Object**, **String** | **`<>`**, **`=`**, **Is Null**, **Is Not Null** only. |

**Target** business fields are filtered to types compatible with assessed side; **fixed value** editors follow assessed type (object instance, list item, date picker, numeric).

### Built-in control types (product documentation ↔ `DATACONTROL_TYPE`)

| UI / doc name | Typical role |
|---------------|--------------|
| **Value Of** | Current value of the data source (`VALUE_OF`). |
| **Series Jump** | Time-series delta: current vs **previous** value (`SERIESJUMP`). |
| **Stale** | Days since the time-series value was last updated (`STALE`); **no parameters** in the PDF. |

**Series Jump** configuration (Factory):

- **Calculation mode**: **% Difference** or **Value Difference** — PDF default when empty: **% Difference**.
- **Factor**: decimal **0–1**, multiplies the computed delta; default **1**.
- **Absolute Value**: **Yes** / **No**, default **No** — **No** preserves sign (increase vs decrease); **Yes** returns magnitude.
- **Time-depth** (days): default **1** — when set (e.g. D-3), **previous_available_value** is the **average** of available values over that many days.

**Series Jump formulas** (with factor **F**):

- **Value Difference:** `(current_value - previous_available_value) * F`
- **% Difference:** `((current_value - previous_available_value) / previous_available_value) * F`

*(PDF section headings swap labels once; formulas above match the body text.)*

### Execution rules

Screen: **Data Control Execution Rules**.

- **Condition** — applicability (business-class scope + optional filter; PDF example: Activity Country = France).
- **Control** — ordered list of controls to execute; only **active** controls whose **applicability matches the rule** can be selected.
- **Effects** — PDF lists **Raise Exception** only: exception **priority**, **reject type**, **assigned user**, **assigned group**; **exception reason** and **exception message** marked **not used** in the PDF.

**Business class inheritance:** rules on a **parent** class apply to **child** classes (PDF example: Security Core vs Equity).

### Screening: PASS / FAIL / ERROR (vendor wording)

NeoXam describes clause outcomes for **execution tracking** as:

- **PASS** — no anomaly; assessed value **does not match** the target encoding that represents the **data issue**.
- **FAIL** — anomaly; assessed value **matches** that issue-encoding target condition.
- **ERROR** — technical error (bad syntax, unavailable server, etc.).

Treat this as **documentation for screening semantics**, not a substitute for proving behaviour on your hub for **every operator** (inequalities and unary null checks should still be validated in the target environment).

### Execution tracking

- Each screening run can produce **`MxControlExecResult`** with rule status, **trigger** (PDF: **on-demand** via **business rules** only at documentation time), control summary, and clause detail (**label**, **status**, **assessed value**, **target value**).

### System parameters (technical errors)

Configure as **`MxParameter`** when required:

| Code | Role |
|------|------|
| **`dqc.tech.err.reject.type`** | Reject type for technical errors; default **`DQC_ERROR`** if unset |
| **`dqc.tech.err.reject.priority`** | Priority for technical errors; empty if unset |
| **`dqc.tech.err.reject.group`** | Group for technical errors; empty if unset |

### Clause maintenance (UI)

**Duplicate** clones a clause row for editing; **Delete** removes the clause and **links** (exceptions, tracking) per product documentation.

## Core structure (authoritative)

- A **control** (`MxDataControl`) contains **many comparison clauses** (rows on the control’s clause table, e.g. `DATACONTROL_CLAUSES`).
- Each clause is one **comparison**: **assessed data** vs **target data** using an **operator** (`=`, `<>`, `>`, `Is Null`, etc.).
- **Assessed data** and **target data** are each an **`MxControlClauseData`** object. They are **definitions** evaluated at run time to values.
- Each `MxControlClauseData` is built as: **control type** × **data point** (plus provider/source metadata).
  - **Control type**: stored as **`CONTROL_TYPE`** — internal code of list **`DATACONTROL_TYPE`**.
  - **Data point**: typically **`MxBusinessField`** referenced by **`BUSINESS_FIELD`**, scoped by **`BUSINESS_CLASS`** (`MxBusinessClass`), resolved at execution to **`MxObjectFieldDef`** / record matching on the **`MxObject`** under control.

**Operand reuse (platform constraint):** a given **`MxControlClauseData`** (**`CODE`**) must **not** be referenced more than **once** on the same **`MxDataControl`** across all clause rows—whether as **assessed** or **target**. You cannot point several clause rows at the same operand definition. When the same *logical* threshold or field applies to N pillars, create **N** distinct **`MxControlClauseData`** objects (each with a unique **`CODE`**; configuration can be identical—e.g. eight **`VALUE_OF`** targets each with **`DATA_VALUE`** **10** for 10%).

Phrase explanations as: **(control type + inputs) operator (other operand)** — not “raw column equals literal” unless both sides are fixed constants.

## Defect-oriented clauses (workspace convention)

In **this DH DQC workspace**, clauses are authored **“as-is” for defects**: phrase the predicate in the shape of the quality breach (what is wrong when the check fires). Stored **`CLAUSE_OPERATOR`** (**`DATACONTROL_CLAUSE_OPERATORS`**) aligns with that reading. For unary **null** checks specifically, stakeholder wording is often **«not pass when null»**: **empty / null assessed value ⇒ clause outcome is not acceptable** (**`NULL`** + **Is Null** list label.)

| Defect intent | Stored operator | Typical UI label (`MxList_DATACONTROL_CLAUSE_OPERATORS`) | Typical assessed / target setup |
|----------------|-----------------|-----------------------------------------------------------|---------------------------------|
| **Missing / empty** field | **`NULL`** | Is Null | **`VALUE_OF`** on **`MxBusinessField`** (**`BUSINESSF`**). **Unary** clause — omit **`TARGET_DATA`**. **`LABEL`** e.g. **`Curve Is Null`** / **`Mid 1D Is Null`**. **`NOTNULL` / Is Not Null** is the complementary unary; use only when validated on the hub for your scenario. |
| **Above cap** on a numeric measure (e.g. variation % points) | **`GREATER`** | **`>`** | Often **«assessed > threshold»** (**e.g.** > 10 percentage points vs target **`10`**). Assessed **`NUMERICF`** (**`YC_TENOR_REL_RATIO`**) vs **`VALUE_OF`** target (**`DATA_VALUE`** **`<![CDATA[10]]>`** / plain **10** in pack). Clause **`LABEL`** e.g. **`Variation Mid 1Y > 10%`**. |

**Alternative (tolerance wording):** **`LOWER_OR_EQUAL`** (**`≤`**) expresses “assessed stays within band” vs the same numeric target—not the breach spelled out—for the same mathematical relationship; pick one style per pack and verify control pass/fail on the hub.

External or historical notes sometimes describe unary **`NULL`** as “clause passes **only when** null”. **That wording is rejected for packs in this repo**—here **`NULL`** means **failure / anomaly on missing null-or-empty assessed values** alongside **Is Null** labelling.

### YC curve valuation — display naming (CV)

- **Control title / `T_DATACONTROL_NAME`:** **`CV - <functional phrase>`** using **ASCII hyphen-minus** (**`-`**, U+002D). **Do not** use the em dash (**`—`**, U+2014) between **`CV`** and the phrase (avoids “CV — …” in dictionaries).
- **`R_DATACONTROL_CLAUSES` `LABEL`** (unary completeness): **`{Field} Is Null`** — **spaces only**, e.g. **`Mid 1D Is Null`**, **`Curve Is Null`**, **`Valuation date Is Null`** (**not** `Field — Is null`, **not** prefixes like “Tenor — …”).
- **`R_DATACONTROL_CLAUSES` `LABEL`** (tenor variation defect): **`Variation Mid <pillar> > 10%`** (e.g. **`Variation Mid 1D > 10%`**). Keep assessed operand dictionary labels short and aligned (**`Variation Mid 1D`** on **`MxControlClauseData`**). Target threshold operands often use **`LABEL`** **`10%`** so runtime text does not repeat the pillar (`LIST_DATACONTROL_TYPE_PARTIAL_YC_TENOR_REL_RATIO_1`: EN **`ITEM_NAME`** **`Variation`** on **`YC_TENOR_REL_RATIO`**).

Runtime **`DataControlType`** instances come from **`DataControlTypeFactory`** reading **`DATACONTROL_TYPE`** (`dh_core`: see `.../define/clausedata/controltype/DataControlTypeFactory.java` under the local DH repo).

**Critical branch:**

1. **If the list item has non-empty Free1** → **`RuleBasedDataControlType`**: Free1 = **rule code**, Free2 = **`DATACONTROL_VALUE_FORMAT`** / return shape (`REF_LISTF`, `NUMERICF`, …), Free3 = list code (`YES_NO`) or return class name when applicable.
2. **Else** → built-in classes (`VALUE_OF`, **`CHANGE`** → `ChangeDataControlType`, `SERIESJUMP`, `STALE`, …). **`ChangeDataControlType`** is a thin class; **operative “Change” behaviour in configured environments usually depends on Free1 pointing at a rule** — verify per database.

**Execution routing** (`ClauseDataBuilder.createBuilder`): if **`controlType.isRuleBased()`** → **`RuleClauseDataBuilder`** (even when **`DATA_SOURCE_TYPE`** is **`BUSINESSF`**). The rule runs as **`RulesManager.executeRule(ruleCode, [controlledMxObject, MxControlClauseData], …)`** (`ClauseRuleEvaluator`).

Rules are exported as **`MxRule`** rows (**`RULE_CODE`**); use **`getObjectPackage`** with **`ClassName`: `MxRule`**, **`ObjectCode`**: rule code from Free1 — class names like **`MxBusinessRule`** may not apply on all installs.

## Methodology — rational for reverse-engineering / modelling (reuse)

Follow this order so conclusions stay **environment-grounded** and **reusable**:

| Step | Action | Why |
|------|--------|-----|
| **A** | Export **`MxControlClauseData`** pack(s) for assessed/target operands | **`BUSINESS_CLASS`**, **`BUSINESS_FIELD`**, **`CONTROL_TYPE`**, **`DATA_SOURCE_TYPE`**, **`PROVIDER`** are authoritative configuration — not UI labels alone. |
| **B** | Export **`MxList` / `DATACONTROL_TYPE`** | **`CONTROL_TYPE`** on clause data is only an internal **list code**. FREE columns decide **rule vs Java-built-in** and **result shape**. |
| **C** | On the **`DATACONTROL_TYPE`** row matching **`CONTROL_TYPE`**: read **Free1 / Free2 / Free3** | **Free1 non-empty** ⇒ **`RuleBasedDataControlType`** → behaviour lives in **`MxRule` IMPACT** (+ Free2/Free3 typing). **Free1 empty** ⇒ inspect **`DataControlTypeFactory`** switch + corresponding **`…DataControlType.java`** under **`controltype/`** in DH source. |
| **D** | If rule-based: **`getObjectPackage(MxRule, Free1)`** and read **`IMPACT`** | True semantics (e.g. audit-trail vs multi-provider compare) are **here** — do not infer only from labels like “Change” or **`PROVIDER`** unless the rule uses them. |
| **E** | Cross-check DH Java only when clarifying **plumbing** (builders, adapters, inactive-rule checks) | Source explains **routing** (`RuleClauseDataBuilder`, `BusinessFieldClauseDataBuilder`); **business meaning** for rule-based types is still **list + rule**. |

**Example pattern (this workspace / typical config):** internal code **`CHANGE`** with Free1 **`DQC_CHANGE`**, Free2 **`REF_LISTF`**, Free3 **`YES_NO`** ⇒ assessed operand resolves to **`YES_NO`** item ids via rule **`DQC_CHANGE`**; rule receives **`(MxObject, MxControlClauseData)`** — implementation detail remains entirely in **`IMPACT`** (do not assume without reading it).

When **modelling new controls**: choose or configure **`DATACONTROL_TYPE`** first (rule vs built-in + return format), then **`MxControlClauseData`** operands, then **`MxDataControl`** clause rows and operators — matching **`EvaluatorValidity`** expectations for assessed/target source-type pairs.

## Authoring a new rule-based control (end-to-end checklist)

Use this when **adding** a type like **`STRING_REGEX`** (full-string Java regex vs a business field, result **`YES_NO`**), or any **Free1-driven** rule type.

### 1. Contract on `DATACONTROL_TYPE`

- Add a **new list item** (internal code = value stored on **`MxControlClauseData.CONTROL_TYPE`**).
- **Free1**: **`MxRule.RULE_CODE`** executed by **`RuleClauseDataBuilder`** (e.g. `DQC_STRING_REGEX`).
- **Free2**: return shape compatible with evaluator expectations (e.g. **`REF_LISTF`** when the rule returns **`YES_NO`** ids via **`getListItemId`**).
- **Free3**: target list code when applicable (e.g. **`YES_NO`**).

Prefer **two migration packages** for lists: **(0)** item row only, **(1)** **`SMARTLIST_ITEM_LABEL`** rows only — same **`PARTIAL="1"`** / **`FIND`** pattern as other list deltas.

### 2. `MxRule` IMPACT (clause evaluator contract)

For **`RulesManager.executeRule(ruleCode, [controlledMxObject, MxControlClauseData], …)`**:

- **`arg1`** — controlled **`MxObject`** (the instance under validation).
- **`arg2`** — assessed **`MxControlClauseData`** clause definition (**same object** the factory passes into **`RuleClauseDataBuilder`**).

**Worked implementation notes** (avoid compiler/runtime pitfalls):

| Topic | Do | Don’t |
|-------|-----|--------|
| Read assessed field code | `businessField := getObject("MxBusinessField", clauseCtrlData.BUSINESS_FIELD)` then `bfCode := businessField.CODE` | Assume **`TECH_FIELD`** or **`PROVIDER`** unless the rule design requires it |
| Field value on controlled object | **`fieldVal := obj.getBusinessFieldValue(bfCode)`** | **`obj.MxObject.getBusinessFieldValue(...)`** — not valid IMPACT |
| Coerce to string | **`strVal := strcat("", fieldVal)`** | **`toStr(...)`** — not available in IMPACT |
| Regex | **`checkPattern(pattern, strVal)`** with **`pattern`** from **`clauseCtrlData.CONTROL_SCRIPT`** (full-string match in product) | Invent helpers not present in grammar |
| Boolean result | Compare rule/helper output to **`"1"`** / **`"0"`** as documented for **`checkPattern`** in your environment | |
| Return type when Free3 is **`YES_NO`** | **`getListItemId("YES_NO", "Y")`** / **`"N"`** | Bare **`"Y"`** / **`"N"`** literals when **`getListItemId`** ids are required |
| Return type when Free2 is **`NUMERICF`** and Free3 is empty | Return a **numeric expression** (e.g. ratio or percentage points) | **`getListItemId`** — wrong type for numeric clause |
| **Units** (numeric assessed vs **`VALUE_OF`** target) | Rule output and **`DATA_VALUE`** must use the **same scale** (both ratio 0–1, both % points 0–100, etc.) | Mixed scales (e.g. `0.09` assessed vs target `10`) without converting in the rule |

### 3. Assessed `MxControlClauseData` (rule-based “compute” operand)

Example **equity ISIN regex** assessed clause:

- **`CONTROL_TYPE`**: internal code of the new **`DATACONTROL_TYPE`** item (e.g. **`STRING_REGEX`**).
- **`BUSINESS_CLASS`**: e.g. **`[CODE='SEC_EQUITY']`** (scope of the clause definition).
- **`BUSINESS_FIELD`**: reference to **`MxBusinessField`** for ISIN on security, matching exports, e.g. **`[TECH_CLASS^CODE='[CLASS_NAME='MxSecurity']^ISIN']`** (verify with **`getObjectPackage(MxBusinessField, …)`** in the target env).
- **`DATA_SOURCE_TYPE`**: **`BUSINESSF`**, **`PROVIDER`**: **`REFERENCE`** (typical for dictionary-driven points).
- **`CONTROL_SCRIPT`**: **Java regex** used by **`checkPattern`** (full match). Note: Java quantifiers use **`{0,1}`** without a space — a pattern like **`{0, 1}`** may fail at runtime even if packaging succeeds.

### 4. Target `MxControlClauseData` (often `VALUE_OF`)

For **`YES_NO`** comparison to “expected pass”:

- **`CONTROL_TYPE`**: **`VALUE_OF`**
- **`DATA_SOURCE_TYPE`**: **`VALUE`**, **`DATA_FORMAT`**: **`REF_LISTF`**, **`DATA_VALUE`**: pack form like **`,"LST","YES_NO","Y",`**
- **`BUSINESS_CLASS`**: align with control scope (e.g. **`SEC_EQUITY`**) when the clause is class-scoped.

### 4b. Completeness / null checks (**`VALUE_OF` + unary clause operators`)

**Quick reference:** see **Defect-oriented clauses (workspace convention)** above (**`NULL`** / **«not pass when null»**).

For **“missing value must be flagged”** (dictionary completeness): model the assessed side as **`VALUE_OF`** on the **`MxBusinessField`** (**`CONTROL_TYPE`** = **`VALUE_OF`**, **`DATA_SOURCE_TYPE`** = **`BUSINESSF`**, scoped **`BUSINESS_CLASS`**, **`PROVIDER`** = **`REFERENCE`** as usual). Author the unary operator as **`NULL`** (**`DATACONTROL_CLAUSE_OPERATORS`**): **`Is Null`** in the UX list corresponds to **`NULL`** in pack XML. **`NULL`** here means **anomaly when the assessed value resolves null / empty** — ie. the clause is written in defect terms (**not** “clause passes only if null”; that older mental model conflicts with authoring in this DH DQC project). Unary **`NOTNULL`** (**“Is Not Null”**) is the symmetric operator for complementary checks — use whichever matches your hub’s unary outcome after validation.

Typically **omit `<TARGET_DATA>`** on the clause row (pure unary). Once loaded, some hubs still persist **`T_DATACONTROL_CLAUSES.CODEFIELDS="ASSESSED_DATA^CLAUSE_OPERATOR^TARGET_DATA"`** with a third merge key sentinel **`null`** (`CODE` triple ends with **`["TARGET_DATA","null",]`**) and an empty **`<TARGET_DATA></TARGET_DATA>`** body — mimic an export from **`get_object_package`** for future deltas.

**Migrator caveat (7.x patterns):** **`MxDataControl`** exports often key clause rows by **`ASSESSED_DATA^CLAUSE_OPERATOR^TARGET_DATA`**. Updating an installed control from **binary** (`EQUAL` + **`Target_YC_DQC_PASS_YES`**) to **unary (`NULL` / `NOTNULL` + no target)** may **fail** with **`EVALUATE_ORDER` duplicates** rather than cleanly replacing clause rows — because the merger treats the triple as a distinct key until old rows are removed. Safer workflows: (**a**) **new `CODE`** + fresh clause rows keyed by **`EVALUATE_ORDER` only**, or (**b**) **delete/remove** the obsolete clause rows in DataHub UI, then re-import; **reuse `get_object_package`** from the hub to mirror exact row shape when in doubt.

### 4d. Target **`VALUE_OF`** — **numeric** threshold (`NUMERICF`)

**Quick reference:** see **Defect-oriented clauses** (**`GREATER`** vs **`LOWER_OR_EQUAL`**) above.

**Factory / dictionary “Value” for a fixed operand:** the **number** belongs in **`CONTROLCLAUSEDATA.DATA_VALUE`**, **not** only in **`LABEL`**, **`PARAMETER_VALUE`**, **`BUSINESS_FIELD`**, or **`CONTROL_SCRIPT`**. With **`VALUE_OF`** + **`DATA_SOURCE_TYPE`** **`VALUE`** + **`DATA_FORMAT`** **`NUMERICF`**, the UI **Value** column is loaded from **`DATA_VALUE`**. For a **10%** cap when the assessed rule returns **percentage points**, pack **`DATA_VALUE`** as plain **`10`** in CDATA (e.g. **`<![CDATA[10]]>`**) so Factory shows **10** — **not** the raw typed blob **`,"DBL",10,`**, which some screens display literally. After import, **`getObjectPackage`** may round-trip either form depending on build; **match your Hub’s export** if in doubt.

Use when the assessed side resolves to a **number** and the clause compares to a **constant**. Two authoring styles:

- **Tolerance / acceptance (traditional):** e.g. **`LOWER_OR_EQUAL`** so the clause expresses **variation ≤ maximum** (“pass inside the band”).
- **Defect-orientation (recommended in this DH DQC workspace):** encode the violation directly — e.g. **`|Δ|` must not exceed 10% vs prior** ⇒ clause **`GREATER`** (list **`>`**) comparing assessed to target numeric **10** when the assessed rule returns percentage points (**`|Δ|/prior| * 100`**). **`LABEL`** e.g. **`Variation Mid 1Y > 10%`**. Targets still use **`VALUE_OF`**, **`DATA_FORMAT`** **`NUMERICF`**, **`DATA_VALUE`** plain **`10`** in CDATA (see above); operand **`LABEL`** often **`10%`**.

- **`CONTROL_TYPE`**: **`VALUE_OF`**
- **`DATA_SOURCE_TYPE`**: **`VALUE`**, **`DATA_FORMAT`**: **`NUMERICF`**
- **`DATA_VALUE`**: **`VALUE_OF`** + **`NUMERICF`** targets for this workspace: prefer **CDATA plain number** (**`<![CDATA[10]]>`** for **10**) when authoring packs so Factory **Value** stays readable. Alternate typed export shape **`,"DBL",<n>,`** may appear after **`getObjectPackage`** — keep **percentage-point scale** aligned with assessed output (**10** ⇒ **10%** when assessed returns **`|Δ|/prior| * 100`**). For ratios in **0–1**, use **`0.1`** / **`,"DBL",0.1,`** consistently with assessed scale.
- **`BUSINESS_CLASS`**: same scope as the control / assessed operands.

If **`DATA_VALUE`** loads but the **UI shows empty**, the encoding may not match your Hub build—set the value once in the UI, then **`getObjectPackage(MxControlClauseData, …)`** and reuse the exported **`DATA_VALUE`** byte-for-byte.

**One operand per clause row:** if multiple pillars need the same numeric threshold, create **separate** **`MxControlClauseData`** rows (unique **`CODE`**) per row—**operand reuse across clause rows is invalid** (see core structure).

**Labels in the UI:** the **`LABEL`** field on **`R_CONTROLCLAUSEDATA`** is not always enough. Add **`T_CONTROLCLAUSEDATA_NAME`** with **`R_CONTROLCLAUSEDATA_NAME`** (**`LANGUAGE`**, **`NAME`**) per the pattern in `Knowledge/Temp/Target_16_04_33.pack` or **`Implementation/Installed/MxControlClauseData_Target_Equity_ISIN_Y.pack`** (`LOCAL_ID` on the name row typically matches the clause-data row in the same pack).

**`CONTROLCLAUSEDATA_NAME` / `DATACONTROL_NAME` on reinstall:**  
- **Full installs** (new control / new operands): populate **`T_DATACONTROL_NAME`** (**`R_DATACONTROL_NAME`**, **`LANGUAGE`**, **`NAME`**) or the control title may show as generic **“Data Control (id)”**. Populate operand **`T_CONTROLCLAUSEDATA_NAME`** for dictionary-friendly labels.  
- **Hotfix / delta-only** reinstalls: if the loader reports duplicate **`LANGUAGE`** on **`DATACONTROL_NAME`** / **`CONTROLCLAUSEDATA_NAME`**, ship **empty** **`T_*_NAME`** sections (same idea as **`MxRule`** name tables) when you are not intentionally renaming.

### 5. `MxDataControl` package XML (learned reference shapes)

Wrapper tag is **`DATACONTROL`** (migration export shape); main row **`T_DATACONTROL`** / **`R_DATACONTROL`**, clauses **`T_DATACONTROL_CLAUSES`** / **`R_DATACONTROL_CLAUSES`**, names **`T_DATACONTROL_NAME`** / **`R_DATACONTROL_NAME`**.

On at least one **7.6**-style environment:

- **`APPLICABILITY`** (list **`CONTROL_APPLICABILITY`**): use the **plain internal code** for Business Dictionary — **`BIZDICO`** — not comma-wrapped **`[INTERNAL_CODE='…']`** strings (those were rejected as unknown list items).
- **`ASSESSED_DATA` / `TARGET_DATA`**: **`[CODE='YourClauseCode']`** (no leading **`,`** wrapper).
- **`CLAUSE_OPERATOR`**: **`EQUAL`** worked for “assessed equals target” (**`=`** in UI).

**Clause merge keys:** Hub exports often set **`T_DATACONTROL_CLAUSES CODEFIELDS="ASSESSED_DATA^CLAUSE_OPERATOR^TARGET_DATA"`**; each **`R_DATACONTROL_CLAUSES`** **`CODE`** attribute encodes that **triple**. Packs keyed only by **`EVALUATE_ORDER`** can **fail to update** an existing control (e.g. **duplicate `EVALUATE_ORDER`** / insert path). For the **canonical shape**, **`getObjectPackage(MxDataControl, controlCode)`** from the **target** environment. After changing operator or target references, the **merge triple** changes—expect merge friction unless rows are removed.

**Recreate-after-delete pattern:** if the user **deletes the control** (or all clause rows) in the UI, import a **fresh** pack with **`LOCAL_ID="0"`** on **`R_DATACONTROL`** and on clause rows (Hub assigns ids). Ensure each **`R_DATACONTROL_CLAUSES`** **`CODE`** attribute matches the **actual** **`ASSESSED_DATA`**, **`CLAUSE_OPERATOR`**, and **`TARGET_DATA`** in the row body—do not embed an **old** triple in **`CODE`** while the body shows **new** operator/target.

**Operational gotcha:** **`getObjectPackage(MxDataControl, objectCode)`** can **fail when `CODE` contains `/`** (filesystem path for the temp pack). Prefer **slash-free control codes** (e.g. `CONTROL_EQUITY_ISIN_REGEX`) for objects you need to export by code.

### 5b. Worked pattern — yield curve **tenor variation** (numeric assessed vs threshold)

Example aligned with **`MxYieldCurveValu`** pillar mids (see **`MxDataControl_CONTROL_YC_TENOR_VARIATION.pack`**, **`…_VARIATION_1.pack`**, **`…_VARIATION_2.pack`** — suffix bumps when reinstalling):

1. **`DATACONTROL_TYPE`** item **`YC_TENOR_REL_RATIO`**: Free1 **`DQC_YC_TENOR_REL_VAR_RATIO`**, Free2 **`NUMERICF`**, Free3 empty; rule returns a **number** (percentage points if target is **10** for 10%).
2. **Assessed operands** (one per pillar): **`CONTROL_TYPE`** **`YC_TENOR_REL_RATIO`**, **`BUSINESS_FIELD`** = pillar mid, **`DATA_SOURCE_TYPE`** **`BUSINESSF`** — **unique `CODE` per pillar**.
3. **Target operands** (one per pillar): **`VALUE_OF`**, **`DATA_SOURCE_TYPE`** **`VALUE`**, **`DATA_FORMAT`** **`NUMERICF`**, **`DATA_VALUE`** **`<![CDATA[10]]>`** (plain **10** = **10%** when assessed returns **% points**). **Unique `CODE` per pillar**. Dictionary **`LABEL`** **`10%`** is **display only** — execution uses **`DATA_VALUE`**.
4. **Clauses (defect-oriented, recommended here):** **`GREATER`** (list **`>`**). **`R_DATACONTROL_CLAUSES` `LABEL`** = **`Variation Mid <pillar> > 10%`**. **Alternative:** **`LOWER_OR_EQUAL`** (**`≤`**) if you prefer tolerance (“in band”) wording for the same cap.
5. **Rule contract:** compute **`|Δ|/prior|`** vs latest prior **`MxYieldCurveValu`** on same **`YIELDCURVE`**; scale **`* 100`** if targets use **percentage points**.

### 5c. Worked pattern — **equity** reference quotes empty (unary completeness)

**Field discovery:** **`SEC_EQUITY`** often inherits quote fields from **`SEC_CASH_INSTRUMENT`** (same **`TECH_CLASS`** **`MxSecurity`**). A **`get_object_package(MxBusinessClass, SEC_EQUITY)`** export may list mostly equity-specific analytics fields; **reference prices** typically appear under **`QUOTE_*`** on the **parent** class export (**`MxBusinessClass` `SEC_CASH_INSTRUMENT`**). Confirm operand refs with **`get_object_package(MxBusinessField, …)`** (see **`datahub-object-retrieval`** — simple **`CODE`** like **`QUOTE_LAST`** when unique).

**Operands:** **`CONTROL_TYPE`** **`VALUE_OF`**, **`DATA_SOURCE_TYPE`** **`BUSINESSF`**, **`BUSINESS_CLASS`** **`[CODE='SEC_EQUITY']`**, **`BUSINESS_FIELD`** e.g. **`[TECH_CLASS^CODE='[CLASS_NAME='MxSecurity']^QUOTE_LAST']`** / **`…^QUOTE_MID'`**, **`PROVIDER`** **`REFERENCE`** (matches **`MxBusinessField`** **`REC_SPEC`** on standard quote fields in many hubs).

**Clauses:** unary **`NULL`** (**Is Null**), defect-oriented **`LABEL`** e.g. **`Last Quote Is Null`**, **`Mid Quote Is Null`**; **omit** **`TARGET_DATA`**. One assessed **`CODE`** per clause; do not reuse the same operand **`CODE`** on another row of the same control.

**Naming:** reserve **`CV - …`** / pillar wording for **yield-curve** controls; equity controls use a plain functional title (e.g. **Equity - Quote completeness**).

### 6. Install order and `MxRule` hotfix packages

Recommended order:

1. **`MxRule`** (rule code in **Free1** must exist before the clause type is exercised).
2. **`DATACONTROL_TYPE`** partial **item**, then **labels** — **skip** if the **`INTERNAL_CODE`** already exists (reinstall often returns **duplicate list item** / Status 300).
3. **`MxControlClauseData`** operands (assessed, then target).
4. **`MxDataControl`** linking clause row(s).

**Operand `LOCAL_ID`:** when **updating** existing **`MxControlClauseData`** objects (e.g. fixing **`DATA_VALUE`** for a numeric threshold), set **`R_CONTROLCLAUSEDATA` `LOCAL_ID`** to the **object id in the target database** from **`getObjectPackage(MxControlClauseData, operandCode)`**. Pack ids copied from another environment may **silently fail** to apply **`DATA_VALUE`** if the merger keys on **`LOCAL_ID`**.

**Operand hotfix naming:** reinstalling under the **same `PACKAGE`** code rarely reapplies **`DATA_VALUE`** fixes; ship a **new pack name** (e.g. **`YC_DQC_VAR_THRESH_DATAVALUE_FIX_1`**, **`…_FIX_2`** for plain-**`10`** **`DATA_VALUE`**) and bump **`MxDataControl_…`** pack names similarly. See **`datahub-pack-installation`** (“Same package twice”).

**Pack XML hygiene (Migration):** row elements must use **`CODE=",["KEY","value",]"`** with **double quotes** around the attribute value (`CODE="..."`). Single-quoted **`CODE='...'`** rows can trigger **“Missing keyword `CODE=\"`”** loader errors.

**Reinstalling an existing `MxRule`:** a **full** rule pack may attempt to recreate **`SMARTRULE_NAME`** and fail on duplicate languages. For **IMPACT-only** updates, ship only **`R_SMARTRULE`** under **`T_SMARTRULE`**, leave **`T_SMARTRULE_NAME`** and **`T_SMARTRULE_TRIGGER`** empty (no **`R_`** rows), keep **`T_SMARTRULE_WFLINK`**, and set **`LOCAL_ID`** on **`R_SMARTRULE`** to the **existing** rule object id in that database.

Use **`datahub-pack-installation`** + **`install_package.py`** (`ReleaseManagementResult` JSON) for API installs; validate with **`datahub-business-rules`** / **`validate_impact_syntax`** when br-knowledge is available.

## Agent workflow (modelling new controls)

1. **Data model**: `getObjectPackage` **`MxClassDef`** / **`MxDataControl`** / **`MxControlClauseData`** when packs are missing locally (`Knowledge/Model/Objects/`).
2. **`DATACONTROL_TYPE`**: Treat FREE columns as part of the **contract** for that control type (rule code + result typing).
3. **Clause data**: Correct **`CONTROL_TYPE`**, **`BUSINESS_FIELD`** / **`BUSINESS_CLASS`**, **`DATA_SOURCE_TYPE`**, **`PROVIDER`**, and for rule-based assessed operands **`CONTROL_SCRIPT`** when the rule reads it.
4. **Control**: Clause rows — **unique** assessed + **unique** target **`CODE`** per row (when binary); unary **`NULL`** / **`NOTNULL`** omit target; operators per defect conventions; **`LABEL`**: unary **`{Field} Is Null`**, variation **`Variation Mid <pillar> > 10%`**; **`T_DATACONTROL_NAME`** / control **`LABEL`**: **`CV - …`** with ASCII hyphen for **curve valuation** scopes; otherwise a plain functional title (e.g. equity); evaluate order + parentheses / **`PARENTHESIS_OPERATOR`**.
5. **Validate**: **`datahub-testing-validation`** after install; **`datahub-object-search`** for smoke queries.

## Related skills

- `datahub-business-class` — **`MxBusinessClass`**, **`BUSINESSCLASS_FIELD`**, **`BUSINESS_CLASS`** scoping packs
- `datahub-yield-curve` — **`MxYieldCurveValu`** / **`YC_*`** alignment for curve DQC operands
- `datahub-data-model` — `MxClassDef` / `MxList`
- `datahub-object-search` — query limits / field quirks
- `datahub-object-retrieval` — `getObjectPackage`
- `datahub-pack-creation-modification` — pack edits / lists
- `datahub-pack-installation` — **`install_package.py`**, API install order, duplicate list-item skips
- `datahub-business-rules` — IMPACT grammar, **`EXIT_0`/`EXIT_1`**, **`strcat`**, validation MCP

## Correction note (for the agent)

Do **not** infer operand behaviour from **`CONTROL_TYPE`** label (“Change”) or **`PROVIDER`** alone when **`DATACONTROL_TYPE`** is rule-backed — **`MxRule` IMPACT** + list FREE columns are the source of truth.

Do **not** map unary **`NULL`** to “clause passes **only when** empty” when authoring **`Implementation/Installed`** curve DQC—or swap **`NOTNULL`** in its place—for **missing-field** completeness without user confirmation after **`get_object_package`** on the hub. **Do not** document **section 5b** as **`LOWER_OR_EQUAL`**-only without the **`GREATER`** defect-oriented option for numeric caps (**`>`**) per this workspace.
