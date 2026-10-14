#!/usr/bin/env python3
"""Validate a qualitative skill diagnosis and render a self-contained report."""

import argparse
import difflib
import hashlib
import html
import json
import sys
from pathlib import Path

from session_evidence import verify_snapshot


DIMENSIONS = {
    "efficiency": {"direct", "avoidable_rework", "insufficient_evidence"},
    "code_quality": {"sound", "issue", "not_applicable", "insufficient_evidence"},
    "procedure": {"followed", "violation", "not_applicable", "insufficient_evidence"},
    "communication": {"proportionate", "excess", "missing_context", "insufficient_evidence"},
}
SKILL_STATES = {"referenced", "loaded", "application_observed", "unknown"}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def validate_report(report, inventory):
    require(report.get("schema_version") == 1, "Report schema_version must be 1.")
    require(not ({"scores", "overall", "grade"} & report.keys()), "Numeric grades are not supported.")
    require(isinstance(report.get("summary"), str) and report["summary"].strip(), "A summary is required.")
    sessions = {session["key"]: session for session in inventory["sessions"] if session["selected"]}
    assessments = report.get("assessments")
    require(isinstance(assessments, list), "assessments must be a list.")
    require(all(isinstance(item, dict) for item in assessments), "Each assessment must be an object.")
    keys = [item.get("session") for item in assessments]
    require(len(keys) == len(set(keys)), "Each session must appear once.")
    require(set(keys) == set(sessions), "Account for every selected session, including those not assessed.")

    verified_sources = set()

    def validate_evidence(evidence):
        require(isinstance(evidence, list) and evidence, "Evidence must include at least one source record.")
        for item in evidence:
            require(isinstance(item, dict), "Each evidence entry must be an object.")
            require(item.get("session") in sessions, "Evidence references an unknown session.")
            source = sessions[item["session"]]["source"]
            count = source.get("records", 0)
            record = item.get("record")
            require(type(record) is int and 1 <= record <= count, "Evidence record is outside its source snapshot.")
            require(bool(item.get("detail")), "Evidence needs a concrete observation.")
            if item["session"] not in verified_sources:
                verify_snapshot(source)
                verified_sources.add(item["session"])

    for assessment in assessments:
        state = assessment.get("status")
        require(state in {"assessed", "not_assessed", "blocked"}, "Invalid assessment status.")
        if state != "assessed":
            require(bool(assessment.get("reason")), "Unassessed sessions need a reason.")
            continue
        dimensions = assessment.get("dimensions", {})
        require(isinstance(dimensions, dict), "dimensions must be an object.")
        require(set(dimensions) == set(DIMENSIONS), "An assessment must account for all four dimensions.")
        for name, labels in DIMENSIONS.items():
            dimension = dimensions[name]
            require(isinstance(dimension, dict), f"{name} must be an object.")
            require(dimension.get("status") in labels, f"Invalid {name} status.")
            require(bool(dimension.get("reason")), f"{name} needs a reason.")
            if dimension["status"] not in {"not_applicable", "insufficient_evidence"}:
                validate_evidence(dimension.get("evidence"))
        for skill in assessment.get("skill_evidence", []):
            require(isinstance(skill, dict), "Each skill evidence entry must be an object.")
            require(skill.get("state") in SKILL_STATES, "Invalid skill evidence state.")
            require(bool(skill.get("name")) and bool(skill.get("reason")), "Skill evidence needs a name and reason.")
            if skill["state"] != "unknown":
                validate_evidence(skill.get("evidence"))

    findings = report.get("findings", [])
    require(isinstance(findings, list), "findings must be a list.")
    require(all(isinstance(item, dict) for item in findings), "Each finding must be an object.")
    identifiers = [item.get("id") for item in findings]
    require(all(identifiers) and len(identifiers) == len(set(identifiers)), "Finding IDs must be nonempty and unique.")
    for finding in findings:
        require(finding.get("priority") in {"high", "medium", "low"}, "Invalid finding priority.")
        require(finding.get("confidence") in {"supported", "tentative"}, "Invalid finding confidence.")
        require(all(finding.get(key) for key in ("summary", "cause", "recommendation")), "A finding needs its cause and recommendation.")
        validate_evidence(finding.get("evidence"))
        if finding.get("counterevidence"):
            validate_evidence(finding["counterevidence"])

    proposals = report.get("proposals", [])
    require(isinstance(proposals, list), "proposals must be a list.")
    copies = {copy["path"]: copy for skill in inventory["skills"] for copy in skill["copies"]}
    supported = {item["id"] for item in findings if item["confidence"] == "supported"}
    for proposal in proposals:
        require(isinstance(proposal, dict), "Each proposal must be an object.")
        require(proposal.get("finding") in supported, "A proposal needs a supported finding.")
        source = copies.get(proposal.get("skill_path"))
        require(source is not None, "A proposal must name the exact collected skill path.")
        require(proposal.get("skill_sha256") == source["sha256"], "Proposal skill version does not match the collected version.")
        current = Path(source["path"]).read_bytes()
        require(hashlib.sha256(current).hexdigest() == source["sha256"], "The proposed skill changed; reassess before reporting this proposal.")
        require(all(proposal.get(key) for key in ("proposed_path", "diff", "validation")), "A proposal needs its draft, diff, and validation plan.")
        require(Path(proposal["proposed_path"]).is_file(), "Proposed skill draft does not exist.")
        require(Path(proposal["proposed_path"]).resolve() != Path(source["path"]).resolve(), "Drafts must be separate from installed skills.")
        draft = Path(proposal["proposed_path"]).read_text(encoding="utf-8")
        expected_diff = "".join(difflib.unified_diff(
            current.decode("utf-8").splitlines(keepends=True),
            draft.splitlines(keepends=True),
            fromfile=source["path"], tofile=proposal["proposed_path"],
        ))
        require(expected_diff and proposal["diff"] == expected_diff, "Proposal diff must match the collected skill and draft exactly.")
    require(isinstance(report.get("gaps", []), list), "gaps must be a list.")
    return sessions


