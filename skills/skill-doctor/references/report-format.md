# Report format

`render_report.py` validates a JSON report against the inventory and generates
self-contained HTML. It rejects missing session accounting, invalid evidence
locations, changed source records, numeric grade fields, and stale or inaccurate
proposal diffs. It cannot establish whether an observation or causal claim is
correct; the assessor must check that against the records.

Use schema version 1. `summary` is required; `title` is optional. `assessments`
contains exactly one entry for every inventory session with `selected: true`.
`findings`, `proposals`, and `gaps` are lists and may be empty.

An assessed entry has this shape (replace placeholders with actual evidence):

```json
{
  "session": "inventory-session-key",
  "status": "assessed",
  "dimensions": {
    "efficiency": {
      "status": "direct",
      "reason": "The investigation used the failing case to choose the next check.",
      "evidence": [{"session": "inventory-session-key", "record": 12, "detail": "Describe the observed action."}]
    },
    "code_quality": {
      "status": "insufficient_evidence",
      "reason": "The final candidate is absent from the recorded context."
    },
    "procedure": {
      "status": "insufficient_evidence",
      "reason": "The historical instruction body is unavailable."
    },
    "communication": {
      "status": "proportionate",
      "reason": "The response explains the result and its remaining limit.",
      "evidence": [{"session": "inventory-session-key", "record": 18, "detail": "Describe the final response."}]
    }
  },
  "skill_evidence": [
    {
      "name": "example-skill",
      "state": "referenced",
      "reason": "The tool arguments include its path; the output does not show a successful read.",
      "evidence": [{"session": "inventory-session-key", "record": 5, "detail": "A path appears in the read command."}]
    }
  ]
}
```

Allowed dimension statuses:

| Dimension | Statuses |
| --- | --- |
| `efficiency` | `direct`, `avoidable_rework`, `insufficient_evidence` |
| `code_quality` | `sound`, `issue`, `not_applicable`, `insufficient_evidence` |
| `procedure` | `followed`, `violation`, `not_applicable`, `insufficient_evidence` |
| `communication` | `proportionate`, `excess`, `missing_context`, `insufficient_evidence` |

Each dimension needs a reason. Judgments other than `insufficient_evidence` and
`not_applicable` need an evidence list. Skill states are `referenced`, `loaded`,
`application_observed`, and `unknown`; all but `unknown` require evidence. A
whole-session `blocked` or `not_assessed` entry needs a reason instead of
dimensions. Record material limitations in `gaps` as strings.

Each finding contains `id`, `priority` (`high`, `medium`, `low`), `confidence`
(`supported`, `tentative`), `summary`, `cause`, `recommendation`, and `evidence`.
Add `counterevidence` using the same session/record/detail shape when applicable.
Explain the search for counterexamples and version uncertainty in the cause or
gaps. An isolated lead can be tentative without implying an instruction change.

Each proposal contains `finding` (a supported finding ID), `skill_path` (the
exact collected path), `skill_sha256`, `proposed_path` (a separate local draft),
`diff`, and `validation` (a focused trial and expected observation). The skill
must still match its collected hash. Generate the diff from actual files:

```python
diff = "".join(difflib.unified_diff(
    original.splitlines(keepends=True),
    proposed.splitlines(keepends=True),
    fromfile=skill_path,
    tofile=proposed_path,
))
```

Do not handwrite an approximate diff. Use the exact path strings from the
proposal. Supporting changes to other resources can be described in the
recommendation; this renderer validates proposals for collected `SKILL.md`
files. HTML escapes all report text and loads no remote resources.
