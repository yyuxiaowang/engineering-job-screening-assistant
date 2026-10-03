---
name: engineering-phd-job-audit
description: Screen and rank current public industry and engineering-research roles for an engineering PhD using candidate materials explicitly provided by the user. Use for a named company or program, from small specialist hiring to high-volume portals, when official role verification, reversible filtering, full-JD comparison, team investigation, or finalist compensation evidence may be needed. Do not use for non-engineering hiring, university faculty applications, or standalone resume wording.
---

# Engineering PhD Recruitment Audit

## Purpose

Identify and rank suitable public industry and engineering-research roles for an engineering PhD. Use the candidate's authorized materials as the evidence base, verify the official recruitment scope, and choose direct review, reversible bulk filtering, or umbrella-role decomposition according to access cost.

Use the least expensive route that can support the requested conclusion. Do not force every request through all filters or all fit levels.

The workflow is optimized for Chinese-language recruitment contexts. Interact in the user's language and preserve official role titles and source evidence in their original language.

## Invariants

1. Use current official sources for recruitment scope, eligibility, duties, status, and application links; label historical or incomplete material accordingly.
2. Verify list completeness separately from detail-page access. Search results and publicity examples are not a complete inventory.
3. Preserve each upstream inventory. Every automated removal must record its rule, evidence field, and origin and remain reversible.
4. Treat missing or unread data as unknown, not as evidence of mismatch.
5. Compare engineering object, technical layer, problem, methods, and outputs. Neither a different subfield label nor a shared generic tool is sufficient to decide fit.
6. Read the complete official JD before a final recommendation and distinguish sourced facts from inference.
7. If the requested method is materially expensive or risky, report the measured workload and confirm the route before proceeding.

## Workflow

### 1. Intake

Read [references/intake-and-resume.md](references/intake-and-resume.md) and apply the intake gate before recruitment reconnaissance or candidate discovery. Until the gate passes, do not browse recruitment sites, search local directories, or read candidate files. The gate passes when the target entity, recruitment scope, read-only candidate-material paths, execution mode, and writable project-output root are clear.

If the gate does not pass, return `RECRUITMENT AUDIT: WAITING FOR INPUT`, request only the missing items, and stop. Do not ask whether the user wants a title screen or personalized ranking: personalized screening and ranking are the default. Do not guess the hiring program, combine campus and experienced hiring, scan the workspace for resumes, or select among candidate files by filename or modification time.

Candidate evidence may come only from files or folders named by the user and facts explicitly supplied for the current audit. Relevant materials may include resumes, research or project records, papers, theses, patents, presentations, portfolios, and job-search records. Infer the candidate's fields and credible adjacent directions from this evidence rather than requiring a self-classification. If the materials omit a hard eligibility fact or conflict materially, ask a targeted follow-up after reading them.

Treat candidate sources as read-only. Copy selected source files into the designated project workspace only when the user explicitly authorizes copying; preserve the originals and record each source path and destination.

Execution modes:

- `staged` (recommended): save the current stage, report its counts and files, then stop for confirmation before the next stage;
- `continuous`: run without routine confirmation, but save every stage and apply the same early-stop rules.

Create the intake checkpoint in the designated project-output root. Do not place a persistent audit in a date-based temporary workspace unless the user explicitly chooses that location.

### 2. Provisional Candidate Profile and Official-Site Reconnaissance

Read the progressive-loading section of [references/candidate-fingerprint.md](references/candidate-fingerprint.md). Build only the provisional candidate profile needed to recommend recruitment projects and official filters. Do not read every paper, thesis chapter, presentation, or historical application before the recruitment scope is confirmed.

Then read [references/access-and-cost.md](references/access-and-cost.md). Establish the official scope, access date, displayed record count, visible fields, usable filters, update status, detail-page behavior, and access barriers before selecting a route. Prefer a direct position-list page. Use browser control only when ordinary web access cannot read the official dynamic or session-dependent page; never bypass access controls.

