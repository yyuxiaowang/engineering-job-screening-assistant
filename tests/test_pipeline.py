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
                {"岗位编号": "1", "职位名称": "材料研究工程师", "工作地点": "城市甲", "专业要求": "材料科学与工程"},
                {"岗位编号": "2", "职位名称": "财务专员", "工作地点": "城市甲", "专业要求": "会计"},
                {"岗位编号": "3", "职位名称": "系统工程师", "工作地点": "示例城市", "专业要求": "机械工程"},
                {"岗位编号": "4", "职位名称": "算法研究员", "工作地点": "城市乙"},
            ], ensure_ascii=False), encoding="utf-8")

            result = run_script("normalize_inventory.py", source, normalized)
            self.assertEqual(result.returncode, 0, result.stderr)

            rules.write_text(json.dumps({
                "stage": "filter4",
                "rules": [
                    {
                        "id": "R1", "action": "remove", "reason": "Nontechnical title", "origin": "skill-rule",
                        "conditions": [{"field": "title", "operator": "contains", "value": "财务"}],
                    },
                    {
                        "id": "R2", "action": "remove", "reason": "User-excluded city", "origin": "user-rule",
                        "conditions": [{"field": "location", "operator": "equals", "value": "示例城市"}],
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
            records[0]["location"] = "城市乙"
            records.append({"role_id": "5", "title": "新增岗位"})
            newer.write_text("\n".join(json.dumps(record, ensure_ascii=False) for record in records) + "\n", encoding="utf-8")
            result = run_script("diff_snapshots.py", normalized, newer)
            self.assertEqual(result.returncode, 0, result.stderr)
            diff = json.loads(result.stdout)
            self.assertEqual(diff["added"], ["5"])
            self.assertEqual(diff["changed"][0]["role_id"], "1")


if __name__ == "__main__":
    unittest.main()
