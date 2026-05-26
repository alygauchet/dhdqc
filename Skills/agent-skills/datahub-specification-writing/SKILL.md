---
name: datahub-specification-writing
description: Writes functional specifications in Specification/ with goals, mermaid diagrams, and PROJECT_SPEC_ naming. Use when creating or updating specifications, user stories, or feature documentation.
---

# DataHub Specification Writing

## File Location

All specifications produced or updated by the assistant must be in **Specification/** folder.

**Project name**: Read `workspace.projectName` from `.datahub-workspace.json`. Use it for naming: each specification file must be named `{projectName}_SPEC_{FeatureName}.md` (e.g. `MyProject_SPEC_UserRegistration.md`). If `projectName` is missing, fall back to `PROJECT_SPEC_`.

## Specification Structure

- Include owner, version, and date headers
- Define goals and non-goals clearly
- Specify inputs, processing logic, and outputs
- Include error handling requirements
- Add performance considerations
- Document testing approach
- Reference deployment packages
- Use mermaid for designing schemas

## Markdown Standards

- Use clear headings hierarchy
- Include version numbers and dates in specifications
- Use code blocks with language identifiers
- Include mermaid diagrams where appropriate
- Follow the existing specification template structure

## Documentation Standards

- Keep specifications up-to-date with implementation
- Include version numbers and change dates
- Reference related specifications and user stories
- Use consistent terminology from the domain model
