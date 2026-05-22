#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""Re-vendor skills from their upstream repositories.

Reads sources.json, shallow-clones each upstream repo once, and copies every
skill's subdirectory into plugins/<plugin>/skills/<name>/. Skills marked
"source": "local" have no upstream and are left untouched.

Usage:
    python3 scripts/sync.py            # sync every upstream skill
    python3 scripts/sync.py NAME ...   # sync only the named skills
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCES = ROOT / "sources.json"


def git(*args: str) -> str:
    """Run a git command, returning stdout; raises on non-zero exit."""
    return subprocess.run(
        ["git", *args], check=True, capture_output=True, text=True
    ).stdout.strip()


def main() -> int:
    skills = json.loads(SOURCES.read_text())["skills"]
    wanted = set(sys.argv[1:])

    remote = {
        name: spec
        for name, spec in skills.items()
        if spec.get("repo") and (not wanted or name in wanted)
    }
    if not remote:
        print("Nothing to sync.")
        return 0

    # One clone per (repo, ref); a repo may supply several skills.
    groups: dict[tuple[str, str], list[tuple[str, dict]]] = {}
    for name, spec in remote.items():
        key = (spec["repo"], spec.get("ref", "main"))
        groups.setdefault(key, []).append((name, spec))

    synced: list[str] = []
    failed: list[str] = []

    for (repo, ref), items in groups.items():
        print(f"\n== {repo} @ {ref} ==")
        try:
            with tempfile.TemporaryDirectory() as tmp:
                git("clone", "--depth", "1", "--branch", ref,
                    "--filter=blob:none", "--sparse", repo, tmp)
                git("-C", tmp, "sparse-checkout", "set",
                    *[spec["path"] for _, spec in items])
                sha = git("-C", tmp, "rev-parse", "HEAD")
                print(f"   commit {sha[:12]}")
                for name, spec in items:
                    src = Path(tmp) / spec["path"]
                    if not (src / "SKILL.md").is_file():
                        print(f"   SKIP {name}: no SKILL.md at {spec['path']}")
                        failed.append(name)
                        continue
                    dst = ROOT / "plugins" / spec["plugin"] / "skills" / name
                    try:
                        shutil.rmtree(dst, ignore_errors=True)
                        # ignore_dangling_symlinks: some upstreams ship skills
                        # with broken symlinks (data/scripts assembled by a CLI).
                        shutil.copytree(src, dst, ignore_dangling_symlinks=True)
                    except (OSError, shutil.Error) as exc:
                        print(f"   FAIL {name}: {exc}")
                        failed.append(name)
                        continue
                    print(f"   OK   {name} -> {spec['plugin']}")
                    synced.append(name)
        except subprocess.CalledProcessError as exc:
            detail = (exc.stderr or "").strip() or exc
            print(f"   FAIL {repo}: {detail}")
            failed.extend(name for name, _ in items)

    local = sorted(n for n, s in skills.items() if not s.get("repo"))
    print(f"\nSynced {len(synced)} skill(s).")
    if local:
        print(f"Local-only, untouched: {', '.join(local)}")
    if failed:
        print(f"FAILED: {', '.join(sorted(set(failed)))}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
