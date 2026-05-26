# Data Dictionary Customization Guide — Main Concepts

Extracted from *NeoXam DataHub - Data Dictionary Customization Guide* for understanding how data models are constructed in DataHub.

---

## 1. Object Internal Representation

Each object in NeoXam DataHub is a **3-dimensional array** `[table][record][field]`:

- **X-axis**: Tables in the object
- **Y-axis**: Records in a specific table
- **Z-axis**: Fields in a specific record

**Note**: The first table always has a 1:1 cardinality with the object.

---

## 2. Data Dictionary as a Class

The data dictionary is **itself a class of objects** (MxClassDef). Updates to the dictionary happen in **real time** and are published to all connected clients. The dictionary controls the database via the NeoXam DataHub server.

---

## 3. Objects: Master and Secondary Tables

Each class of business object has:

- **Master table**: Defines instances of the class (one record = one object). Cardinality 1:1.
- **Secondary tables**: Linked to the master with cardinality 0–1 or 0–n. Classify characteristics by nature and multiplicity.

**Example (SECURITY)**: Master table SECURITY; secondary tables SECURITY_PRICE (0–n prices), SECURITY_CDS (0–1 CDS-specific data).

---

## 4. Types of Tables

| Type | Purpose | Cardinality |
|------|---------|--------------|
| **Chronological** | Dated analysis, financial, price data; often with provider | 0–n |
| **CODE** | Code + type (ISIN, Sedol, Cusip, ISO) | 0–n |
| **NAME** | Internationalization; name + language | 0–n |
| **STATUS** | Life cycle, validity, process stages | 0–n |
| **COMMENT** | Non-structured text, date/user/type stamped | 0–n |
| **CLASSIFICATION** | Categorization (sectors, ratings) | 0–n |

**MxClassificationItem**: Handles classification tables that evolve over time, bitemporalization, and parent-child hierarchies.

---

## 5. Table Naming Conventions

- Master table name is **prefix** for secondary tables (e.g., SECURITY → SECURITY_PRICE).
- Master table name must **not** contain `_` (e.g., YIELDCURVE, not YIELD_CURVE).
- Names should be significant, avoid excessive abbreviations.
- Table names must not exceed **27 characters**.

---

## 6. Field Types

| Type | Description | Notes |
|------|-------------|-------|
| **Decimal** | Numeric decimal data | |
| **Date** | Date type | Format dd/mm/yyyy |
| **String** | Character strings | Up to 255 chars by default; use Text for longer |
| **Text** | Long data | No apparent size limit |
| **Integer / Reference** | Integers or reference to another class | Values in Integer range |
| **Reference** | Points to another object class | e.g., ISSUER → AGENT |
| **List** | Value from SMARTLIST | `[LIST_CODE='LIST_NAME']` → SMARTLIST_ITEM |
| **File** | File stored on server | Original format |
| **Document** | File stored as BLOB in database | |

---

## 7. Field Constraints and Uniqueness

- **Mandatory**: Field must be filled; server rejects save if empty.
- **Key**: Contributes to table key (max 5 fields).
- **Constraint**: Restricts perimeter of referenced class (e.g., ISSUER category for AGENT).
- **Uniqueness modes**:
  - **Intern**: Uniqueness among records in the table
  - **Extern**: Uniqueness among all objects
  - **Intern combined**: Multiple keys in table
  - **Intern+Extern**: Both
  - **Unique extern with same keys**: n-uplet unique across objects
  - **Unique extern/intern in same time interval**: For history tables (start/end date)

---

## 8. Fields Association and Secondary References

- **Fields association**: A field’s values can depend on other fields (e.g., RATING_VALUE depends on RATING_FEED and RATING_TYPE). Use **DISPLAY** property (CustomUI class).
- **Secondary references**: Retrieve codes from a referred object using key values. Format: `source_field1=target_field1, source_field2=target_field2`.

---

## 9. Objects Categories

Categories limit objects available in joints. Defined as **dynamic conditions** on the object. Example: AGENT categories (broker, issuer, counterparty) constrain references in TRADE.

---

## 10. History and Historicization

- **Code historicization**: Identification tables can have start/end date of validity. Requires start and end date fields in Optimization tab.
- **Time series**: Tables with DATE key; `*_DATE_END` field chains records. End date of most recent = 31/12/2999.
- **History discontinuity**: "Is discontinuous" allows gaps (e.g., ratings suspended then resumed).
- **Intraday data**: Time field (String, 8 chars) in key; null for EOD, HH:MM:SS for snapshots.

---

## 11. Maintenance Limitations

- **Deletions** of tables/fields: Effective in dictionary, must be **manually applied** in database.
- **Technical names** (class, table, field): Cannot be changed via UI; requires manual DBMS work.
- **Field type**: Cannot be modified. String size can be increased, not decreased.
- **Field reassignment**: Cannot move a field to another table; delete and recreate.

---

## 12. Data Dictionary Tabs

| Tab | Purpose |
|-----|---------|
| General | Structure of classes, tables |
| Fields | Field definitions |
| Categories | Object categories |
| Versioning | Object versioning |
| Override | Manual override |
| Validation | 4-Eyes validation |
| Packaging | Data packaging and transfer |
| Optimization | Caches, indexes, historicization |
| Archive | Data purge and archiving |
| Misc | Miscellaneous |

---

## Reference Document

Full guide: `NeoXam DataHub - Data Dictionary Customization Guide.pdf` (in this skill folder).
