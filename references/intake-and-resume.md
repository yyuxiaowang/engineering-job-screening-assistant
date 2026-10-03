# Intake and Candidate-Material Protocol

## Hard Gate

Before recruitment-related web search, browser action, local file discovery, or candidate-file reading, determine whether the request establishes:

- the target company, program, or hiring unit;
- the recruitment scope when campus, experienced, internship, or special programs could produce different inventories;
- the read-only files or folders that contain the candidate's background evidence.
- the execution mode: `staged` or `continuous`;
- the writable project root for audit outputs.

If any required item is missing, ask once and stop. Do not perform reconnaissance first. The official URL is optional: prefer the direct position-list or search-results page rather than a recruitment landing page. If the user does not have it, locate the direct list after the gate passes.

## Default Outcome

The default task is to identify and rank suitable roles using the candidate's actual background. Do not ask the user to choose between a broad direction screen and personalized matching.

Recruitment-status checks, inventory collection, and title screening are internal stages. Team, research-community, level, and compensation investigation are performed when requested or needed to distinguish finalists.

## Minimum Intake

Ask for only missing material facts:

| Input | Required when | Accepted form |
|---|---|---|
| Target entity | Always | Company, program, or named unit |
| Recruitment scope | When multiple hiring programs are plausible | Campus cohort, experienced hiring, internship, special program, or all public hiring |
| Candidate materials | Always | Explicit read-only file paths, an explicitly authorized folder, or a compact profile |
| Execution mode | Always | `staged` or `continuous`; recommend `staged` when omitted |
| Output project root | Always | Explicit writable folder for persistent audit artifacts |
| Hard constraints | Optional | Only restrictions the user explicitly wants enforced; absence means none |

The candidate materials may include a resume, research and project records, representative papers, thesis material, patents, standards, presentations, code or portfolio evidence, and prior job-search records. Do not imply that a resume alone is necessarily sufficient, and do not require the user to classify their own field when the evidence can establish it.

## Candidate-Source Authorization

Use only:

- files explicitly named in the request;
- files inside a folder the user explicitly identifies as readable for this audit;
- candidate facts explicitly supplied for the current audit.

Do not search outside the supplied paths for likely materials. File accessibility is not authorization. Do not infer the current resume from filenames, timestamps, or prior applications. If several versions exist within an authorized location and the controlling version is unclear, ask the user.

Access candidate sources read-only. Copy files only when the user explicitly grants that permission. When copying is authorized:

- copy only files actually useful to the audit;
- place them in a new folder under the designated project workspace;
- preserve source files unchanged;
- record source and destination paths in the checkpoint or audit report.

## Candidate Profile Fallback

When file paths are unavailable, request a compact profile using the user's language:

```text
Degree and expected graduation date:
Engineering family and research subfields:
Core research objects:
Methods, tools, and experimental platforms:
Representative papers, patents, standards, or prototypes:
Explicit hard constraints, if any:
```

Do not demand every field. Mark omitted optional fields as unknown.

## Waiting Response

Use this shape in the user's language when the gate does not pass:

```text
RECRUITMENT AUDIT: WAITING FOR INPUT

Required:
- Recruitment scope: ...
- Candidate material paths or readable folder: ...
- Execution mode: staged or continuous
- Writable project-output root: ...

Optional:
- Direct position-list URL; otherwise state that the skill should locate it
- Explicit hard constraints, if any

If some recommended materials are unavailable, the user may authorize proceeding with the specified materials only; record the resulting evidence limits.

Resume phrase: <a short phrase in the user's language>
```

Omit fields already supplied. Do not separately request degree, graduation date, publications, or projects before reading the authorized materials; ask later only when a missing fact affects eligibility or ranking.

When useful, provide a response example that emphasizes source access rather than suggested preferences:

```text
Review the specified recruitment scope in staged mode. I authorize read-only access to <candidate-material folder>, which contains my resume, publications, research presentations, job-search records, and other background material. You may also read <additional path>. Save every stage under <writable project root>/<company and scope>. I have no location or role constraints; infer suitable roles from the verified materials. I also authorize copying only the key files used into the audit folder and recording their sources.
```

Use `Continue <company> recruitment audit` or the equivalent in the user's language as the company-specific resume phrase.

If the task is multi-turn or costly, create `Recruitment_Intake_<Company>_<Program>_<Year>.md` containing:

- status: `waiting`, `scope-confirmation`, `route-confirmation`, `ready`, or `resumed`;
- request and verified scope;
- official URL and access date;
- authorized candidate sources;
- required missing inputs;
- optional unknowns;
- reconnaissance summary;
- proposed route and alternatives;
- last confirmed user decision;
- next executable action.

## Resume Behavior

When the user uses the stated resume phrase or an equivalent expression:

1. locate the checkpoint in the current project or use the path the user supplies;
2. verify that required inputs are now present;
3. recheck volatile official status when the checkpoint is not current;
4. resume from `next executable action` rather than restarting;
5. do not infer approval for an expensive alternative route unless the checkpoint records it.

An unrelated intervening question does not cancel the audit. It also does not authorize automatic continuation.
