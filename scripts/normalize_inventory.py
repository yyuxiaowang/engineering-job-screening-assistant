#!/usr/bin/env python3
"""Normalize CSV, JSON, or JSONL recruitment records into canonical JSONL."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Iterable


# Escaped aliases preserve Chinese-language headers in ASCII source.
ALIASES = {
    "role_id": ["role_id", "job_id", "position_id", "\u804c\u4f4d\u7f16\u53f7", "\u5c97\u4f4d\u7f16\u53f7"],
    "group": ["group", "\u96c6\u56e2", "\u62db\u8058\u96c6\u56e2"],
    "unit": ["unit", "company", "\u5355\u4f4d", "\u62db\u8058\u5355\u4f4d", "\u516c\u53f8"],
    "program": ["program", "\u62db\u8058\u9879\u76ee", "\u9879\u76ee"],
    "cohort": ["cohort", "\u5c4a\u522b", "\u6bd5\u4e1a\u5c4a\u522b"],
    "title": ["title", "job_title", "\u5c97\u4f4d\u540d\u79f0", "\u804c\u4f4d\u540d\u79f0"],
    "category": ["category", "\u804c\u4f4d\u7c7b\u522b", "\u5c97\u4f4d\u7c7b\u522b"],
    "degree": ["degree", "\u5b66\u5386", "\u5b66\u5386\u8981\u6c42"],
    "majors": ["majors", "major", "\u4e13\u4e1a", "\u4e13\u4e1a\u8981\u6c42"],
    "location": ["location", "city", "\u5730\u70b9", "\u5de5\u4f5c\u5730\u70b9", "\u57ce\u5e02"],
    "url": ["url", "job_url", "\u804c\u4f4d\u94fe\u63a5", "\u5c97\u4f4d\u94fe\u63a5"],
    "status": ["status", "\u62db\u8058\u72b6\u6001", "\u72b6\u6001"],
    "duties": ["duties", "responsibilities", "\u5c97\u4f4d\u804c\u8d23", "\u5de5\u4f5c\u804c\u8d23"],
    "requirements": ["requirements", "qualifications", "\u4efb\u804c\u8981\u6c42", "\u4efb\u804c\u6761\u4ef6"],
    "source_url": ["source_url", "list_url", "\u6765\u6e90\u94fe\u63a5", "\u62db\u8058\u5165\u53e3"],
    "accessed_at": ["accessed_at", "\u91c7\u96c6\u65e5\u671f", "\u8bbf\u95ee\u65e5\u671f"],
}

CANONICAL_FIELDS = tuple(ALIASES)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")


def compact(value: Any) -> Any:
    if value is None:
        return None
    if isinstance(value, str):
        value = re.sub(r"\s+", " ", value).strip()
        return value or None
    return value


def read_records(path: Path) -> list[dict[str, Any]]:
    suffix = path.suffix.lower()
    if suffix == ".csv":
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            return [dict(row) for row in csv.DictReader(handle)]
    if suffix == ".jsonl":
        records = []
        with path.open("r", encoding="utf-8-sig") as handle:
            for line_no, line in enumerate(handle, 1):
                if line.strip():
                    item = json.loads(line)
                    if not isinstance(item, dict):
                        raise ValueError(f"Line {line_no} is not an object")
                    records.append(item)
        return records
    if suffix == ".json":
        data = json.loads(path.read_text(encoding="utf-8-sig"))
        if isinstance(data, dict) and isinstance(data.get("roles"), list):
            data = data["roles"]
        if not isinstance(data, list) or not all(isinstance(item, dict) for item in data):
            raise ValueError("JSON input must be a list of objects or {'roles': [...]} ")
        return data
    raise ValueError("Input must use .csv, .json, or .jsonl")


def load_mapping(path: Path | None) -> dict[str, list[str]]:
    mapping = {key: list(values) for key, values in ALIASES.items()}
    if path is None:
        return mapping
    custom = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(custom, dict):
        raise ValueError("Mapping must be a JSON object")
    for key, values in custom.items():
        if key not in mapping:
            raise ValueError(f"Unknown canonical field in mapping: {key}")
        mapping[key] = [values] if isinstance(values, str) else list(values)
    return mapping


def first_value(record: dict[str, Any], aliases: Iterable[str]) -> Any:
    for key in aliases:
        if key in record and compact(record[key]) is not None:
            return compact(record[key])
    return None


def derived_id(record: dict[str, Any]) -> str:
    basis = "|".join(
        str(record.get(field) or "")
        for field in ("group", "unit", "program", "title", "location")
    )
    return "derived-" + hashlib.sha1(basis.encode("utf-8")).hexdigest()[:16]


def normalize(record: dict[str, Any], mapping: dict[str, list[str]]) -> dict[str, Any]:
    result = {field: first_value(record, mapping[field]) for field in CANONICAL_FIELDS}
    if not result["title"]:
        raise ValueError("Every record must contain a role title")
    id_is_derived = not bool(result["role_id"])
    if id_is_derived:
        result["role_id"] = derived_id(result)
    disclosed = any(result[field] for field in ("duties", "requirements", "majors", "degree"))
    result["read_state"] = "disclosed" if disclosed else "not-read"
    result["source_record"] = {"id_is_derived": id_is_derived, "raw": record}
    return result


def write_jsonl(path: Path, records: Iterable[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--mapping", type=Path, help="Optional canonical-field mapping JSON")
    args = parser.parse_args()

    mapping = load_mapping(args.mapping)
    normalized = [normalize(record, mapping) for record in read_records(args.input)]
    ids = [record["role_id"] for record in normalized]
    duplicates = sorted(role_id for role_id, count in Counter(ids).items() if count > 1)
    if duplicates:
        raise ValueError(f"Duplicate role IDs after normalization: {duplicates[:10]}")
    write_jsonl(args.output, normalized)
    print(json.dumps({"input": len(normalized), "output": str(args.output)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
