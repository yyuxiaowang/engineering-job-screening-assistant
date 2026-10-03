# Official-Site Access and Cost Reconnaissance

## Scope Verification

Establish:

- company and legal or recruiting unit;
- recruitment program and cohort;
- official landing page and actual application list;
- current opening status and known dates;
- whether the scope is all roles, one unit, one program, or one location;
- whether roles are still being added.

Press releases and program introductions are not role inventories.

## Inventory Probe

Inspect the list without opening every detail or collecting every page:

1. record displayed total count and pagination or infinite-scroll behavior;
2. record official filters and their selected state;
3. identify visible fields;
4. test whether all titles can be copied or read in batches;
5. distinguish duplicate titles by role ID when available;
6. reconcile unit totals with the portal total when possible.

## Scope-Refinement Gate

Run this gate before full inventory collection when any of these conditions applies:

- more than one recruitment project could satisfy the intake scope;
- official filters could materially reduce the result set without excluding credible adjacent work;
- collection would require substantial pagination or repeated UI actions;
- obtaining the list would require investigating a dynamic bulk interface.

Record and present:

- the direct official position-list URL, not only the recruitment landing page;
- each recruitment project available within the confirmed hiring category;
- relevant official filter groups and their displayed options;
- current selections and result count;
- whether leaving a group unselected means all results, only when verified from the interface;
- a recommended selection derived from the candidate evidence;
- the expected effect on scope and collection cost when visible or reasonably bounded.

Ask the user to confirm the recruitment projects and filters, or explicitly choose no filter. Do not begin pagination, bulk endpoint investigation, or complete inventory extraction before confirmation. This gate applies in `continuous` mode as well when the unresolved choice materially changes coverage or cost.

Use a compact stopping response:

```text
RECRUITMENT AUDIT: SCOPE CONFIRMATION

Direct position-list page: ...
Current result count: ...

Recruitment projects:
- ...

Official filter groups that materially affect this audit:
- ...

Recommended scope based on the provisional candidate profile:
- ...

Please confirm the projects and filters, or state that a group should remain unfiltered.
```

List options actually shown by the official portal. Do not invent a universal category menu or require location filtering when the candidate has no location constraint.

Do not define universal exclusions for engineering PhDs. Recommend filters from the current candidate's evidence and explain only the distinctions that affect this audit.

## Representative Detail Probe

Open one representative role before declaring details inaccessible:

1. snapshot the current tab list or browser state;
2. use a fresh DOM or screenshot;
3. activate the visible card or detail action;
4. check the original page for a drawer, modal, or in-place navigation;
5. check for a new tab;
6. verify that duties and qualifications are official and readable;
7. record the stable role URL when exposed.

An unchanged list URL does not prove failure when the site opens a new tab.

## Access Results

- `PASS - direct`: current complete scope and economical details are available.
- `PASS - bulk`: complete current title inventory and later survivor-detail access are available.
- `PASS - umbrella`: complete broad-role list and internal directions are readable.
- `STOP - inaccessible`: login, CAPTCHA, rendering, geography, or access failure prevents verification.
- `STOP - incomplete`: only partial roles, examples, cached fragments, or missing required scope are available.
- `STOP - unverified`: currency or completeness cannot be established.

## Workload Report

Report concrete quantities:

| Measure | Meaning |
|---|---|
| Inventory records | All official records in scope |
| Effective review units | Records or subdirections requiring fit judgment |
| Expected detail opens | Full JDs that the proposed route would open |
| Navigation cost | Low, medium, or high |
| Access risk | None observed, moderate, or high |
| Update risk | Static, unknown, or still updating |

Avoid exact completion-time or token promises. Give a bounded qualitative estimate and explain the dominant cost.

## Safe Access Behavior

- Use official filters before custom scraping when they accurately represent the requested scope.
- Prefer batch-visible text or an official export over repetitive clicks.
- Do not evade anti-bot controls or increase request frequency after warning signals.
- When a user-provided export has clear official provenance and scope, it may satisfy inventory access.
- Recheck official availability before final submission advice.
