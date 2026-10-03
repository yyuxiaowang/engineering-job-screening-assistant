# Detailed Job-Fit Audit

## Execution and Persistence

Save every executed level and the official role text used by that level. Store each retrieved JD under `roles/` with exact title, unit, role ID, source URL, access date, duties, and requirements so later work does not need to retrieve it again.

In `staged` mode, report the current decisions and artifact paths after each level, then stop for confirmation. In `continuous` mode, proceed only while the next level can materially improve the decision.

## L0: Recruitment Status

Record one status:

- active and fully open;
- active for a clearly bounded partial scope;
- announced, roles pending;
- not started;
- closed;
- inaccessible;
- unverified.

Include official URL, access date, cohort, locations, completeness boundary, and whether older material is historical only.

## L1: Fast Screen

Use the selected route's retained title and metadata set.

- Apply shared program eligibility once.
- Remove obvious nontechnical or hard-ineligible records.
- In strict-specialist hiring, an explicit object/layer mismatch can reject early.
- In broad-engineering hiring, retain adjacent accepted disciplines until the JD resolves daily work.
- Open official details only for surviving or ambiguous records.

## L2: Full-JD Technical Screen

Identify:

- core engineered object and problem;
- technical layer;
- mandatory methods, stack, platform, protocols, and instruments;
- expected deliverables;
- whether generic terms create a false friend;
- candidate's direct evidence, transfer bridge, and unsupported gaps.

Decisions:

- `L2 reject`;
- `L2 hold`;
- `L2 advance`.

Treat semantic conclusions from the JD as JD-based inference, not verified team facts.

## L3: Team and Research-Community Verification

Run only for the most relevant L2 survivors when team evidence could change their ranking or viability.

1. map the narrowest publicly supportable team;
2. inspect repeated recent outputs rather than one isolated paper;
3. use people, papers, patents, standards, products, technical talks, and open source;
4. compare team and candidate fingerprints using the same dimensions;
5. stop when a material mismatch is established.

Decisions:

- `L3 reject - different community`;
- `L3 adjacent`;
- `L3 pass`;
- `L3 uncertain`.

Do not infer that a coauthor is a current employee or that a public senior leader is the hiring manager.

## L4: Finalist Due Diligence

Run only for finalists when application or interview due diligence is needed.

Investigate:

- likely daily work and deliverables;
- engineering stack and validation environment;
- research versus standards, product, operations, or customer-delivery balance;
- comparable publicly documented candidate backgrounds;
- interview topics and evidence gaps;
- organization, location, and stability when supportable;
- truthful resume emphasis and claims that must not be made.

Decisions:

- `strong match`;
- `match with bounded gaps`;
- `credible adjacent`;
- `stretch`;
- `reject`.

## Ranking

Rank by:

1. highest verified stage;
2. direct object/layer alignment;
3. candidate evidence depth;
4. transfer-bridge strength;
5. evidence confidence;
6. user constraints and preferences.

Recommend only genuinely viable roles. Do not fill a quota with mismatched roles.

## L5: Level and Compensation

Run only when the user requests level or compensation analysis.

- distinguish campus PhD, postdoc, experienced hire, and special talent program;
- normalize year, city, degree, role family, salary months, bonus, stock, sign-on, and subsidies;
- separate official guarantees from self-reported samples and inference;
- use low/base/high ranges and prefer the central cluster;
- state sample quality and confidence;
- do not present government subsidies or research funding as recurring salary.
