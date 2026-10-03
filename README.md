# Engineering Job Screening Assistant

A reusable AI skill that screens and ranks industry and engineering R&D roles for engineering PhDs using verified recruitment information and the candidate's research evidence.

Optimized for Chinese-language recruitment contexts, with English documentation and instructions. Supports employers, corporate research institutes, group subsidiaries, and research organizations using public job listings. Not intended for university faculty applications.

Preview release. Feedback is welcome through Issues; do not submit personal materials or sensitive information.

## Installation

Send this request in Codex:

```text
Use $skill-installer to install the skill at the root of https://github.com/yyuxiaowang/engineering-job-screening-assistant as engineering-phd-job-audit.
```

Requires an AI tool with web search and authorized local-file access; dynamic recruitment pages may require browser control. Optional helper scripts require Python 3.10+ and use only the standard library. Codex is the primary environment; compatibility with other tools has not been verified.

## Usage

Invoke the skill:

```text
$engineering-phd-job-audit Screen roles at <company>
```

For a more complete request:

```text
Use $engineering-phd-job-audit to screen <company>'s <year> campus recruitment in staged mode, waiting for my confirmation after each stage. The position-list page is <URL>; locate it if unavailable. I authorize read-only access to <material folder>, containing my resume, research projects, representative papers, presentations, and job-search records, and to <additional path> for supporting evidence. Save each stage's role lists, removal logs, retrieved job descriptions, and final report under <writable project path>/<company folder>. I have no location or role restrictions; infer suitable roles from my research evidence. I also authorize copying only the key source files used into the audit folder and recording their sources.
```

Provide information useful to the audit, including:

- Target company, recruitment program, and hiring scope
- Direct position-list URL, or a request to locate it
- Candidate-material paths, such as a resume, projects, papers, and other research evidence
- Execution mode: staged confirmation or continuous execution
- Writable project path for stage outputs
- Any explicit location, role, or other hard constraints; omit if none
- Additional investigation requested, such as team research, level, or compensation

The skill reads only explicitly supplied or authorized candidate materials, never searching the workspace for resumes. It asks for missing critical inputs before proceeding. Small inventories receive direct review; larger portals start with recruitment programs, official filters, and workload assessment. In staged mode, scope confirmation precedes full inventory collection and successive filtering rounds.

## Outputs

- Verified recruitment scope, role status, and official links
- Retained roles and auditable removal reasons
- Candidate-specific fit, key gaps, and recommended ranking
- Team, research, level, and compensation evidence when requested

Reports distinguish official facts, public evidence, reasonable inference, and unconfirmed information.

## License

[MIT](LICENSE). Use, modification, and redistribution, including commercial use, are permitted with the copyright notice and license retained.