def escape(value):
    return html.escape(str(value), quote=True)


def render_report(report, inventory):
    sessions = validate_report(report, inventory)
    rows = []
    assessed = 0
    for item in report["assessments"]:
        assessed += item["status"] == "assessed"
        dimensions = item.get("dimensions", {})
        cells = "".join(
            f"<td>{escape(dimensions.get(name, {}).get('status', 'not assessed'))}</td>"
            for name in DIMENSIONS
        )
        detail = json.dumps(item, indent=2, ensure_ascii=False)
        rows.append(
            f"<tr><td>{escape(item['session'])}<details><summary>Evidence and reasons</summary>"
            f"<pre>{escape(detail)}</pre></details></td><td>{escape(item['status'])}</td>{cells}</tr>"
        )
    findings = []
    for item in report.get("findings", []):
        findings.append(
            f"<article><h3>{escape(item['id'])}: {escape(item['summary'])}</h3>"
            f"<p>{escape(item['priority'])} priority · {escape(item['confidence'])}</p>"
            f"<p>{escape(item['cause'])}</p><p>{escape(item['recommendation'])}</p>"
            f"<details><summary>Evidence and counterevidence</summary>"
            f"<pre>{escape(json.dumps({key: item.get(key, []) for key in ('evidence', 'counterevidence')}, indent=2))}</pre></details></article>"
        )
    proposals = "".join(
        f"<article><h3>{escape(item['skill_path'])}</h3><p>{escape(item['validation'])}</p>"
        f"<details><summary>Proposed diff</summary><pre>{escape(item['diff'])}</pre></details></article>"
        for item in report.get("proposals", [])
    )
    gaps = "".join(f"<li>{escape(item)}</li>" for item in report.get("gaps", []))
    references = "".join(
        f"<tr><td>{escape(name)}</td><td>{escape(count)}</td></tr>"
        for name, count in inventory.get("skill_reference_counts", {}).items()
    )
    title = report.get("title", "Skill diagnosis")
    scope = json.dumps(inventory["scope"], indent=2)
    return f"""<!doctype html>
<html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)}</title><style>
:root {{ color-scheme: light dark; }}
body {{ font: 16px/1.6 system-ui,sans-serif; max-width: 1100px; margin: 3rem auto; padding: 0 1rem; }}
h1,h2,h3 {{ line-height: 1.2; }} article {{ margin: 1.5rem 0; }}
table {{ width: 100%; border-collapse: collapse; }} th,td {{ text-align: left; padding: .6rem; border-bottom: 1px solid #8886; vertical-align: top; }}
.table {{ overflow-x: auto; }} pre {{ white-space: pre-wrap; overflow-wrap: anywhere; font: .85rem/1.5 ui-monospace,monospace; }}
summary {{ cursor: pointer; }} details {{ margin: .5rem 0; }}
</style><main><h1>{escape(title)}</h1><p>{escape(report['summary'])}</p>
<p>Assessed {assessed} of {len(sessions)} sessions included in the report; {inventory['stats']['sessions_considered']} sessions considered. Usage references do not establish skill application or effectiveness.</p>
<details><summary>Collection scope</summary><pre>{escape(scope)}</pre></details>
<h2>Findings</h2>{''.join(findings) or '<p>No findings recorded. Review assessment coverage and gaps below.</p>'}
<h2>Proposed changes</h2>{proposals or '<p>No skill edits proposed.</p>'}
<h2>Session assessments</h2><div class="table"><table><thead><tr><th>Session</th><th>Assessment</th><th>Efficiency</th><th>Code quality</th><th>Procedure</th><th>Communication</th></tr></thead><tbody>{''.join(rows)}</tbody></table></div>
<h2>Reference counts</h2><p>These counts cover all considered sessions, including any excluded by a cap, and include inspections. They are not quality scores.</p>
<table><thead><tr><th>Skill name</th><th>Sessions with a reference</th></tr></thead><tbody>{references}</tbody></table>
<h2>Gaps</h2><ul>{gaps or '<li>No additional gaps recorded.</li>'}</ul>
<footer><p>Collected {escape(inventory['generated_at'])}. Review evidence and proposals before changing instructions.</p></footer></main></html>"""


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", type=Path)
    parser.add_argument("--inventory", type=Path, required=True)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    try:
        report = json.loads(args.report.read_text(encoding="utf-8"))
        inventory = json.loads(args.inventory.read_text(encoding="utf-8"))
        output = render_report(report, inventory)
        destination = args.out or args.report.with_suffix(".html")
        destination.write_text(output, encoding="utf-8")
        print(destination.resolve())
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
