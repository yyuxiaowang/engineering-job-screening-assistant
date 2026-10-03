# Reversible Bulk Filtering

## Stage Persistence and Confirmation

Every executed filter must save its complete retained, removed, and review sets plus the decision log. Include exact titles and stable role IDs when available; never save only counts or a final shortlist.

In `staged` mode:

1. run one filter only;
2. save all outputs and a stage summary;
3. report counts, principal rules, and artifact paths;
4. stop until the user confirms the next filter or changes the rules.

In `continuous` mode, run successive safe filters without routine confirmation, but create the same artifacts. Stop immediately when the next rule would depend on ambiguous titles or undisclosed fields.

## Filter 1: Complete Inventory

- Capture the user-confirmed recruitment projects and official filter state at a named access date.
- Preserve exact title, unit, role ID, location, visible eligibility, URL, and source.
- Do not merge identical titles with different IDs.
- Record portal and per-unit counts.
- Do not write fit conclusions into the raw inventory.
- Save the complete title list in a readable Markdown file and the structured snapshot when available.
- Do not collect the unfiltered portal inventory when a scope-refinement gate is still unresolved.

## Filter 2: Broad Title Screen

- Remove only clearly nontechnical or explicitly out-of-scope functions.
- Keep broad terms such as research, algorithm, system, network, engineering, product, project, and solution when the technical object is unclear.
- Keep ambiguous engineering subfields for later metadata or JD review.
- Group removed records by concise reason and retain their IDs.
- Save retained, removed, review, and decision files before continuing.

This stage favors recall over precision.

## Filter 3: Hard Eligibility

- Apply degree, cohort, graduation date, work authorization, and explicit major restrictions.
- Degree requirements are minimum eligibility, not proof of the intended hire's degree or compensation. Retain `master or above` roles for PhD matching; assess technical fit and investigate PhD-specific level or compensation separately when needed. A broad degree minimum or conflicting list/JD labels must not alone cause removal.
- For `bachelor or above`, assess the work rather than assuming either PhD suitability or mismatch. Apply a degree-floor exclusion only when the user explicitly confirms that constraint.
- Keep undisclosed eligibility as `review`, not `remove`.
- For broad engineering hiring, retain accepted parent disciplines even when the role specialization is not yet clear.

## Filter 4: User-Confirmed Rules

The user provides generalizable constraints; deterministic processing applies them to all records.

Examples of suitable rule types:

- excluded cities;
- unwanted job families;
- required degree floor;
- explicit work-content exclusions;
- professionally incompatible disclosed majors.

Do not turn one user's city or business preference into a skill default. Use compound conditions when a broad keyword could also appear in relevant engineering work.

## Filter 5: Direct Human Decisions

The user directly identifies units, businesses, or records to remove or retain. Do not invent a general rule from these choices. Record the decision as `origin: user-manual` and preserve Filter 4.

## Early Convergence

Stop filtering and enter full-JD review when:

- the remaining set is economical to open;
- another title rule would risk material false removals;
- the visible fields can no longer resolve ambiguity.

Five files are not a success criterion. A safe shortlist is.

## Removal Safety

Before deleting an engineering record, verify:

1. the decision is supported by a visible field;
2. the field is not missing or unread;
3. the rule does not rely on a generic keyword alone;
4. adjacent subfields have passed the transfer-bridge check when relevant;
5. the record can be restored from an upstream snapshot;
6. the reason and rule origin are logged.

When uncertainty remains, use `review`.

## Defensive Validation

- Reconcile portal totals and unit totals.
- For every stage, require `input = keep + remove + review`.
- Require mutually exclusive output IDs and exact coverage of parent IDs.
- Sample both kept and removed records manually.
- Reopen every final recommendation's current official JD.
- Compare new and previous inventories when the portal is still updating.

Use `scripts/validate_funnel.py` for count and ID invariants when JSONL records are available.
