#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""Regenerate the auto-maintained sections of README.md.

The README delimits generated regions with HTML comments:

    <!-- BEGIN GENERATED: <name> -->
    ...generated content...
    <!-- END GENERATED: <name> -->

Each region is rebuilt from the repo's source-of-truth files
(.claude-plugin/marketplace.json, sources.json and the plugins/ tree) so the
docs never drift. `make docs` writes the result; `make docs-check` fails when
the committed README is stale.

Usage:
    python3 scripts/gen_docs.py            # rewrite README.md in place
    python3 scripts/gen_docs.py --check    # exit 1 if README.md is stale
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
MARKETPLACE = ROOT / ".claude-plugin" / "marketplace.json"
SOURCES = ROOT / "sources.json"


def cell(text: str) -> str:
    """Escape a value for use inside a Markdown table cell."""
    return text.replace("|", "\\|")


def repo_slug(url: str) -> str:
    """https://github.com/owner/name.git -> owner/name"""
    return re.sub(r"^https?://github\.com/|\.git$", "", url)


def build_regions() -> dict[str, str]:
    plugins = json.loads(MARKETPLACE.read_text())["plugins"]
    skills = json.loads(SOURCES.read_text())["skills"]

    # Total MCP servers declared across every plugins/*/.mcp.json
    mcp_count = sum(
        len(json.loads(f.read_text()).get("mcpServers", {}))
        for f in sorted(ROOT.glob("plugins/*/.mcp.json"))
    )

    # count line
    count = f"{len(plugins)} toolkits bundling **{len(skills)} skills**"
    if mcp_count:
        noun = "MCP server" if mcp_count == 1 else "MCP servers"
        count += f" and **{mcp_count} {noun}**"
    count += ":"

    # `<toolkit>` list
    toolkit_list = (
        "`<toolkit>` is one of "
        + ", ".join(f"`{p['name']}`" for p in plugins)
        + "."
    )

    # What's inside table
    inside = ["| Toolkit | Description |", "| --- | --- |"]
    for p in plugins:
        name = p["name"]
        inside.append(f"| [`{name}`](plugins/{name}) | {cell(p['description'])} |")

    # Upstream sources table: skills grouped by repo, repos in first-appearance
    # order, locally-authored skills (no upstream) last.
    by_repo: dict[str | None, list[str]] = {}
    url_of: dict[str, str] = {}
    for skill, spec in skills.items():
        url = spec.get("repo")
        key = repo_slug(url) if url else None
        by_repo.setdefault(key, []).append(skill)
        if url:
            url_of[key] = url
    ordered = [k for k in by_repo if k is not None]
    if None in by_repo:
        ordered.append(None)

    upstream = ["| Skill | Upstream |", "| --- | --- |"]
    for key in ordered:
        names = ", ".join(by_repo[key])
        if key is None:
            src = "_local — no upstream_"
        else:
            src = f"[{key}]({url_of[key].removesuffix('.git')})"
        upstream.append(f"| {cell(names)} | {src} |")

    return {
        "count": count,
        "toolkit-list": toolkit_list,
        "whats-inside": "\n".join(inside),
        "upstream": "\n".join(upstream),
    }


def render(text: str, regions: dict[str, str]) -> str:
    for name, content in regions.items():
        marker = re.compile(
            r"(<!-- BEGIN GENERATED: " + re.escape(name) + r" -->\n)"
            r".*?"
            r"(\n<!-- END GENERATED: " + re.escape(name) + r" -->)",
            re.DOTALL,
        )
        if not marker.search(text):
            sys.exit(f"error: README.md has no '{name}' generated region")
        text = marker.sub(lambda m: m.group(1) + content + m.group(2), text)
    return text


def main() -> int:
    check = "--check" in sys.argv[1:]
    current = README.read_text()
    updated = render(current, build_regions())

    if current == updated:
        print("README.md generated sections are up to date.")
        return 0
    if check:
        print("README.md is out of date — run `make docs` and commit.")
        return 1
    README.write_text(updated)
    print("README.md regenerated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
