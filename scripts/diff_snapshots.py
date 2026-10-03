#!/usr/bin/env python3
"""Compare canonical recruitment snapshots by role_id."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")


DEFAULT_FIELDS = (
    "group", "unit", "program", "cohort", "title", "category", "degree",
    "majors", "location", "url", "status", "duties", "requirements",
)


def read_jsonl(path: Path) -> dict[str, dict[str, Any]]:
    result = {}
    with path.open("r", encoding="utf-8-sig") as handle:
        for line_no, line in enumerate(handle, 1):
            if not line.strip():
                continue
            record = json.loads(line)
            role_id = record.get("role_id")
            if not role_id:
                raise ValueError(f"{path}:{line_no} has no role_id")
            role_id = str(role_id)
            if role_id in result:
                raise ValueError(f"Duplicate role_id in {path}: {role_id}")
            result[role_id] = record
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("old", type=Path)
    parser.add_argument("new", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--fields", nargs="+", default=list(DEFAULT_FIELDS))
    args = parser.parse_args()

    old = read_jsonl(args.old)
    new = read_jsonl(args.new)
    added = sorted(set(new) - set(old))
    removed = sorted(set(old) - set(new))
    changed = []
    for role_id in sorted(set(old) & set(new)):
        changes = {
            field: {"old": old[role_id].get(field), "new": new[role_id].get(field)}
            for field in args.fields
            if old[role_id].get(field) != new[role_id].get(field)
        }
        if changes:
            changed.append({"role_id": role_id, "changes": changes})

    result = {
        "old_count": len(old),
        "new_count": len(new),
        "added": added,
        "removed": removed,
        "changed": changed,
    }
    payload = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload + "\n", encoding="utf-8")
    print(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
