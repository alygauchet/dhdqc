#!/usr/bin/env python3
"""
Merge DataHub MCP server entry into an MCP client JSON file from .datahub-workspace.json.

Default target is ~/.cursor/mcp.json (Cursor).
Use --claude-code to target {repo}/.mcp.json (Claude Code / VSCode).
Use --mcp-json for any other client.

Server key: datahub-mcp-dev-{workspace.projectName}
Preserves all other mcpServers entries.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from pathlib import Path


_WINDOWS_STORE_STUB_DIR = os.path.join("WindowsApps", "python")


def _is_windows_store_stub(path: str) -> bool:
    """Return True if the path is a Windows Store Python stub (not a real interpreter)."""
    return "WindowsApps" in path and "python" in os.path.basename(path).lower()


def _resolve_python() -> str:
    for cmd in ("python3.11", "python3.12", "python3", "python"):
        p = shutil.which(cmd)
        if p and not _is_windows_store_stub(p):
            return p
    return "python3"


def _resolve_uv() -> str | None:
    return shutil.which("uv")


def _read_json(path: Path) -> dict:
    if not path.is_file():
        return {}
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
        f.write("\n")


def build_entry(workspace: dict, python_exe: str | None) -> tuple[str, dict]:
    dh = workspace["datahub"]
    ws = workspace["workspace"]

    base = Path(ws["centralizedFolder"]).expanduser().resolve()
    rel = Path(ws["mcpCentralizedFolder"])
    mcp_root = (base / rel).resolve()

    script = mcp_root / "mcp-datahub-server" / "mcp_datahub_server.py"
    if not script.is_file():
        raise FileNotFoundError(f"MCP script not found: {script}")

    url = dh["url"].rstrip("/")
    install_ep = dh.get("packageInstallEndpoint", "/smartservicegate/services/Packages/install")
    get_ep = dh.get(
        "getObjectPackageEndpoint",
        "/smartservicegate/services/Packages/getObjectPackage",
    )
    if not str(install_ep).startswith("/"):
        install_ep = "/" + str(install_ep)
    if not str(get_ep).startswith("/"):
        get_ep = "/" + str(get_ep)

    server_key = f"datahub-mcp-dev-{ws['projectName']}"

    env = {
        "DATAHUB_ENDPOINT_INSTALL": url + str(install_ep),
        "DATAHUB_ENDPOINT_GET_OBJECT": url + str(get_ep),
        "DATAHUB_USERNAME": str(dh.get("username", "")),
        "DATAHUB_PASSWORD": str(dh.get("password", "")),
    }

    uv = python_exe is None and _resolve_uv()
    if uv:
        entry = {
            "command": uv,
            "args": [
                "run",
                "--with", "mcp>=1.0.0",
                "--with", "httpx>=0.27.0",
                str(script),
            ],
            "cwd": str(mcp_root / "mcp-datahub-server"),
            "env": env,
        }
    else:
        py = python_exe or os.environ.get("PYTHON_FOR_MCP") or _resolve_python()
        entry = {
            "command": py,
            "args": [str(script)],
            "cwd": str(mcp_root / "mcp-datahub-server"),
            "env": env,
        }

    return server_key, entry


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Add or update datahub-mcp-dev-<projectName> in MCP client mcp.json from .datahub-workspace.json"
    )
    parser.add_argument(
        "--workspace",
        type=Path,
        default=None,
        help="Path to .datahub-workspace.json (default: <repo>/.datahub-workspace.json)",
    )
    parser.add_argument(
        "--repo",
        type=Path,
        default=None,
        help="Project root containing .datahub-workspace.json (default: current directory)",
    )
    parser.add_argument(
        "--mcp-json",
        type=Path,
        default=None,
        help="Path to MCP client config. Default: ~/.cursor/mcp.json, or {repo}/.mcp.json when --claude-code is set.",
    )
    parser.add_argument(
        "--claude-code",
        action="store_true",
        help="Write to {repo}/.mcp.json (Claude Code / VSCode) instead of ~/.cursor/mcp.json.",
    )
    parser.add_argument(
        "--python",
        default=None,
        help="Python executable for MCP command. If omitted, uv is preferred when available (skips Windows Store stubs).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the server key and entry JSON, do not write",
    )
    args = parser.parse_args()

    repo = args.repo.resolve() if args.repo else Path.cwd().resolve()
    ws_path = args.workspace
    if ws_path is None:
        ws_path = repo / ".datahub-workspace.json"
    else:
        ws_path = ws_path.resolve()

    if args.mcp_json is not None:
        mcp_json_path = args.mcp_json
    elif args.claude_code:
        mcp_json_path = repo / ".mcp.json"
    else:
        mcp_json_path = Path.home() / ".cursor" / "mcp.json"

    if not ws_path.is_file():
        print(f"Error: workspace file not found: {ws_path}", file=sys.stderr)
        return 1

    with open(ws_path, encoding="utf-8") as f:
        workspace = json.load(f)

    try:
        server_key, entry = build_entry(workspace, args.python)
    except (KeyError, FileNotFoundError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    if args.dry_run:
        print(server_key)
        print(json.dumps(entry, indent=2))
        return 0

    if args.claude_code and entry.get("env", {}).get("DATAHUB_PASSWORD"):
        print(
            "Warning: DATAHUB_PASSWORD is non-empty. "
            ".mcp.json may be committed to git — consider adding it to .gitignore.",
            file=sys.stderr,
        )

    mcp_path = mcp_json_path.expanduser().resolve()
    data = _read_json(mcp_path)
    if "mcpServers" not in data or not isinstance(data["mcpServers"], dict):
        data["mcpServers"] = {}

    data["mcpServers"][server_key] = entry
    _write_json(mcp_path, data)

    print(f"Updated {mcp_path}")
    print(f"Server key: {server_key}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
