"""Exercise evidence integrity, broad collection, and reviewable reports."""

import contextlib
import copy
import difflib
import hashlib
import io
import json
import os
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import collect_sessions
from render_report import render_report, validate_report
from session_evidence import JsonlRecords, read_record_range, redact_record, verify_snapshot


SCRIPTS = Path(__file__).parent


def write_records(path, records):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(item) + "\n" for item in records), encoding="utf-8")


def codex_records(identifier, cwd, reference=None):
    records = [{"type": "session_meta", "payload": {"id": identifier, "cwd": str(cwd)}}]
    if reference:
        records.append({"type": "response_item", "payload": {
            "type": "function_call", "name": "read_file",
            "arguments": json.dumps({"path": str(reference)}),
        }})
    records.append({"type": "response_item", "payload": {
        "type": "message", "role": "assistant",
        "content": [{"type": "output_text", "text": "The requested explanation."}],
    }})
    return records


def collected_source(path):
    reader = JsonlRecords(path)
    list(reader)
    return reader.snapshot()


class EvidenceTests(unittest.TestCase):
    def test_middle_excerpts_retain_physical_record_locations(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "rollout-middle.jsonl"
            records = codex_records("middle", directory)
            records.extend({"type": "response_item", "payload": {
                "type": "message", "role": "assistant",
                "content": [{"type": "text", "text": f"step {index}"}],
            }} for index in range(200))
            write_records(path, records)
            with path.open("a") as stream:
                stream.write("invalid JSON\n")
            _, _, entries, _ = collect_sessions.parse_codex_session(path, set(), False)
            self.assertEqual(entries.source["invalid_records"], [203])
            self.assertEqual(entries.locations[0]["record"], 2)
            self.assertNotIn(("assistant", "step 120"), entries)
            original = read_record_range(entries.source, 123, 123)
            self.assertEqual(original[0]["value"]["payload"]["content"][0]["text"], "step 120")

    def test_appended_records_do_not_change_the_collected_prefix(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "source.jsonl"
            path.write_text('{"text": "original"}')
            source = collected_source(path)
            with path.open("a") as stream:
                stream.write('\n{"text": "later"}\n')
            verify_snapshot(source)
            self.assertEqual(read_record_range(source, 1, 1)[0]["value"], {"text": "original"})
            path.write_text('{"text": "modified"}\n')
            with self.assertRaises(ValueError):
                verify_snapshot(source)

    def test_credentials_and_private_reasoning_are_omitted(self):
        record = {
            "api_key": "private-value",
            "text": 'password="another-value" Authorization: Bearer bearer-value',
            "items": [{"type": "reasoning", "summary": "private-thought"},
                      {"channel": "analysis", "content": "private-analysis"}],
        }
        result = json.dumps(redact_record(record))
        for value in ("private-value", "another-value", "bearer-value", "private-thought", "private-analysis"):
            self.assertNotIn(value, result)
        self.assertIn("REDACTED", result)

    def test_codex_analysis_messages_are_not_transcript_entries(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "source.jsonl"
            records = codex_records("analysis", directory)
            records.append({"type": "response_item", "payload": {
                "type": "message", "role": "assistant", "channel": "analysis",
                "content": [{"type": "text", "text": "private-analysis"}],
            }})
            write_records(path, records)
            _, _, entries, _ = collect_sessions.parse_codex_session(path, set(), False)
            self.assertNotIn("private-analysis", json.dumps(entries))


class CollectionTests(unittest.TestCase):
    def test_all_projects_no_tool_sessions_and_unbiased_explicit_cap(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            skill = root / "skills" / "example" / "SKILL.md"
            skill.parent.mkdir(parents=True)
            skill.write_text("---\nname: example\ndescription: Example\n---\n")
            first = root / "codex" / "sessions" / "rollout-older.jsonl"
            second = first.with_name("rollout-newer.jsonl")
            write_records(first, codex_records("older", root / "project-one", skill))
            write_records(second, codex_records("newer", root / "project-two"))
            os.utime(first, (100, 100))
            os.utime(second, (200, 200))
            arguments = ["collector", "--days", "0", "--skills-dir", str(root / "skills")]
            for name in ("codex", "claude", "pi", "grok", "zcode"):
                arguments.extend((f"--{name}-home", str(root / name)))
            arguments.extend(("--warp-data-dir", str(root / "warp")))
            for cap, expected in ((0, 2), (1, 1)):
                out = root / f"report-{cap}"
                argv = arguments + ["--out", str(out), "--max-sessions", str(cap)]
                with patch.object(sys, "argv", argv), patch("pathlib.Path.home", return_value=root):
                    with contextlib.redirect_stdout(io.StringIO()):
                        collect_sessions.main()
                inventory = json.loads((out / "inventory.json").read_text())
                self.assertEqual(inventory["scope"]["conversation_scope"], "all_projects")
                self.assertEqual(inventory["stats"]["sessions_selected"], expected)
                self.assertEqual(inventory["skill_reference_counts"]["example"], 1)
                self.assertEqual(inventory["sessions"][0]["meta"]["id"], "newer")
                self.assertEqual(inventory["sessions"][0]["skill_references"], [])
                self.assertNotIn("skills_used", inventory["sessions"][0])

    def test_same_names_keep_distinct_versions_and_deduplicate_symlinks(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for version in ("one", "two"):
                path = root / version / "example" / "SKILL.md"
                path.parent.mkdir(parents=True)
                path.write_text(f"---\ndisable-model-invocation: true\n---\n{version}\n")
            (root / "alias").symlink_to(root / "one", target_is_directory=True)
            skills = collect_sessions.discover_skills([], root, [root / name for name in ("one", "two", "alias")], False)
            copies = skills["example"]["copies"]
            self.assertEqual(len(copies), 2)
            self.assertEqual(len({item["sha256"] for item in copies}), 2)
            self.assertTrue(all(item["explicit_only"] for item in copies))

    def test_same_repository_name_does_not_match_an_unrelated_checkout(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            first, second = root / "first" / "repo", root / "second" / "repo"
            first.mkdir(parents=True)
            second.mkdir(parents=True)
            self.assertFalse(collect_sessions.session_matches_repo(second, first))

    def test_warp_database_collection_saves_addressable_visible_messages(self):
        def varint(value):
            result = bytearray()
            while value > 127:
                result.append((value & 127) | 128)
                value >>= 7
            result.append(value)
            return bytes(result)

        def field(number, value):
            if isinstance(value, str):
                value = value.encode()
            return varint((number << 3) | 2) + varint(len(value)) + value

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            database = root / "warp.sqlite"
            messages = [field(2, field(1, "Explain this")), field(15, field(1, "private-thought")),
                        field(3, field(1, "The explanation"))]
            task = b"".join(field(5, message) for message in messages)
            with sqlite3.connect(database) as connection:
                connection.execute("CREATE TABLE agent_conversations (conversation_id TEXT, conversation_data TEXT, last_modified_at TEXT, summary TEXT)")
                connection.execute("CREATE TABLE agent_tasks (id INTEGER, conversation_id TEXT, task BLOB)")
                connection.execute("INSERT INTO agent_conversations VALUES (?, ?, ?, ?)", ("warp-one", "{}", "2026-10-08 10:00:00", "{}"))
                connection.execute("INSERT INTO agent_tasks VALUES (?, ?, ?)", (1, "warp-one", task))
            before = hashlib.sha256(database.read_bytes()).hexdigest()
            out = root / "report"
            argv = ["collector", "--harness", "warp", "--warp-db", str(database),
                    "--warp-data-dir", str(root / "absent"), "--out", str(out), "--days", "0"]
            with patch.object(sys, "argv", argv), patch("pathlib.Path.home", return_value=root):
                with contextlib.redirect_stdout(io.StringIO()):
                    collect_sessions.main()
            inventory = json.loads((out / "inventory.json").read_text())
            session = inventory["sessions"][0]
            evidence = read_record_range(session["source"], 1, 3)
            self.assertEqual(evidence[2]["value"]["text"], "The explanation")
            self.assertNotIn("private-thought", json.dumps(evidence))
            self.assertEqual(hashlib.sha256(database.read_bytes()).hexdigest(), before)


class ReportTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        root = Path(self.directory.name)
        self.path = root / "session.jsonl"
        write_records(self.path, [{"text": "Observed action"}])
        self.skill = root / "skill" / "SKILL.md"
        self.skill.parent.mkdir()
        self.skill.write_text("Original guidance.\n")
        self.inventory = {
            "generated_at": "2026-10-08T10:00:00Z", "scope": {"selection": "all_in_scope"},
            "stats": {"sessions_considered": 1}, "skill_reference_counts": {"skill": 0},
            "skills": [{"name": "skill", "copies": [{"path": str(self.skill),
                       "sha256": hashlib.sha256(self.skill.read_bytes()).hexdigest()}]}],
            "sessions": [{"key": "session", "selected": True, "source": collected_source(self.path)}],
        }
        self.report = {
            "schema_version": 1, "summary": "Evidence is incomplete.",
            "assessments": [{"session": "session", "status": "assessed", "dimensions": {
                name: {"status": "insufficient_evidence", "reason": "Relevant context is missing."}
                for name in ("efficiency", "code_quality", "procedure", "communication")
            }}], "findings": [], "proposals": [], "gaps": [],
        }
        self.evidence = [{"session": "session", "record": 1, "detail": "An observed action."}]

    def test_unknown_dimensions_and_zero_findings_are_valid(self):
        output = render_report(self.report, self.inventory)
        self.assertIn("insufficient_evidence", output)
        self.assertEqual(self.report["findings"], [])

    def test_every_session_must_be_accounted_for(self):
        self.report["assessments"] = []
        with self.assertRaises(ValueError):
            validate_report(self.report, self.inventory)
        self.report["assessments"] = [{"session": "session", "status": "not_assessed", "reason": "Source unavailable."}]
        validate_report(self.report, self.inventory)

    def test_numeric_grade_is_rejected(self):
        self.report["grade"] = 90
        with self.assertRaises(ValueError):
            validate_report(self.report, self.inventory)

    def test_judgments_require_valid_unchanged_source_evidence(self):
        dimension = self.report["assessments"][0]["dimensions"]["efficiency"]
        dimension["status"] = "direct"
        with self.assertRaises(ValueError):
            validate_report(self.report, self.inventory)
        dimension["evidence"] = copy.deepcopy(self.evidence)
        dimension["evidence"][0]["record"] = 2
        with self.assertRaises(ValueError):
            validate_report(self.report, self.inventory)
        dimension["evidence"] = self.evidence
        validate_report(self.report, self.inventory)
        self.path.write_text('{"text": "changed"}\n')
        with self.assertRaises(ValueError):
            validate_report(self.report, self.inventory)

    def test_report_text_is_escaped_and_has_no_external_assets(self):
        self.report["summary"] = '<script src="https://example.com/attack.js">attack()</script>'
        output = render_report(self.report, self.inventory)
        self.assertNotIn("<script", output)
        self.assertIn("&lt;script", output)
        self.assertNotIn("<link", output)

    def test_proposal_requires_supported_finding_exact_diff_and_current_version(self):
        finding = {"id": "F1", "priority": "medium", "confidence": "supported",
                   "summary": "Missing condition", "cause": "Guidance omits a condition.",
                   "recommendation": "State the condition.", "evidence": self.evidence}
        self.report["findings"] = [finding]
        draft = self.skill.parent.parent / "proposed.md"
        draft.write_text("Revised guidance.\n")
        proposal = {"finding": "F1", "skill_path": str(self.skill),
                    "skill_sha256": self.inventory["skills"][0]["copies"][0]["sha256"],
                    "proposed_path": str(draft), "validation": "Exercise the missing condition.",
                    "diff": "".join(difflib.unified_diff(self.skill.read_text().splitlines(keepends=True),
                              draft.read_text().splitlines(keepends=True), fromfile=str(self.skill), tofile=str(draft)))}
        self.report["proposals"] = [proposal]
        validate_report(self.report, self.inventory)
        finding["confidence"] = "tentative"
        with self.assertRaises(ValueError):
            validate_report(self.report, self.inventory)
        finding["confidence"] = "supported"
        draft.write_text("A different draft.\n")
        with self.assertRaises(ValueError):
            validate_report(self.report, self.inventory)
        draft.write_text("Revised guidance.\n")
        self.skill.write_text("Later guidance.\n")
        with self.assertRaises(ValueError):
            validate_report(self.report, self.inventory)

    def test_cli_inspection_and_rendering(self):
        root = Path(self.directory.name)
        inventory_path, report_path = root / "inventory.json", root / "report.json"
        inventory_path.write_text(json.dumps(self.inventory))
        report_path.write_text(json.dumps(self.report))
        inspected = subprocess.run([sys.executable, str(SCRIPTS / "inspect_evidence.py"), str(inventory_path),
                                    "--session", "session", "--record", "1", "--context", "0"],
                                   capture_output=True, text=True, check=True)
        self.assertEqual(json.loads(inspected.stdout)[0]["value"]["text"], "Observed action")
        subprocess.run([sys.executable, str(SCRIPTS / "render_report.py"), str(report_path),
                        "--inventory", str(inventory_path)], capture_output=True, text=True, check=True)
        self.assertTrue(report_path.with_suffix(".html").is_file())


if __name__ == "__main__":
    unittest.main()
