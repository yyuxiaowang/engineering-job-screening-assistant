#!/usr/bin/env python3
"""Apply auditable AND-condition rules to canonical recruitment JSONL."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path
from typing import Any, Iterable


VALID_ACTIONS = {"keep", "remove", "review"}
PRECEDENCE = {"keep": 0, "review": 1, "remove": 2}

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


def write_jsonl(path: Path, records: Iterable[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")


def is_missing(value: Any) -> bool:
    return value is None or value == "" or value == []


def text(value: Any, case_sensitive: bool) -> str:
    result = "" if value is None else str(value)
    return result if case_sensitive else result.casefold()


def condition_matches(record: dict[str, Any], condition: dict[str, Any]) -> bool:
    field = condition.get("field")
    operator = condition.get("operator")
    expected = condition.get("value")
    case_sensitive = bool(condition.get("case_sensitive", False))
    actual = record.get(field)

    if operator == "missing":
        return is_missing(actual)
    if operator == "present":
        return not is_missing(actual)

    actual_text = text(actual, case_sensitive)
    expected_text = text(expected, case_sensitive)
    if operator == "equals":
        return actual_text == expected_text
    if operator == "not_equals":
        return actual_text != expected_text
    if operator == "contains":
        return expected_text in actual_text
    if operator == "not_contains":
        return expected_text not in actual_text
    if operator == "regex":
        flags = 0 if case_sensitive else re.IGNORECASE
        return re.search(str(expected), "" if actual is None else str(actual), flags) is not None
    if operator == "in":
        if not isinstance(expected, list):
            raise ValueError("The 'in' operator requires a list value")
        choices = {text(item, case_sensitive) for item in expected}
        return actual_text in choices
    raise ValueError(f"Unsupported operator: {operator}")


def validate_rules(data: dict[str, Any]) -> list[dict[str, Any]]:
    rules = data.get("rules")
    if not isinstance(rules, list):
        raise ValueError("Rule file must contain a rules list")
    seen = set()
    for rule in rules:
        required = ("id", "action", "reason", "origin", "conditions")
        missing = [key for key in required if key not in rule]
        if missing:
            raise ValueError(f"Rule missing fields {missing}: {rule}")
        if rule["id"] in seen:
            raise ValueError(f"Duplicate rule ID: {rule['id']}")
        seen.add(rule["id"])
        if rule["action"] not in VALID_ACTIONS:
            raise ValueError(f"Invalid action in {rule['id']}: {rule['action']}")
        if not isinstance(rule["conditions"], list) or not rule["conditions"]:
            raise ValueError(f"Rule {rule['id']} needs at least one condition")
    return rules


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("rules", type=Path)
    parser.add_argument("--kept", type=Path, required=True)
    parser.add_argument("--removed", type=Path, required=True)
    parser.add_argument("--review", type=Path, required=True)
    parser.add_argument("--decisions", type=Path, required=True)
    args = parser.parse_args()

    records = read_jsonl(args.input)
    rule_data = json.loads(args.rules.read_text(encoding="utf-8-sig"))
    rules = validate_rules(rule_data)
    stage = rule_data.get("stage", "unspecified")

    buckets: dict[str, list[dict[str, Any]]] = {key: [] for key in VALID_ACTIONS}
    decisions = []
    for record in records:
        if not record.get("role_id"):
            raise ValueError("Every input record must have role_id")
        matches = [
            rule for rule in rules
            if all(condition_matches(record, condition) for condition in rule["conditions"])
        ]
        action = max((rule["action"] for rule in matches), key=PRECEDENCE.get, default="keep")
        buckets[action].append(record)
        for rule in matches:
            if rule["action"] == action and action != "keep":
                decisions.append({
                    "role_id": record["role_id"],
                    "stage": stage,
                    "decision": action,
                    "rule_id": rule["id"],
                    "reason": rule["reason"],
                    "evidence_fields": sorted({c["field"] for c in rule["conditions"]}),
                    "origin": rule["origin"],
                    "decided_at": date.today().isoformat(),
                })

    write_jsonl(args.kept, buckets["keep"])
    write_jsonl(args.removed, buckets["remove"])
    write_jsonl(args.review, buckets["review"])
    write_jsonl(args.decisions, decisions)
    print(json.dumps({
        "input": len(records),
        "keep": len(buckets["keep"]),
        "remove": len(buckets["remove"]),
        "review": len(buckets["review"]),
        "decisions": len(decisions),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
