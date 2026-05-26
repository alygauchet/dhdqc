# DataHub Pack Creation — Reference

## Pack File Structure (Full)

Pack files are XML-based DataHub package exports:

```xml
<?xml version='1.0' encoding="UTF-8" ?>
<HEAD>
  <PACKAGE>PACKAGE_CODE</PACKAGE>
  <NAME>Package Display Name</NAME>
  <BUILD_DATE>YYYYMMDD</BUILD_DATE>
  <LEVEL>OPTIONAL</LEVEL>
  <RELEASE>7.5.0</RELEASE>
  <CREATOR>Creator Name</CREATOR>
</HEAD>
<BODY>
  <RESULT MODE="XML" ACTION="GETOBJECTS" VERSION="2" CHARSET="UTF8">
    <!-- Object definitions here -->
  </RESULT>
</BODY>
```

## List Modification (SMARTLIST) — Full XML Example

**Correct structure for adding items** to an existing list:

```xml
<SMARTLIST FIND="LIST_CODE='LIST_NAME'" USER="..." UPDATE_DATE="..." UPDATE_TIME="..." LABEL='...' PARTIAL='1'>
  <T_SMARTLIST CODEFIELDS="LIST_CODE"></T_SMARTLIST>
  <T_SMARTLIST_CATEGORY></T_SMARTLIST_CATEGORY>
  <T_SMARTLIST_ITEM CODEFIELDS="INTERNAL_CODE">
    <R_SMARTLIST_ITEM CODE="..." LOCAL_ID="...">
      <!-- Item properties -->
    </R_SMARTLIST_ITEM>
  </T_SMARTLIST_ITEM>
  <T_SMARTLIST_ITEM_LABEL CODEFIELDS="IL_ITEM_ID^IL_LANGUAGE">
    <!-- Label entries -->
  </T_SMARTLIST_ITEM_LABEL>
  <T_SMARTLIST_NAME CODEFIELDS="NAME_LANGUAGE"></T_SMARTLIST_NAME>
</SMARTLIST>
```

Reference: Check `Knowledge/Model/Templates/LIST_MODIFICATION_EXAMPLE.pack` or `Implementation/Templates/LIST_MODIFICATION_EXAMPLE.pack` for the correct pattern.

## Workflow: Adding a New Item to an Existing List (with Custom Display Name)

Use this process when adding a new item (e.g. a new feed) to an existing list like FEED, where the item has a code (INTERNAL_CODE) and a display name (ITEM_NAME) that differ.

### Step 1 — Retrieve the List Package (Optional but Recommended)

Use getObjectPackage to fetch the current list (e.g. `MxList` / `FEED`). This provides:
- `FIND`, `USER`, `UPDATE_DATE`, `UPDATE_TIME`, `LABEL` for the SMARTLIST tag
- Structure of `R_SMARTLIST_ITEM` and `R_SMARTLIST_ITEM_LABEL` for reference

### Step 2 — Create Package 1: Add the Item

Create a pack with `PARTIAL='1'` that adds only the `R_SMARTLIST_ITEM`:

- `T_SMARTLIST`, `T_SMARTLIST_CATEGORY`: empty
- `T_SMARTLIST_ITEM`: one `R_SMARTLIST_ITEM` with:
  - `CODE=",["INTERNAL_CODE","YOUR_CODE",]"`
  - `LOCAL_ID="0"` (new item)
  - `INTERNAL_CODE`, `ITEM_ACTIVE`, `ITEM_PRIVACY_LEVEL`, `SORTING`
  - Empty: `COMMENT_TEXT`, `FREE1`–`FREE4`, `ICON_FILENAME`
- `T_SMARTLIST_ITEM_LABEL`: empty
- `T_SMARTLIST_NAME`: empty

Install this package first.

### Step 3 — Create Package 2: Add the Display Name (Label)

Create a second pack with `PARTIAL='1'` that adds only the `R_SMARTLIST_ITEM_LABEL`:

- `T_SMARTLIST`, `T_SMARTLIST_CATEGORY`, `T_SMARTLIST_ITEM`: empty
- `T_SMARTLIST_ITEM_LABEL`: one `R_SMARTLIST_ITEM_LABEL` with:
  - `CODE=",["IL_ITEM_ID",",[""INTERNAL_CODE"",""YOUR_CODE"",]",]["IL_LANGUAGE","0",]"` (0 = English)
  - `IL_ITEM_ID`, `IL_LANGUAGE`, `ITEM_NAME`, `ITEM_SHORT_NAME`
- `T_SMARTLIST_NAME`: empty

Install this package **after** the item package. The item must exist before the label can reference it.

### Import Order

1. `MxList_LISTNAME_ADD_ITEM.pack` (item)
2. `MxList_LISTNAME_ADD_ITEM_LABEL.pack` (label)

### Example: FEED List

See `Implementation/Installed/MxList_FEED_ADD_CURSOR.pack` and `MxList_FEED_ADD_CURSOR_LABEL.pack` for a working example (adds feed "Cursor" with code CURSOR).

## Package Creation Best Practices

- Create packages incrementally (not all changes at once)
- Include all dependencies in package or release
- Validate package before adding to release
- Use descriptive package names
- Document package purpose
- Group related objects together; keep packages focused
- Avoid mixing unrelated changes
