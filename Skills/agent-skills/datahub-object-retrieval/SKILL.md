---
name: datahub-object-retrieval
description: Retrieves object packages from DataHub via getObjectPackage (prefer project DataHub MCP get_object_package; see datahub-mcp-project-setup). Use when fetching objects from DataHub, exporting packages, or when the user asks to get/retrieve an object.
---

# DataHub Object Retrieval

## MCP Tools Used

- **`get_object_package`** on the **DataHub MCP** server configured for this project (see **datahub-mcp-project-setup** — server key `datahub-mcp-dev-{projectName}`). The IDE or agent exposes MCP tools with a prefixed name that includes that server key. Use `class_name`, `object_code`, and optionally `save_path` (target directory; filename is enforced as `{class_name}_{object_code}.pack`).

**`object_code` shortcuts:** For **`MxBusinessField`**, hubs often accept the **plain internal `CODE`** as `object_code` when it is unique globally (e.g. **`ISIN`**, **`QUOTE_LAST`**, **`QUOTE_MID`**). If retrieval fails, fall back to the composite form **`[TECH_CLASS^CODE='[CLASS_NAME='MxSecurity']^…']`** from **`BUSINESSFIELD FIND=…`** in an existing pack or **`MxBusinessClass`** export.

## Retrieval workflow (MCP preferred)

1. Prefer the **`get_object_package`** MCP tool from the project’s DataHub server so endpoints and credentials match `.datahub-workspace.json` (via the MCP env/config).
2. Save retrieved packages under `Knowledge/Model/Objects/` (or `Implementation/Temp/` when appropriate), using `{ClassName}_{ObjectCode}.pack` naming.
3. Apply **CRITICAL** quote-handling rules below when persisting pack XML from API responses.

## Fallback: Direct API Call

When the DataHub MCP server is not available, use the direct SOAP API:

- **Endpoint**: `POST {datahub.url}/smartservicegate/services/Packages/getObjectPackage`
- **Authentication**: Basic auth with `{datahub.username}` and `{datahub.password}`

### Request body — SOAP (XML)

Use this shape for the standard HTTP call:

- **Content-Type**: `text/xml; charset=utf-8`
- **SOAPAction**: `urn:getObjectPackage`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsd="http://smart.ws.packages/xsd">
  <soapenv:Header/>
  <soapenv:Body>
    <xsd:getObjectPackage>
      <xsd:ObjectPackage>
        <xsd:Package>
          <xsd:ClassName>MxClassDef</xsd:ClassName>
          <xsd:ObjectCode>MxWorkflow</xsd:ObjectCode>
        </xsd:Package>
      </xsd:ObjectPackage>
    </xsd:getObjectPackage>
  </soapenv:Body>
</soapenv:Envelope>
```

Replace `ClassName` and `ObjectCode` as needed (e.g. `MxClassDef` / `MxWorkflow` for a class definition; `MxList` / `FEED` for a list; `MxClassDef` / `MxCalendar` for another class definition).

### Request body — JSON

The same **`POST {datahub.url}/smartservicegate/services/Packages/getObjectPackage`** endpoint often accepts JSON (verify on your deployment):

- **Content-Type**: `application/json`
- **Body**: `ObjectPackage` with a `Package` array; each element has `ClassName` and `ObjectCode`.

Example — list instance:

```json
{
  "ObjectPackage": {
    "Package": [
      {
        "ClassName": "MxList",
        "ObjectCode": "YES_NO"
      }
    ]
  }
}
```

Example — class definition (correct object code is **`MxCalendar`**, not `MsCalendar`):

```json
{
  "ObjectPackage": {
    "Package": [
      {
        "ClassName": "MxClassDef",
        "ObjectCode": "MxCalendar"
      }
    ]
  }
}
```

Use multiple entries in `Package` when the API supports batch export.

**Response (JSON)**: `PackageResult.Result.Status` (e.g. `OK`) and **`PackageResult.Result.Comment`**: the pack XML as a string. Parse JSON, then write `Comment` to a `.pack` file (UTF-8). See **CRITICAL** below for quote handling when normalizing exports.

**Response (SOAP)**: Pack XML is typically inside the SOAP body (e.g. `Comment`); decode `&lt;`/`&gt;` when needed when saving to `.pack`.

## Storage Locations

| Folder | Purpose |
|--------|---------|
| `Knowledge/Model/Objects/` | Primary storage for retrieved packages. Filenames: `{ClassName}_{ObjectCode}.pack` (e.g., `MxList_WF_STATUS.pack`). Overwrites if same object is retrieved again |
| `Implementation/Temp/` | Temporary storage when fetching. Remove packages already present in Knowledge/Model/Objects to avoid duplication |

## CRITICAL: Package Recovery from getObjectPackage API

When extracting a package from the getObjectPackage API response (JSON):

- **Replace** `\"` with `&quot;` in the extracted pack XML, **NOT** with raw `"` (double quote)
- **Why**: The API returns the pack in `PackageResult.Result.Comment` with JSON-escaped quotes (`\"`). Use XML entity `&quot;` so the pack matches DataHub manual export format and remains valid XML
- **Scope**: Replace in XML attribute values (e.g., CODE attributes). Do NOT replace quotes inside CDATA sections (CONDITION, DESCRIPTION, IMPACT, etc.)—those remain as literal content
- **Applies to**: Any script, tool, or process that fetches packages via getObjectPackage API and saves them to disk

## Related: Adding Items to Lists

When adding new items to an existing list (e.g. FEED), retrieve the list first via getObjectPackage to get the SMARTLIST attributes (`FIND`, `USER`, `UPDATE_DATE`, etc.) and item structure. Then use the **datahub-pack-creation-modification** skill for the two-package workflow (item first, then label).

## Configuration

Read from `.datahub-workspace.json`:

- **Endpoint**: `{datahub.getObjectPackageEndpoint}` (e.g., `/smartservicegate/services/Packages/getObjectPackage`)
- **Authentication**: Username `{datahub.username}`, Password `{datahub.password}`

For MCP retrieval, the project DataHub server should already map these via **datahub-mcp-project-setup** (`DATAHUB_ENDPOINT_GET_OBJECT`, `DATAHUB_USERNAME`, `DATAHUB_PASSWORD`). For direct HTTP calls, build the full URL from `{datahub.url}` and the endpoint path above.
