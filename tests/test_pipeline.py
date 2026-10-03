from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"


def run_script(name: str, *args: object) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPTS / name), *(str(arg) for arg in args)],
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )


class PipelineTest(unittest.TestCase):
    def test_chinese_header_compatibility(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            source = Path(temp_dir) / "roles.json"
            output = Path(temp_dir) / "normalized.jsonl"
            source.write_text(json.dumps([{
                "\u5c97\u4f4d\u7f16\u53f7": "1",
                "\u804c\u4f4d\u540d\u79f0": "Research Engineer",
                "\u5de5\u4f5c\u5730\u70b9": "Example City",
                "\u4e13\u4e1a\u8981\u6c42": "Mechanical Engineering",
            }]), encoding="utf-8")
            result = run_script("normalize_inventory.py", source, output)
            self.assertEqual(result.returncode, 0, result.stderr)
            record = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(record["role_id"], "1")
            self.assertEqual(record["title"], "Research Engineer")
            self.assertEqual(record["location"], "Example City")
            self.assertEqual(record["majors"], "Mechanical Engineering")

    def test_normalize_filter_validate_and_diff(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp = Path(temp_dir)
            source = temp / "roles.json"
            normalized = temp / "parent.jsonl"
            rules = temp / "rules.json"
            kept = temp / "kept.jsonl"
            removed = temp / "removed.jsonl"
            review = temp / "review.jsonl"
            decisions = temp / "decisions.jsonl"

            source.write_text(json.dumps([
                {"job_id": "1", "job_title": "Materials Research Engineer", "city": "City A", "major": "Materials Science and Engineering"},
                {"job_id": "2", "job_title": "Finance Specialist", "city": "City A", "major": "Accounting"},
                {"job_id": "3", "job_title": "Systems Engineer", "city": "Example City", "major": "Mechanical Engineering"},
                {"job_id": "4", "job_title": "Algorithm Researcher", "city": "City B"},
            ], ensure_ascii=False), encoding="utf-8")

            result = run_script("normalize_inventory.py", source, normalized)
            self.assertEqual(result.returncode, 0, result.stderr)

            rules.write_text(json.dumps({
                "stage": "filter4",
                "rules": [
                    {
                        "id": "R1", "action": "remove", "reason": "Nontechnical title", "origin": "skill-rule",
                        "conditions": [{"field": "title", "operator": "contains", "value": "Finance"}],
                    },
                    {
                        "id": "R2", "action": "remove", "reason": "User-excluded city", "origin": "user-rule",
                        "conditions": [{"field": "location", "operator": "equals", "value": "Example City"}],
                    },
                    {
                        "id": "R3", "action": "review", "reason": "Major not disclosed", "origin": "skill-rule",
                        "conditions": [{"field": "majors", "operator": "missing"}],
                    },
                ],
            }, ensure_ascii=False), encoding="utf-8")

            result = run_script(
                "apply_filter_rules.py", normalized, rules,
                "--kept", kept, "--removed", removed, "--review", review, "--decisions", decisions,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            summary = json.loads(result.stdout)
            self.assertEqual(summary["keep"], 1)
            self.assertEqual(summary["remove"], 2)
            self.assertEqual(summary["review"], 1)

            result = run_script(
                "validate_funnel.py", normalized,
                "--kept", kept, "--removed", removed, "--review", review, "--decisions", decisions,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertTrue(json.loads(result.stdout)["valid"])

            newer = temp / "newer.jsonl"
            records = [json.loads(line) for line in normalized.read_text(encoding="utf-8").splitlines()]
            records[0]["location"] = "City B"
            records.append({"role_id": "5", "title": "New Role"})
            newer.write_text("\n".join(json.dumps(record, ensure_ascii=False) for record in records) + "\n", encoding="utf-8")
            result = run_script("diff_snapshots.py", normalized, newer)
            self.assertEqual(result.returncode, 0, result.stderr)
            diff = json.loads(result.stdout)
            self.assertEqual(diff["added"], ["5"])
            self.assertEqual(diff["changed"][0]["role_id"], "1")


if __name__ == "__main__":
    unittest.main()
