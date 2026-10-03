# Routing Rules

## Two Independent Axes

Choose an access route and a hiring standard independently.

### Access Route

- `direct`: few effective review units and cheap official details;
- `bulk`: many records or expensive repetitive detail navigation;
- `umbrella`: few titles but each contains distinct technical subdirections;
- `assisted`: the confirmed official inventory requires a user-provided export or other bounded assistance. Missing candidate evidence is handled by the intake gate, not route selection.

### Hiring Standard

- `strict specialist`: named research direction, elite PhD program, research scientist, or advanced pre-research;
- `broad engineering`: broad engineering-family eligibility and general research/development placement;
- `pooled allocation`: common entry followed by internal team matching.

Do not equate `PhD candidate` with `strict specialist`. Use the job's actual selection model.

## Effective Review Units

Raw title count is not always the workload.

- Duplicate records with distinct IDs remain distinct inventory records.
- One umbrella title with six technical tracks creates six review units for fit analysis.
- A portal with 1,000 roles but an official degree/category filter yielding 25 roles has roughly 25 effective units after the filter is verified.

## Default Route Heuristics

These are defaults, not hard thresholds:

| Condition | Preferred route |
|---|---|
| Up to roughly 20-30 effective units, stable direct details | Direct |
| Roughly 30-100 units with batch metadata and cheap details | Direct or short bulk funnel |
| More than roughly 100 units, many subsidiaries, or repeated backtracking | Bulk |
| Fewer than 10 broad titles with multiple embedded directions | Umbrella |
| Complete list cannot be established | Assisted or stop |

Override the count when detail access cost or anti-bot risk dominates.

## Route-Cost Model

Estimate, do not fabricate precision:

```text
expected work = inventory pages
              + required detail opens
              + navigation/backtracking cost
              + team-research cost for finalists
```

Classify detail access:

- `low`: batch text, stable URLs, or new tabs;
- `medium`: drawers, pagination, or occasional backtracking;
- `high`: repeated in-place navigation, login/session fragility, slow rendering, or rate-limit signals.

## Confirmation Rule

Request user confirmation when:

- exhaustive review would require hundreds of detail opens;
- the official scope differs materially from the user's assumed scope;
- a limited-scope audit is the only available alternative to an incomplete list.

Do not ask merely because two reasonable low-cost routes exist. Choose conservatively and proceed.
