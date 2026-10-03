# Structured Data Schema

Use UTF-8 JSON Lines (`.jsonl`) for deterministic processing. CSV is acceptable for human editing but should be normalized before rule application.

## Canonical Role Record

```json
{
  "role_id": "stable-id-or-derived-id",
  "group": "parent group",
  "unit": "hiring unit",
  "program": "campus or talent program",
  "cohort": "official cohort or null",
  "title": "exact official title",
  "category": "official category or null",
  "degree": "official degree text or null",
  "majors": "official major text or null",
  "location": "official location text or null",
  "url": "official role or lookup URL",
  "status": "open/closed/unknown",
  "duties": "official text or null",
  "requirements": "official text or null",
  "source_url": "official inventory URL",
  "accessed_at": "YYYY-MM-DD",
  "read_state": "disclosed/not-disclosed/not-read",
  "source_record": {}
}
```

`role_id` must be unique within the snapshot. If no official ID exists, derive a stable ID from unit, exact title, location, and program, and label it as derived in `source_record`.

## Decision Record

```json
{
  "role_id": "...",
  "stage": "filter4",
  "decision": "keep/remove/review",
  "rule_id": "F4-USER-001",
  "reason": "User-excluded city",
  "evidence_fields": ["location"],
  "origin": "user-rule",
  "decided_at": "YYYY-MM-DD"
}
```

Allowed origins:

- `official-hard-condition`;
- `skill-rule`;
- `user-rule`;
- `user-manual`;
- `analyst-inference`.

## Filter Rule File

```json
{
  "stage": "filter4",
  "rules": [
    {
      "id": "F4-USER-001",
      "action": "remove",
      "reason": "User-excluded city",
      "origin": "user-rule",
      "conditions": [
        {"field": "location", "operator": "contains", "value": "Example City"}
      ]
    }
  ]
}
```

Conditions in one rule are combined with AND. Supported operators in `apply_filter_rules.py`:

- `equals`, `not_equals`;
- `contains`, `not_contains`;
- `regex`;
- `in`;
- `missing`, `present`.

Default decision is `keep`. Use `review` instead of `remove` for missing or ambiguous evidence.
When several rules match, `remove` takes precedence over `review`, which takes precedence over `keep`; a `keep` rule is therefore descriptive and does not protect a record from a matching removal rule.

## File Invariants

- input IDs are unique;
- keep, remove, and review are mutually exclusive;
- their union equals the parent input IDs;
- every removed or reviewed record has at least one decision record;
- every stage records access date and source scope in its accompanying report.
