# DataHub Object Search Skill

## Importing in Another Workspace

To use this skill in a different workspace:

1. **Copy the skill folder** to the target workspace (canonical path in this template):
   ```
   Skills/agent-skills/datahub-object-search/
   ├── SKILL.md
   └── README.md
   ```
   If the target project uses Cursor, you can place the copy under `.cursor/skills/datahub-object-search/` instead.

2. **Or** copy to your personal Cursor skills (available in all projects):
   ```
   ~/.cursor/skills/datahub-object-search/
   ```

3. Ensure the target workspace has `.datahub-workspace.json` with `url`, `username`, and `password` for the DataHub connection.

## Prerequisites

- `.datahub-workspace.json` in the workspace root with DataHub connection config
- `requests` Python package if using the Python example