If the official inventory cannot be verified, stop or request an official export. If only candidate information is missing, pause at intake rather than reporting an access failure.

Probe filters before collecting the full inventory. Invoke the scope-refinement gate defined in [references/access-and-cost.md](references/access-and-cost.md) when multiple recruitment projects remain unresolved, when official facets could materially reduce the result set, or when collection would require substantial pagination, repeated UI actions, or bulk-interface investigation. Save the reconnaissance, present the actual options and a candidate-specific recommendation, then stop for confirmation. Do not begin full pagination or investigate bulk data interfaces before this gate is resolved.

After the project and filters are confirmed, collect and save the complete filtered inventory as Filter 1. In `staged` mode, report its count and artifacts, then wait before Filter 2. In `continuous` mode, still pause when an unresolved scope choice would materially change coverage, cost, or false-removal risk.

### 3. Full Candidate and Hiring Model

Expand the provisional candidate profile only as needed for the confirmed scope. Represent the candidate and role with the same engineering dimensions and evidence tiers from [references/candidate-fingerprint.md](references/candidate-fingerprint.md). Separately classify the hiring model as `strict specialist`, `broad engineering`, or `pooled allocation`; a PhD requirement alone does not imply strict specialist hiring.

### 4. Route

Read [references/routing-rules.md](references/routing-rules.md) and choose by effective review units, detail-access cost, ambiguity, and site risk:

- `direct`: few roles with economical full JDs;
- `bulk`: many records or costly repetitive navigation;
- `umbrella`: few broad titles containing distinct technical tracks;
- `assisted`: the confirmed official scope cannot be retrieved without a user-provided export or other bounded assistance.

For `bulk`, follow [references/bulk-filtering.md](references/bulk-filtering.md). Use `scripts/normalize_inventory.py`, `apply_filter_rules.py`, `validate_funnel.py`, and `diff_snapshots.py` when structured data makes deterministic processing useful. Filters 4 and 5 are optional; enter full-JD review once further metadata filtering would risk false removals.

### 5. Convergence

Before detailed analysis, each survivor must have an exact title, hiring unit, current official source, application or lookup link, hard-eligibility status, and retrievable duties and qualifications. If the set remains too large, apply only the next safe filtering stage and never tighten a rule silently.

### 6. Detailed Fit

Read [references/detailed-job-fit.md](references/detailed-job-fit.md) and [references/evidence-rules.md](references/evidence-rules.md). Progress from recruitment status and title screening (`L0-L1`) through full-JD comparison (`L2`), team verification (`L3`), finalist due diligence (`L4`), and finalist compensation (`L5`). Stop investigating rejected roles unless a post-mortem is requested.

Rank by verified fit and evidence confidence, not keyword count. Do not add mismatched roles to reach a requested quota.

Stop after `L2` when no viable role remains or deeper research cannot change the recommendation. Run `L3` only when team evidence can resolve a material ambiguity, `L4` for finalists requiring application due diligence, and `L5` only when compensation or level is requested. In `staged` mode, save and pause after every executed level.

### 7. Corrections and Updates

When detailed review exposes an unsafe earlier rule, restore affected records from the upstream snapshot, revise the rule without overwriting history, and rerun validation. For an updated portal, compare snapshots and process added or changed records when possible.

## Artifacts and Reporting

Use the writable project-output root confirmed during intake. Read [references/data-schema.md](references/data-schema.md) for structured records and [references/report-templates.md](references/report-templates.md) for outputs.

Create one folder per company and recruitment scope. Persist every executed stage, including the complete inventory, retained and removed records, decision log, retrieved official JDs, detailed-fit levels, and final report. Preserve prior snapshots rather than overwriting them. A direct route may omit unused filter numbers, but it must still save its inventory and each executed fit level.

Report the verified scope and access date, route and coverage, recommendations with official links, decisive fit evidence and gaps, confidence, and unresolved limitations. Identify the evidence type behind compensation estimates. Never present inference as company policy or an incomplete list as exhaustive.
