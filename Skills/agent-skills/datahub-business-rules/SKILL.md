---
name: datahub-business-rules
description: Writes DataHub SmartRule business rules with EXIT_0/EXIT_1, getListItemCode, foreach patterns. Use when writing SmartRule logic, business rules, status management, or validation logic. Use br-knowledge MCP for optimized, quality IMPACT code.
---

# DataHub Business Rules

## MCP Tools Used

- **user-br-knowledge**: `get_br_context`, `get_pack_template`, `validate_impact_syntax` — For optimized IMPACT code and syntax validation.

## IMPACT Variable Syntax

- **No `$` prefix** – variables are plain identifiers: `arg1`, `arg2`, `result`, `inputDate`, etc.
- **Assignment** – use `:=` not `=`: `result := dateadd(arg1, 7);`
- **Rule arguments** – passed as `arg1`, `arg2`, `arg3`, etc. (no `$arg1`)

## Error Handling Pattern

- Use `EXIT_0` for success with payload
- Use `EXIT_1` for errors with descriptive messages
- Validate inputs before processing
- Return `array("EXIT_1", "descriptive message")` on errors
- Return `array("EXIT_0", payload)` on success
- Validate inputs early in functions
- Provide actionable error messages

## Status Management

- Use `getListItemCode("WF_STATUS", status, 0)` to convert IDs to codes
- Check `IS_TEMPLATE = "N"` before processing runs
- Validate step prerequisites before status updates

## Iteration

- Iterate over relations using `foreach`

## Testing Considerations

- Test with real workflow runs, not just templates
- Validate edge cases (empty inputs, missing objects)

## br-knowledge MCP (Optimized & Quality Rules)

Full details on how to create optimized and quality business rules scripts can be enhanced using the resources available in the **br-knowledge** MCP server (`user-br-knowledge`). Use these tools proactively:

| Tool | When to Use |
|------|-------------|
| **get_br_context** | Before generating or correcting IMPACT code. Semantic search over grammar, functions, best practices, and BRUT standards. Pass a query (e.g. `"validation"`, `"error handling"`, `"hello world simple rule"`). Optionally filter by `type_filter`: `GRAMMAR`, `BEST_PRACTICES`, `BRUT_STANDARDS`, `PARAMETER_DOCS`, `OFFICIAL_GUIDE`, `GENERAL`. |
| **get_pack_template** | When creating a new Business Rule. Returns a minimal .pack XML skeleton; fill the IMPACT section with generated code. |
| **validate_impact_syntax** | After generating or modifying IMPACT code. Validates code or .pack file; returns errors and warnings (unknown functions, forbidden syntax). |

**Workflow**: Call `get_br_context` first to retrieve relevant knowledge → generate or correct IMPACT code → call `validate_impact_syntax` to ensure correctness.

## Notes

- Business rules use DataHub SmartRule language
- Workflow steps follow a state machine pattern
- Four-eyes validation adds an intermediate approval state
- Events drive step progression and dependencies
