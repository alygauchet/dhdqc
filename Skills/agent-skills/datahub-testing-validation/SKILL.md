---
name: datahub-testing-validation
description: Validates IMPACT syntax, tests pack imports, and runs smoke tests after installation. Use when testing packs, validating IMPACT code, or running smoke tests after install.
---

# DataHub Testing & Validation

## MCP Tools Used

- **user-br-knowledge**: `validate_impact_syntax` — Validates IMPACT code or .pack file; returns errors and warnings (unknown functions, forbidden syntax).

## IMPACT Syntax Validation

Before deploying business rules:

1. Call `validate_impact_syntax` from br-knowledge MCP with the IMPACT code or .pack file
2. Fix any reported errors (unknown functions, forbidden syntax)
3. Re-validate until clean

See **datahub-business-rules** skill for full br-knowledge workflow (get_br_context → generate code → validate_impact_syntax).

## Pack Import Test Flow

1. Install the pack using **datahub-pack-installation** skill (MCP install_datahub_package)
2. Verify in DataHub: navigate to the object URL displayed after installation
3. Confirm object appears correctly and dependencies are satisfied
4. For workflow packs: create a run and verify step transitions
5. For list modifications: verify new items appear in the list

## Smoke Test Checklist

After installing a pack:

- [ ] Object is visible in DataHub UI
- [ ] No import errors in DataHub logs
- [ ] For business rules: validate IMPACT syntax before and after changes
- [ ] For workflows: test run creation and step progression
- [ ] For lists: verify items and labels display correctly

## Related Skills

- **datahub-pack-installation** — Install packs before testing
- **datahub-business-rules** — IMPACT validation via br-knowledge MCP
