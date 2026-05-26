---
name: datahub-object-search
description: Search NeoXam DataHub objects via the REST search API. Use when the user wants to query DataHub (MxDataControl, MxSecurity, MxWorkflow, MxControlClauseData, etc.), list objects, or retrieve object details without getObjectPackage.
---

# DataHub Object Search

## MCP Tools Used

- **REST search API** — Typically via DataHub MCP server. Queries objects by class with filters and field selection.

## Overview

The DataHub search API allows querying objects by class with filters and field selection. Use it to list controls, workflows, securities, clause data, or any searchable SmartClass.

## Endpoint

```
POST {baseUrl}/smartservicegate/resources/search
```

**Configuration:** Read `baseUrl` and credentials from `.datahub-workspace.json`:

```json
{
  "datahub": {
    "url": "http://nxdh-docker-product",
    "username": "lf.guimaraes",
    "password": ""
  }
}
```

## Request Format

```json
{
  "from": [
    {
      "className": "MxDataControl",
      "type": "data"
    }
  ],
  "where": {
    "logicalOperator": "AND",
    "criteria": [
      {
        "className": "MxDataControl",
        "field": "CODE",
        "operator": "EQUAL",
        "value": "CONTROL_CODE"
      }
    ]
  },
  "fields": [
    {"className": "MxDataControl", "field": "CODE", "label": "Code"},
    {"className": "MxDataControl", "field": "LABEL", "label": "Label"}
  ]
}
```

- **from**: Array of `{className, type: "data"}`. Use the SmartClass name (e.g. `MxDataControl`, `MxSecurity`, `MxWorkflow`).
- **where**: `logicalOperator` ("AND" | "OR") and `criteria` array. Empty `criteria: []` returns all objects (subject to API limits).
- **fields**: Array of `{className, field, label}`. Optionally add `keys` for multi-language or keyed fields.

## Operators

Common operators: `EQUAL`, `NOT_EQUAL`, `GREATER`, `LOWER`, `Is Null`, etc. Use the operator string as returned in responses (e.g. `=`, `>`, `<` for display; API may accept both).

## Multi-Language Fields (Secondary Tables)

For fields in secondary name/label tables (e.g. `SECURITY_NAME`, `DATACONTROL_NAME`), use `keys` to select the row:

```json
{
  "className": "MxDataControl",
  "field": "NAME",
  "label": "Name",
  "keys": [
    {"field": "LANGUAGE", "operator": "EQUAL", "value": "English"}
  ]
}
```

Use `"0"` for English, `"1"` for French when `"English"` is not supported.

## Secondary Table Fields (Child Tables)

Fields from child tables (e.g. `DATACONTROL_CLAUSES`, `DATACONTROL_NAME`) are requested with the **parent** `className`. For one-to-many children, the API returns one row per child (parent fields repeated).

**MxDataControl** – include clause fields:

```json
{"className": "MxDataControl", "field": "ASSESSED_DATA", "label": "AssessedData"},
{"className": "MxDataControl", "field": "CLAUSE_OPERATOR", "label": "ClauseOperator"},
{"className": "MxDataControl", "field": "TARGET_DATA", "label": "TargetData"},
{"className": "MxDataControl", "field": "EVALUATE_ORDER", "label": "EvaluateOrder"},
{"className": "MxDataControl", "field": "PARENTHESIS_OPEN", "label": "ParenthesisOpen"},
{"className": "MxDataControl", "field": "PARENTHESIS_CLOSE", "label": "ParenthesisClose"},
{"className": "MxDataControl", "field": "PARENTHESIS_OPERATOR", "label": "ParenthesisOperator"},
{"className": "MxDataControl", "field": "LABEL", "label": "ClauseLabel"},
{"className": "MxDataControl", "field": "CONTROL_GROUP", "label": "ControlGroup"}
```

## Response Format

```json
{
  "total": 15,
  "elapsedTime": 24,
  "content": [
    {
      "id": 526,
      "version": 5,
      "update_date": "2026-02-27",
      "ref": [],
      "fields": {
        "Code": "CONTROL_21/01/2026_17:38:10",
        "Name": "Business Entities - Domiciliation",
        "AssessedData": {"id": 1070, "value": "Value of Country (Dom)", "ref": []},
        "ClauseOperator": "=",
        "TargetData": {"id": 1069, "value": "Value of Country (Address)", "ref": []}
      }
    }
  ]
}
```

- **total**: Total matching records.
- **content**: Array of results. Each has `id`, `version`, `update_date`, `ref`, and `fields` (requested field values).
- Reference fields return `{id, value, ref}`.

## Searchable Classes

**Any class existing in the DataHub database** can be searched. Use the SmartClass name as `className` (e.g. `MxDataControl`, `MxSecurity`, `MxWorkflow`, `MxControlClauseData`, `MxClassDef`, `MxList`, etc.).

Some classes may not support all fields (e.g. `NAME` with keys). Use `CODE` and `LABEL` when richer fields fail.

## cURL Example

```bash
curl -s -X POST "http://nxdh-docker-product/smartservicegate/resources/search" \
  -H "Content-Type: application/json" \
  -u "lf.guimaraes:" \
  -d '{
    "from": [{"className": "MxDataControl", "type": "data"}],
    "where": {"logicalOperator": "AND", "criteria": [{"className": "MxDataControl", "field": "CODE", "operator": "EQUAL", "value": "EQUITY_NEG_PRICE_CHECK_V4"}]},
    "fields": [
      {"className": "MxDataControl", "field": "CODE", "label": "Code"},
      {"className": "MxDataControl", "field": "NAME", "label": "Name", "keys": [{"field": "LANGUAGE", "operator": "EQUAL", "value": "English"}]},
      {"className": "MxDataControl", "field": "ASSESSED_DATA", "label": "AssessedData"},
      {"className": "MxDataControl", "field": "CLAUSE_OPERATOR", "label": "ClauseOperator"},
      {"className": "MxDataControl", "field": "TARGET_DATA", "label": "TargetData"}
    ]
  }'
```

## Python Example

```python
import json
import requests

def load_config():
    with open(".datahub-workspace.json", encoding="utf-8") as f:
        return json.load(f)["datahub"]

def search_datahub(className, criteria=None, fields=None):
    config = load_config()
    url = f"{config['url'].rstrip('/')}/smartservicegate/resources/search"
    auth = (config["username"], config.get("password", ""))
    payload = {
        "from": [{"className": className, "type": "data"}],
        "where": {"logicalOperator": "AND", "criteria": criteria or []},
        "fields": fields or [{"className": className, "field": "CODE", "label": "Code"}],
    }
    r = requests.post(url, json=payload, auth=auth, timeout=60)
    r.raise_for_status()
    return r.json()

# Example: get all controls
result = search_datahub("MxDataControl", fields=[
    {"className": "MxDataControl", "field": "CODE", "label": "Code"},
    {"className": "MxDataControl", "field": "NAME", "label": "Name", "keys": [{"field": "LANGUAGE", "operator": "EQUAL", "value": "0"}]},
])
print(f"Found {result['total']} controls")
for item in result["content"]:
    print(item["fields"])
```

## Notes

- **Pagination**: The API may return a default limit (e.g. 10) even when `total` is higher. `offset`/`limit` may not be supported on all deployments.
- **getObjectPackage**: For full object export (including all children), use getObjectPackage. The search API returns flattened/selected fields only.
- **Authentication**: Empty password may work in some environments; otherwise set `password` in `.datahub-workspace.json`.
