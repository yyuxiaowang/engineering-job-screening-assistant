#!/usr/bin/env python3
"""Validate count, uniqueness, coverage, and decision invariants for one filter stage."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    records = []
    with path.open("r", encoding="utf-8-sig") as handle:
        for line_no, line in enumerate(handle, 1):
            if line.strip():
                item = json.loads(line)
                if not isinstance(item, dict):
                    raise ValueError(f"{path}:{line_no} is not an object")
                records.append(item)
    return records


def ids(records: list[dict[str, Any]], label: str) -> list[str]:
    result = []
    for index, record in enumerate(records, 1):
        role_id = record.get("role_id")
        if not role_id:
            raise ValueError(f"{label} record {index} has no role_id")
        result.append(str(role_id))
    return result


def duplicates(values: list[str]) -> list[str]:
    return sorted(key for key, count in Counter(values).items() if count > 1)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("parent", type=Path)
    parser.add_argument("--kept", type=Path, required=True)
    parser.add_argument("--removed", type=Path, required=True)
    parser.add_argument("--review", type=Path, required=True)
    parser.add_argument("--decisions", type=Path)
    args = parser.parse_args()

    datasets = {
        "parent": read_jsonl(args.parent),
        "kept": read_jsonl(args.kept),
        "removed": read_jsonl(args.removed),
        "review": read_jsonl(args.review),
    }
    id_lists = {label: ids(records, label) for label, records in datasets.items()}
    errors = []

    for label, values in id_lists.items():
        dupes = duplicates(values)
        if dupes:
            errors.append(f"duplicate IDs in {label}: {dupes[:10]}")

    parent = set(id_lists["parent"])
    child_sets = {label: set(id_lists[label]) for label in ("kept", "removed", "review")}
    labels = list(child_sets)
    for i, left in enumerate(labels):
        for right in labels[i + 1:]:
            overlap = sorted(child_sets[left] & child_sets[right])
            if overlap:
                errors.append(f"overlap between {left} and {right}: {overlap[:10]}")

    union = set().union(*child_sets.values())
    missing = sorted(parent - union)
    extra = sorted(union - parent)
    if missing:
        errors.append(f"parent IDs missing from outputs: {missing[:10]}")
    if extra:
        errors.append(f"output IDs absent from parent: {extra[:10]}")

    if len(id_lists["parent"]) != sum(len(id_lists[label]) for label in labels):
        errors.append("count invariant failed: input != kept + removed + review")

    if args.decisions:
        decision_records = read_jsonl(args.decisions)
        decision_ids = {str(record.get("role_id")) for record in decision_records if record.get("role_id")}
        needed = child_sets["removed"] | child_sets["review"]
        absent = sorted(needed - decision_ids)
        unexpected = sorted(decision_ids - needed)
        if absent:
            errors.append(f"removed/review IDs without decisions: {absent[:10]}")
        if unexpected:
            errors.append(f"decision IDs not removed/reviewed: {unexpected[:10]}")

    result = {
        "valid": not errors,
        "input": len(id_lists["parent"]),
        "kept": len(id_lists["kept"]),
        "removed": len(id_lists["removed"]),
        "review": len(id_lists["review"]),
        "errors": errors,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
