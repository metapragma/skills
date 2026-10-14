#!/usr/bin/env python3
"""Collect local Claude Code, Codex, Warp, Pi, Grok Build, and ZCode sessions and skill references for diagnosis.

Scans Claude Code project history, Codex rollout files, Warp's local
conversation databases, Pi agent session JSONL, Grok Build chat history,
and/or ZCode model-io rollouts, discovers installed skills, detects which
sessions referenced which skills, and emits:

  <out>/inventory.json        - skill copies, source records, scope, and counters
  <out>/transcripts/<id>.md   - condensed transcripts with source locations

Collection uses local files only. Assessment uses the active model runtime.
Python 3.9+, stdlib only.
"""

import argparse
import hashlib
import json
import os
import re
import sqlite3
import subprocess
import sys
from collections import deque
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import unquote
from warp_decoder import ProtobufDecodeError, decode_task
from session_evidence import JsonlRecords, MemoryRecords, redact_record, redact_text

MAX_WARP_CONVERSATION_BYTES = 32 * 1024 * 1024
MAX_MSG_CHARS = 1500
MAX_TOOL_CHARS = 500
MAX_TRANSCRIPT_ENTRIES = 160
TRANSCRIPT_HEAD = 100
TRANSCRIPT_TAIL = 40

CODE_EDIT_HINTS = ("apply_patch", "*** Begin Patch", "edit_file", "create_file", "str_replace", "write_file")
CLAUDE_CODE_EDIT_TOOLS = {"Edit", "MultiEdit", "NotebookEdit", "Write"}
GENERIC_EDIT_TOOLS = {"edit", "write", "apply_patch", "edit_file", "write_file", "str_replace", "search_replace"}


def parse_args():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--harness",
        choices=("auto", "all", "claude", "codex", "warp", "pi", "grok", "zcode"),
        default="auto",
        help="session source (default: auto; scans every locally available source)",
    )
    p.add_argument(
        "--claude-home",
        default=os.environ.get("CLAUDE_CONFIG_DIR", "~/.claude"),
        help="Claude Code config directory (default: CLAUDE_CONFIG_DIR or ~/.claude)",
    )
    p.add_argument("--codex-home", default=os.environ.get("CODEX_HOME", "~/.codex"))
    p.add_argument(
        "--pi-home",
        default="~/.pi/agent",
        help="Pi agent home (default: ~/.pi/agent)",
    )
    p.add_argument(
        "--grok-home",
        default="~/.grok",
        help="Grok Build home (default: ~/.grok)",
    )
    p.add_argument(
        "--zcode-home",
        default="~/.zcode",
        help="ZCode home (default: ~/.zcode)",
    )
    p.add_argument(
        "--warp-db",
        action="append",
        default=[],
        help="explicit Warp warp.sqlite path (repeatable)",
    )
    p.add_argument(
        "--warp-data-dir",
        default=os.environ.get("WARP_DATA_DIR"),
        help="directory containing Warp channel data directories",
    )
    p.add_argument(
        "--repo",
        action="append",
        default=[],
        help="project to include (repeatable; default: every project)",
    )
    p.add_argument(
        "--all-conversations",
        action="store_true",
        help="collect every project represented in local history (the default)",
    )
    p.add_argument("--include-global-skills", action="store_true",
                   help="also discover skills outside the repo (~/.codex/skills, ~/.agents/skills, ~/.claude/skills, ~/.pi/agent/skills, ~/.grok/skills, ~/.zcode/skills)")
    p.add_argument("--days", type=int, default=45, help="lookback window; 0 includes all history")
    p.add_argument("--max-sessions", type=int, default=0, help="newest-first cap; 0 collects every in-scope session")
    p.add_argument("--skills-dir", action="append", default=[], help="extra skills directory to scan (repeatable)")
    p.add_argument("--include-subagents", action="store_true", help="include subagent/child sessions")
    p.add_argument("--out", default="./skill-doctor-report")
    return p.parse_args()


def resolve_repo(repo_arg) -> Path:
    if repo_arg:
        return Path(repo_arg).expanduser().resolve()
    try:
        res = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, timeout=10
        )
        if res.returncode == 0 and res.stdout.strip():
            return Path(res.stdout.strip()).resolve()
    except (subprocess.TimeoutExpired, OSError):
        pass
    return Path.cwd().resolve()


def resolve_repos(repo_args):
    if not repo_args:
        return [resolve_repo(None)]
    repos = []
    seen = set()
    for value in repo_args:
        repo = resolve_repo(value)
        if repo in seen:
            continue
        seen.add(repo)
        repos.append(repo)
    return repos


def discover_skills(repos, codex_home: Path, extra_dirs, include_global: bool,
                    pi_home: Path = None, grok_home: Path = None, zcode_home: Path = None,
                    claude_home: Path = None):
    if isinstance(repos, Path):
        repos = [repos]
    roots = []
    for repo in repos:
        roots.extend((
            repo / ".agents" / "skills",
            repo / ".claude" / "skills",
            repo / ".codex" / "skills",
        ))
    if include_global:
        roots += [
            codex_home / "skills",
            Path.home() / ".agents" / "skills",
            Path.home() / ".claude" / "skills",
        ]
        for home in (claude_home, pi_home, grok_home, zcode_home):
            if home is not None:
                roots.append(Path(home) / "skills")
    roots += [Path(d).expanduser() for d in extra_dirs]

    skills = {}
    seen_paths = set()
    for root in roots:
        if not root.is_dir():
            continue
        for skill_md in sorted(root.glob("*/SKILL.md")):
            resolved = skill_md.resolve()
            if resolved in seen_paths:
                continue
            seen_paths.add(resolved)
            try:
                content = skill_md.read_bytes()
                text = content.decode("utf-8", errors="replace")
            except OSError:
                continue
            name = skill_md.parent.name
            description = re.search(r"^description:\s*(.+)$", text, re.MULTILINE)
            explicit_only = bool(re.search(r"^disable-model-invocation:\s*true\s*$", text, re.MULTILINE))
            ui_file = skill_md.parent / "agents" / "openai.yaml"
            if ui_file.is_file():
                explicit_only = explicit_only or bool(re.search(
                    r"^\s*allow_implicit_invocation:\s*false\s*$",
                    ui_file.read_text(errors="replace"), re.MULTILINE,
                ))
            copy = {
                "path": str(resolved),
                "sha256": hashlib.sha256(content).hexdigest(),
                "explicit_only": explicit_only,
                "modified_at": datetime.fromtimestamp(skill_md.stat().st_mtime, tz=timezone.utc).isoformat(),
            }
            if name not in skills:
                skills[name] = {
                    "name": name,
                    "description": description.group(1).strip().strip("\"'") if description else "",
                    "copies": [],
                }
            skills[name]["copies"].append(copy)
    return skills


def find_codex_session_files(codex_home: Path, cutoff: datetime):
    files = []
    for sub in ("sessions", "archived_sessions"):
        root = codex_home / sub
        if not root.is_dir():
            continue
        for f in root.rglob("rollout-*.jsonl"):
            try:
                mtime = datetime.fromtimestamp(f.stat().st_mtime, tz=timezone.utc)
            except OSError:
                continue
            if mtime >= cutoff:
                files.append((mtime, f))
    files.sort(key=lambda t: t[0], reverse=True)
    return files


def find_claude_session_files(claude_home: Path, cutoff: datetime, include_subagents: bool):
    """Find recent Claude Code parent sessions and, optionally, sidechains."""
    projects = claude_home / "projects"
    if not projects.is_dir():
        return []

    candidates = list(projects.glob("*/*.jsonl"))
    if include_subagents:
        candidates.extend(projects.glob("*/*/subagents/*.jsonl"))

    files = []
    for path in candidates:
        try:
            mtime = datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)
        except OSError:
            continue
        if mtime >= cutoff:
            files.append((mtime, path))
    files.sort(key=lambda item: item[0], reverse=True)
    return files


def truncate(text: str, limit: int) -> str:
    text = redact_text(text.strip())
    if len(text) <= limit:
        return text
    return text[:limit] + f" …[truncated {len(text) - limit} chars]"


def extract_text(content) -> str:
    if isinstance(content, str):
        return content
    parts = []
    if isinstance(content, list):
        for block in content:
            if isinstance(block, dict):
                t = block.get("text") or block.get("content") or ""
                if isinstance(t, str) and t:
                    parts.append(t)
            elif isinstance(block, str):
                parts.append(block)
    return "\n".join(parts)


def iter_jsonl_records(path: Path):
    return JsonlRecords(path)


class TranscriptEntries(list):
    def __init__(self, entries, locations, source=None):
        super().__init__(entries)
        self.locations = locations
        self.source = source.snapshot() if source else {}
        self.raw_records = source.records if isinstance(source, MemoryRecords) else None


class TranscriptBuffer:
    """Keep bounded excerpts without losing the source location of each entry."""

    def __init__(self, source=None):
        self.source = source
        self._entries = []
        self._tail = None
        self._total = 0

    def append(self, entry):
        location = dict(self.source.location) if self.source else {}
        item = (entry, location)
        self._total += 1
        if self._tail is None:
            self._entries.append(item)
            if len(self._entries) > MAX_TRANSCRIPT_ENTRIES:
                self._tail = deque(self._entries[-TRANSCRIPT_TAIL:], maxlen=TRANSCRIPT_TAIL)
                self._entries = self._entries[:TRANSCRIPT_HEAD]
        else:
            self._tail.append(item)

    def finish(self):
        items = self._entries
        if self._tail is not None:
            omitted = self._total - TRANSCRIPT_HEAD - TRANSCRIPT_TAIL
            items = items + [(("note", f"[... {omitted} entries omitted ...]"), {})] + list(self._tail)
        return TranscriptEntries(
            [entry for entry, _ in items],
            [location for _, location in items],
            self.source,
        )


def detect_skill_candidates(text: str):
    """Extract possible installed-skill names from one tool argument payload."""
    normalized = text.replace("\\", "/")
    candidates = set(re.findall(r"(?:^|/)skills/+([^/]+)/+", normalized))
    candidates.update(re.findall(
        r'"(?:skill|name|bundled_skill_id)"\s*:\s*"([^"]+)"',
        normalized,
    ))
    return candidates


def parse_claude_session(path: Path, skill_names, include_subagents: bool):
    """Normalize one Claude Code JSONL session to the shared transcript shape."""
    try:
        records = iter_jsonl_records(path)
    except OSError:
        return None

    meta = {}
    stats = {
        "user_turns": 0,
        "assistant_turns": 0,
        "tool_calls": 0,
        "repeated_tool_calls": 0,
        "error_outputs": 0,
    }
    entries = TranscriptBuffer(records)
    seen_calls = {}
    seen_assistant_messages = set()
    used_tool_names = set()
    skill_references = set()
    has_code_edit_hint = False
    first_ts = last_ts = None
    is_sidechain = False

    for obj in records:
        ts = obj.get("timestamp")
        if ts:
            first_ts = first_ts or ts
            last_ts = ts

        if obj.get("isSidechain"):
            is_sidechain = True
            if not include_subagents:
                return None

        if not meta and obj.get("sessionId"):
            session_id = obj.get("sessionId")
            agent_id = obj.get("agentId")
            meta = {
                "id": f"{session_id}-{agent_id}" if agent_id else session_id,
                "cwd": obj.get("cwd"),
                "started_at": ts,
                "originator": "claude-code",
                "thread_source": "subagent" if obj.get("isSidechain") else None,
                "cli_version": obj.get("version"),
                "entrypoint": obj.get("entrypoint"),
            }
        elif meta:
            meta["cwd"] = meta.get("cwd") or obj.get("cwd")
            meta["started_at"] = meta.get("started_at") or ts
            meta["cli_version"] = meta.get("cli_version") or obj.get("version")
            meta["entrypoint"] = meta.get("entrypoint") or obj.get("entrypoint")
            agent_id = obj.get("agentId")
            if agent_id and not meta["id"].endswith(f"-{agent_id}"):
                meta["id"] = f"{obj.get('sessionId') or meta['id']}-{agent_id}"

        record_type = obj.get("type")
        message = obj.get("message")
        if record_type not in ("user", "assistant") or not isinstance(message, dict):
            continue

        role = message.get("role") or record_type
        content = message.get("content")
        blocks = content if isinstance(content, list) else [{"type": "text", "text": content}]
        has_user_text = False

        if role == "assistant":
            message_id = message.get("id") or obj.get("uuid")
            if message_id and message_id not in seen_assistant_messages:
                seen_assistant_messages.add(message_id)
                stats["assistant_turns"] += 1

        for block in blocks:
            if not isinstance(block, dict):
                continue
            block_type = block.get("type")
            if block_type == "text":
                text = block.get("text")
                if not isinstance(text, str) or not text or looks_injected(text):
                    continue
                if role == "user":
                    has_user_text = True
                    entries.append(("user", truncate(text, MAX_MSG_CHARS)))
                elif role == "assistant":
                    entries.append(("assistant", truncate(text, MAX_MSG_CHARS)))
            elif block_type == "tool_use":
                stats["tool_calls"] += 1
                name = str(block.get("name") or "unknown")
                args = block.get("input") or {}
                args_text = args if isinstance(args, str) else json.dumps(args, ensure_ascii=False)
                key = hashlib.sha1((name + args_text).encode()).hexdigest()
                seen_calls[key] = seen_calls.get(key, 0) + 1
                if seen_calls[key] > 1:
                    stats["repeated_tool_calls"] += 1
                used_tool_names.add(name)
                skill_references.update(detect_skill_candidates(args_text))
                has_code_edit_hint = has_code_edit_hint or any(
                    hint in args_text for hint in CODE_EDIT_HINTS
                )
                if name == "Skill" and isinstance(args, dict):
                    skill_name = args.get("skill")
                    if skill_name:
                        skill_references.add(skill_name)
                entries.append((f"tool:{name}", truncate(args_text, MAX_TOOL_CHARS)))
            elif block_type == "tool_result":
                result = extract_text(block.get("content"))
                low = result[:2000].lower()
                if block.get("is_error") or "error" in low or "failed" in low or "traceback" in low:
                    stats["error_outputs"] += 1
                entries.append(("output", truncate(result, MAX_TOOL_CHARS)))

        if role == "user" and has_user_text:
            stats["user_turns"] += 1

    if not meta:
        meta = {
            "id": path.stem,
            "cwd": None,
            "started_at": first_ts,
            "originator": "claude-code",
            "thread_source": "subagent" if is_sidechain else None,
        }
    elif is_sidechain:
        meta["thread_source"] = "subagent"

    stats["first_ts"] = first_ts
    stats["last_ts"] = last_ts
    stats["has_code_edits"] = (
        bool(used_tool_names & CLAUDE_CODE_EDIT_TOOLS)
        or has_code_edit_hint
    )
    return meta, stats, entries.finish(), sorted(skill_references)


def looks_injected(text: str) -> bool:
    head = text.lstrip()[:80]
    return head.startswith("<") and any(
        tag in head
        for tag in (
            "environment_context", "user_instructions", "ENVIRONMENT", "system-reminder",
            "permissions", "collaboration_mode", "recommended_plugins", "turn_context",
            "user_info",
        )
    )


def parse_codex_session(path: Path, skill_names, include_subagents: bool):
    """Returns (meta, stats, entries) or None if the session should be skipped."""
    try:
        records = iter_jsonl_records(path)
    except OSError:
        return None

    meta = {}
    stats = {"user_turns": 0, "assistant_turns": 0, "tool_calls": 0, "repeated_tool_calls": 0, "error_outputs": 0}
    entries = TranscriptBuffer(records)
    seen_calls = {}
    skill_references = set()
    has_code_edits = False
    first_ts = last_ts = None
    message_counts = {"user": 0, "assistant": 0}

    for obj in records:
        ltype = obj.get("type")
        payload = obj.get("payload") or {}
        if not isinstance(payload, dict):
            continue
        ts = obj.get("timestamp")
        if ts:
            first_ts = first_ts or ts
            last_ts = ts

        if ltype == "session_meta":
            meta = {
                "id": payload.get("id") or payload.get("session_id") or path.stem,
                "cwd": payload.get("cwd"),
                "started_at": payload.get("timestamp"),
                "originator": payload.get("originator"),
                "thread_source": payload.get("thread_source"),
                "cli_version": payload.get("cli_version"),
            }
            source = payload.get("source")
            is_subagent = payload.get("thread_source") == "subagent" or (
                isinstance(source, dict) and "subagent" in source
            )
            if is_subagent and not include_subagents:
                return None

        elif ltype == "event_msg":
            ptype = payload.get("type")
            if ptype == "user_message":
                stats["user_turns"] += 1
            elif ptype == "agent_message":
                stats["assistant_turns"] += 1

        elif ltype == "response_item":
            ptype = payload.get("type")
            if ptype == "message":
                role = payload.get("role")
                if payload.get("channel") == "analysis":
                    continue
                text = extract_text(payload.get("content"))
                if not text:
                    continue
                if role in message_counts:
                    message_counts[role] += 1
                if role == "user":
                    if looks_injected(text):
                        continue
                    entries.append(("user", truncate(text, MAX_MSG_CHARS)))
                elif role == "assistant":
                    entries.append(("assistant", truncate(text, MAX_MSG_CHARS)))
            elif ptype in ("function_call", "custom_tool_call", "local_shell_call"):
                stats["tool_calls"] += 1
                name = payload.get("name") or ptype
                args = payload.get("arguments") or payload.get("input") or ""
                if not isinstance(args, str):
                    args = json.dumps(args)
                key = hashlib.sha1((name + args).encode()).hexdigest()
                seen_calls[key] = seen_calls.get(key, 0) + 1
                if seen_calls[key] > 1:
                    stats["repeated_tool_calls"] += 1
                skill_references.update(detect_skill_candidates(args))
                has_code_edits = has_code_edits or any(
                    hint in args for hint in CODE_EDIT_HINTS
                )
                entries.append((f"tool:{name}", truncate(args, MAX_TOOL_CHARS)))
            elif ptype in ("function_call_output", "custom_tool_call_output"):
                out = payload.get("output") or ""
                if not isinstance(out, str):
                    out = json.dumps(out)
                low = out[:2000].lower()
                if "error" in low or "failed" in low or "traceback" in low:
                    stats["error_outputs"] += 1
                entries.append(("output", truncate(out, MAX_TOOL_CHARS)))

    if not meta:
        meta = {"id": path.stem, "cwd": None, "started_at": first_ts}

    stats["user_turns"] = stats["user_turns"] or message_counts["user"]
    stats["assistant_turns"] = stats["assistant_turns"] or message_counts["assistant"]
    stats["first_ts"] = first_ts
    stats["last_ts"] = last_ts
    stats["has_code_edits"] = has_code_edits
    return meta, stats, entries.finish(), sorted(skill_references)


def parse_sqlite_timestamp(value):
    if not value:
        return None
    text = str(value).strip().replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def discover_warp_databases(explicit_paths=(), data_dir=None):
    """Find Warp channel databases, preferring explicit paths when provided."""
    candidates = []
    for value in explicit_paths:
        candidates.append(Path(value).expanduser())

    roots = []
    if data_dir:
        roots.append(Path(data_dir).expanduser())
    elif sys.platform == "darwin":
        roots.append(
            Path.home()
            / "Library"
            / "Group Containers"
            / "2BBY89MBSN.dev.warp"
            / "Library"
            / "Application Support"
        )
    elif sys.platform.startswith("linux"):
        xdg_data = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share"))
        roots.extend((xdg_data / "warp-terminal", xdg_data / "warp"))
    elif os.name == "nt" and os.environ.get("APPDATA"):
        roots.append(Path(os.environ["APPDATA"]) / "Warp")

    for root in roots:
        if root.is_file():
            candidates.append(root)
            continue
        candidates.append(root / "warp.sqlite")
        if root.is_dir():
            candidates.extend(root.glob("*/warp.sqlite"))

    databases = []
    seen = set()
    for candidate in candidates:
        try:
            resolved = candidate.resolve()
        except OSError:
            continue
        if resolved in seen or not resolved.is_file():
            continue
        seen.add(resolved)
        databases.append(resolved)
    return sorted(databases)


def open_warp_database(path):
    connection = sqlite3.connect(f"{path.as_uri()}?mode=ro", uri=True, timeout=2)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA query_only = ON")
    return connection


def warp_database_has_sessions(connection):
    row = connection.execute(
        "SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = 'agent_conversations'"
    ).fetchone()
    return row is not None

def sqlite_table_columns(connection, table):
    return {row["name"] for row in connection.execute(f"PRAGMA table_info({table})")}


def find_warp_conversations(databases, cutoff):
    """Return newest copies of Warp conversations across installed channels."""
    newest_by_id = {}
    scanned = 0
    cutoff_text = cutoff.strftime("%Y-%m-%d %H:%M:%S")
    for database in databases:
        connection = None
        try:
            connection = open_warp_database(database)
            if not warp_database_has_sessions(connection):
                continue
            conversation_columns = sqlite_table_columns(connection, "agent_conversations")
            summary_expression = "summary" if "summary" in conversation_columns else "NULL"
            rows = connection.execute(
                f"""
                SELECT conversation_id, conversation_data, last_modified_at,
                       {summary_expression} AS summary
                FROM agent_conversations
                WHERE last_modified_at >= ?
                ORDER BY last_modified_at DESC
                """,
                (cutoff_text,),
            ).fetchall()
        except sqlite3.Error as exc:
            print(f"warning: could not read Warp database {database}: {exc}", file=sys.stderr)
            continue
        finally:
            if connection is not None:
                connection.close()
        scanned += len(rows)
        for row in rows:
            modified_at = parse_sqlite_timestamp(row["last_modified_at"])
            if modified_at is None or modified_at < cutoff:
                continue
            record = {
                "conversation_id": row["conversation_id"],
                "conversation_data": row["conversation_data"],
                "summary": row["summary"],
                "modified_at": modified_at,
                "database": database,
                "channel": database.parent.name,
            }
            existing = newest_by_id.get(record["conversation_id"])
            if existing is None or modified_at > existing["modified_at"]:
                newest_by_id[record["conversation_id"]] = record
    records = sorted(newest_by_id.values(), key=lambda row: row["modified_at"], reverse=True)
    return records, scanned


def load_warp_conversation_data(record):
    """Load task blobs and ai_query fallback metadata for one conversation."""
    connection = open_warp_database(record["database"])
    try:
        task_rows = connection.execute(
            """
            SELECT task
            FROM agent_tasks
            WHERE conversation_id = ?
            ORDER BY id
            """,
            (record["conversation_id"],),
        ).fetchall()
        query_rows = []
        query_columns = sqlite_table_columns(connection, "ai_queries")
        if {"conversation_id", "start_ts"}.issubset(query_columns):
            working_directory_expression = (
                "working_directory" if "working_directory" in query_columns else "NULL"
            )
            query_rows = connection.execute(
                f"""
                SELECT start_ts, {working_directory_expression} AS working_directory
                FROM ai_queries
                WHERE conversation_id = ?
                ORDER BY start_ts
                """,
                (record["conversation_id"],),
            ).fetchall()
    finally:
        connection.close()
    task_blobs = [bytes(row["task"]) for row in task_rows]
    total_bytes = sum(len(blob) for blob in task_blobs)
    if total_bytes > MAX_WARP_CONVERSATION_BYTES:
        raise ProtobufDecodeError(
            f"conversation task snapshot is {total_bytes} bytes "
            f"(limit {MAX_WARP_CONVERSATION_BYTES})"
        )

    first_query_at = None
    working_directory = None
    for row in query_rows:
        first_query_at = first_query_at or parse_sqlite_timestamp(row["start_ts"])
        working_directory = working_directory or row["working_directory"]
    return task_blobs, first_query_at, working_directory


def skill_name_from_reference(reference, skill_names):
    if not reference:
        return None
    candidates = [
        reference.get("name"),
        reference.get("bundled_skill_id"),
    ]
    path = reference.get("path")
    if path:
        skill_path = Path(path)
        candidates.extend((skill_path.parent.name, skill_path.stem))
    return next((name for name in candidates if name in skill_names), None) or next(
        (name for name in candidates if name), None,
    )


def parse_warp_conversation(record, skill_names, include_subagents):
    """Normalize one persisted Warp conversation to the Codex transcript shape."""
    try:
        conversation_data = json.loads(record["conversation_data"] or "{}")
    except (json.JSONDecodeError, TypeError):
        conversation_data = {}
    is_child = bool(
        conversation_data.get("parent_agent_id")
        or conversation_data.get("parent_conversation_id")
    )
    if is_child and not include_subagents:
        return None

    try:
        summary = json.loads(record["summary"] or "{}")
    except (json.JSONDecodeError, TypeError):
        summary = {}

    try:
        task_blobs, first_query_at, query_cwd = load_warp_conversation_data(record)
        tasks = [decode_task(blob) for blob in task_blobs]
    except (OSError, sqlite3.Error, ProtobufDecodeError) as exc:
        print(
            f"warning: could not decode Warp conversation "
            f"{record['conversation_id']} from {record['channel']}: {exc}",
            file=sys.stderr,
        )
        return None

    messages = []
    sequence = 0
    for task in tasks:
        for message in task["messages"]:
            message["_sequence"] = sequence
            sequence += 1
            messages.append(message)
    messages.sort(
        key=lambda message: (
            message.get("order_key") is None,
            message.get("order_key") or (0, 0),
            message["_sequence"],
        )
    )

    stats = {
        "user_turns": 0,
        "assistant_turns": 0,
        "tool_calls": 0,
        "repeated_tool_calls": 0,
        "error_outputs": 0,
    }
    records = MemoryRecords(messages)
    entries = TranscriptBuffer(records)
    seen_calls = {}
    skill_references = set()
    first_ts = last_ts = None
    cwd = summary.get("initial_working_directory") or query_cwd
    has_code_edits = False

    for message in records:
        timestamp = message.get("timestamp")
        if timestamp:
            first_ts = first_ts or timestamp
            last_ts = timestamp
        kind = message["kind"]
        if kind == "user_query":
            text = message.get("text", "")
            cwd = cwd or message.get("cwd")
            if text and not looks_injected(text):
                stats["user_turns"] += 1
                entries.append(("user", truncate(text, MAX_MSG_CHARS)))
        elif kind == "invoke_skill":
            skill_reference = message.get("skill")
            skill_name = skill_name_from_reference(skill_reference, skill_names)
            if skill_name:
                skill_references.add(skill_name)
            if skill_reference:
                entries.append((
                    "skill",
                    truncate(json.dumps(skill_reference, ensure_ascii=False), MAX_TOOL_CHARS),
                ))
            user_query = message.get("user_query") or {}
            text = user_query.get("text", "")
            cwd = cwd or user_query.get("cwd")
            if text and not looks_injected(text):
                stats["user_turns"] += 1
                entries.append(("user", truncate(text, MAX_MSG_CHARS)))
        elif kind == "agent_output":
            text = message.get("text", "")
            if text:
                stats["assistant_turns"] += 1
                entries.append(("assistant", truncate(text, MAX_MSG_CHARS)))
        elif kind == "tool_call":
            stats["tool_calls"] += 1
            name = message.get("name", "unknown")
            payload = message.get("payload", "")
            skill_references.update(detect_skill_candidates(payload))
            key = hashlib.sha1((name + payload).encode()).hexdigest()
            seen_calls[key] = seen_calls.get(key, 0) + 1
            if seen_calls[key] > 1:
                stats["repeated_tool_calls"] += 1
            has_code_edits = has_code_edits or name == "apply_file_diffs"
            skill_reference = message.get("skill")
            skill_name = skill_name_from_reference(skill_reference, skill_names)
            if skill_name:
                skill_references.add(skill_name)
            entries.append((f"tool:{name}", truncate(payload, MAX_TOOL_CHARS)))
            if skill_reference:
                entries.append((
                    "skill",
                    truncate(json.dumps(skill_reference, ensure_ascii=False), MAX_TOOL_CHARS),
                ))
        elif kind == "tool_call_result":
            payload = message.get("payload", "")
            cwd = cwd or message.get("cwd")
            low = payload[:2000].lower()
            if "error" in low or "failed" in low or "traceback" in low:
                stats["error_outputs"] += 1
            entries.append(("output", truncate(payload, MAX_TOOL_CHARS)))

    started_at = first_ts or (first_query_at.isoformat() if first_query_at else None)
    meta = {
        "id": record["conversation_id"],
        "cwd": cwd,
        "started_at": started_at,
        "originator": "warp",
        "thread_source": "subagent" if is_child else None,
        "channel": record["channel"],
    }
    stats["first_ts"] = first_ts
    stats["last_ts"] = last_ts
    stats["has_code_edits"] = has_code_edits
    return meta, stats, entries.finish(), sorted(skill_references)


def find_pi_session_files(pi_home: Path, cutoff: datetime):
    root = pi_home / "sessions"
    if not root.is_dir():
        return []
    files = []
    for path in root.glob("*/*.jsonl"):
        try:
            mtime = datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)
        except OSError:
            continue
        if mtime >= cutoff:
            files.append((mtime, path))
    files.sort(key=lambda item: item[0], reverse=True)
    return files


def parse_pi_session(path: Path, skill_names, include_subagents: bool):
    """Normalize one Pi agent JSONL session to the shared transcript shape.

    Pi has no subagent sessions; include_subagents is accepted for signature
    compatibility with the Claude parser and ignored.
    """
    try:
        records = iter_jsonl_records(path)
    except OSError:
        return None

    meta = {}
    stats = {"user_turns": 0, "assistant_turns": 0, "tool_calls": 0, "repeated_tool_calls": 0, "error_outputs": 0}
    entries = TranscriptBuffer(records)
    seen_calls = {}
    used_tool_names = set()
    skill_references = set()
    has_code_edit_hint = False
    first_ts = last_ts = None

    for obj in records:
        record_type = obj.get("type")
        ts = obj.get("timestamp")
        if ts:
            first_ts = first_ts or ts
            last_ts = ts

        if record_type == "session":
            if not meta:
                meta = {
                    "id": obj.get("id") or path.stem,
                    "cwd": obj.get("cwd"),
                    "started_at": ts,
                    "originator": "pi",
                    "thread_source": None,
                }
            else:
                meta["cwd"] = meta.get("cwd") or obj.get("cwd")
                meta["started_at"] = meta.get("started_at") or ts
            continue

        if record_type != "message":
            continue
        message = obj.get("message")
        if not isinstance(message, dict):
            continue
        role = message.get("role")
        content = message.get("content")
        blocks = content if isinstance(content, list) else [{"type": "text", "text": content}]

        if role == "toolResult":
            message_error = bool(message.get("isError"))
            for block in blocks:
                if not isinstance(block, dict):
                    continue
                result = block.get("text") or ""
                if not isinstance(result, str) or not result:
                    continue
                low = result[:2000].lower()
                if (
                    message_error
                    or block.get("isError")
                    or "error" in low
                    or "failed" in low
                    or "traceback" in low
                ):
                    stats["error_outputs"] += 1
                entries.append(("output", truncate(result, MAX_TOOL_CHARS)))
            continue

        has_user_text = False
        if role == "assistant":
            stats["assistant_turns"] += 1

        for block in blocks:
            if not isinstance(block, dict):
                continue
            block_type = block.get("type")
            if block_type == "text":
                text = block.get("text")
                if not isinstance(text, str) or not text or looks_injected(text):
                    continue
                if role == "user":
                    has_user_text = True
                    entries.append(("user", truncate(text, MAX_MSG_CHARS)))
                elif role == "assistant":
                    entries.append(("assistant", truncate(text, MAX_MSG_CHARS)))
            elif block_type == "toolCall":
                stats["tool_calls"] += 1
                name = str(block.get("name") or "unknown")
                args = block.get("arguments") or {}
                args_text = args if isinstance(args, str) else json.dumps(args, ensure_ascii=False)
                key = hashlib.sha1((name + args_text).encode()).hexdigest()
                seen_calls[key] = seen_calls.get(key, 0) + 1
                if seen_calls[key] > 1:
                    stats["repeated_tool_calls"] += 1
                used_tool_names.add(name)
                skill_references.update(detect_skill_candidates(args_text))
                has_code_edit_hint = has_code_edit_hint or any(
                    hint in args_text for hint in CODE_EDIT_HINTS
                )
                entries.append((f"tool:{name}", truncate(args_text, MAX_TOOL_CHARS)))

        if role == "user" and has_user_text:
            stats["user_turns"] += 1

    if not meta:
        meta = {
            "id": path.stem,
            "cwd": None,
            "started_at": first_ts,
            "originator": "pi",
            "thread_source": None,
        }

    stats["first_ts"] = first_ts
    stats["last_ts"] = last_ts
    stats["has_code_edits"] = (
        bool(used_tool_names & GENERIC_EDIT_TOOLS)
        or has_code_edit_hint
    )
    return meta, stats, entries.finish(), sorted(skill_references)


def find_grok_session_files(grok_home: Path, cutoff: datetime):
    root = grok_home / "sessions"
    if not root.is_dir():
        return []
    files = []
    for path in root.glob("*/*/chat_history.jsonl"):
        try:
            mtime = datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)
        except OSError:
            continue
        if mtime >= cutoff:
            files.append((mtime, path))
    files.sort(key=lambda item: item[0], reverse=True)
    return files


def assistant_tool_calls(message):
    """Extract (name, args_text) pairs from OpenAI-style tool_calls entries."""
    calls = []
    for call in message.get("tool_calls") or []:
        if not isinstance(call, dict):
            continue
        fn = call.get("function") or {}
        name = call.get("name") or fn.get("name") or "unknown"
        args = call.get("arguments")
        if args is None:
            args = fn.get("arguments")
        if not isinstance(args, str):
            args = json.dumps(args, ensure_ascii=False)
        calls.append((str(name), args))
    return calls


def parse_grok_session(path: Path, skill_names, include_subagents: bool):
    """Normalize one Grok Build chat_history.jsonl to the shared transcript shape.

    Grok stores a session as one flat file; subagent activity appears as
    synthetic_reason injections which are skipped, so include_subagents is
    accepted for signature compatibility and ignored.
    """
    try:
        records = iter_jsonl_records(path)
    except OSError:
        return None

    stats = {"user_turns": 0, "assistant_turns": 0, "tool_calls": 0, "repeated_tool_calls": 0, "error_outputs": 0}
    entries = TranscriptBuffer(records)
    seen_calls = {}
    used_tool_names = set()
    skill_references = set()
    has_code_edit_hint = False

    for obj in records:
        record_type = obj.get("type")
        if record_type in ("system", "reasoning", "backend_tool_call"):
            continue
        if obj.get("synthetic_reason"):
            continue

        if record_type == "user":
            text = extract_text(obj.get("content"))
            if not text or looks_injected(text):
                continue
            stats["user_turns"] += 1
            entries.append(("user", truncate(text, MAX_MSG_CHARS)))
        elif record_type == "assistant":
            text = extract_text(obj.get("content"))
            if text:
                stats["assistant_turns"] += 1
                entries.append(("assistant", truncate(text, MAX_MSG_CHARS)))
            for name, args_text in assistant_tool_calls(obj):
                stats["tool_calls"] += 1
                key = hashlib.sha1((name + args_text).encode()).hexdigest()
                seen_calls[key] = seen_calls.get(key, 0) + 1
                if seen_calls[key] > 1:
                    stats["repeated_tool_calls"] += 1
                used_tool_names.add(name)
                skill_references.update(detect_skill_candidates(args_text))
                has_code_edit_hint = has_code_edit_hint or any(
                    hint in args_text for hint in CODE_EDIT_HINTS
                )
                entries.append((f"tool:{name}", truncate(args_text, MAX_TOOL_CHARS)))
        elif record_type == "tool_result":
            result = extract_text(obj.get("content"))
            if not result:
                continue
            low = result[:2000].lower()
            if "error" in low or "failed" in low or "traceback" in low:
                stats["error_outputs"] += 1
            entries.append(("output", truncate(result, MAX_TOOL_CHARS)))

    meta = {
        "id": path.parent.name,
        "cwd": unquote(path.parent.parent.name),
        "started_at": None,
        "originator": "grok",
        "thread_source": None,
    }
    stats["first_ts"] = None
    stats["last_ts"] = None
    stats["has_code_edits"] = (
        bool(used_tool_names & GENERIC_EDIT_TOOLS)
        or has_code_edit_hint
    )
    return meta, stats, entries.finish(), sorted(skill_references)


def find_zcode_session_files(zcode_home: Path, cutoff: datetime):
    root = zcode_home / "cli" / "rollout"
    if not root.is_dir():
        return []
    files = []
    for path in root.glob("model-io-*.jsonl"):
        try:
            mtime = datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)
        except OSError:
            continue
        if mtime >= cutoff:
            files.append((mtime, path))
    files.sort(key=lambda item: item[0], reverse=True)
    return files


def parse_zcode_session(path: Path, skill_names, include_subagents: bool):
    """Normalize one ZCode model-io rollout to the shared transcript shape.

    Model-io logs are request dumps: only the last request's message list is
    reconstructed, so stats describe the final context window rather than the
    full session.
    """
    try:
        records = iter_jsonl_records(path)
    except OSError:
        return None

    messages = None
    request_location = {}
    for obj in records:
        if not isinstance(obj, dict):
            continue
        body = (obj.get("request") or {}).get("body") or {}
        candidate = body.get("messages")
        if isinstance(candidate, list) and candidate:
            messages = candidate
            request_location = dict(records.location)
    if not messages:
        return None

    stats = {"user_turns": 0, "assistant_turns": 0, "tool_calls": 0, "repeated_tool_calls": 0, "error_outputs": 0}
    records.location = request_location
    entries = TranscriptBuffer(records)
    seen_calls = {}
    used_tool_names = set()
    skill_references = set()
    has_code_edit_hint = False

    for message in messages:
        if not isinstance(message, dict):
            continue
        role = message.get("role")
        if role == "user":
            text = extract_text(message.get("content"))
            if not text or looks_injected(text):
                continue
            stats["user_turns"] += 1
            entries.append(("user", truncate(text, MAX_MSG_CHARS)))
        elif role == "assistant":
            text = extract_text(message.get("content"))
            if text:
                stats["assistant_turns"] += 1
                entries.append(("assistant", truncate(text, MAX_MSG_CHARS)))
            for name, args_text in assistant_tool_calls(message):
                stats["tool_calls"] += 1
                key = hashlib.sha1((name + args_text).encode()).hexdigest()
                seen_calls[key] = seen_calls.get(key, 0) + 1
                if seen_calls[key] > 1:
                    stats["repeated_tool_calls"] += 1
                used_tool_names.add(name)
                skill_references.update(detect_skill_candidates(args_text))
                has_code_edit_hint = has_code_edit_hint or any(
                    hint in args_text for hint in CODE_EDIT_HINTS
                )
                entries.append((f"tool:{name}", truncate(args_text, MAX_TOOL_CHARS)))
        elif role == "tool":
            result = extract_text(message.get("content"))
            if not result:
                continue
            low = result[:2000].lower()
            if "error" in low or "failed" in low or "traceback" in low:
                stats["error_outputs"] += 1
            entries.append(("output", truncate(result, MAX_TOOL_CHARS)))

    entries = entries.finish()
    if not entries:
        return None

    meta = {
        "id": path.stem.removeprefix("model-io-"),
        "cwd": None,
        "started_at": None,
        "originator": "zcode",
        "thread_source": None,
    }
    stats["first_ts"] = None
    stats["last_ts"] = None
    stats["has_code_edits"] = (
        bool(used_tool_names & GENERIC_EDIT_TOOLS)
        or has_code_edit_hint
    )
    return meta, stats, entries, sorted(skill_references)


def render_transcript(meta, stats, skill_references, entries) -> str:
    lines = [
        f"# Session {meta.get('id')}",
        f"- cwd: {meta.get('cwd')}",
        f"- started: {meta.get('started_at') or stats.get('first_ts')}",
        f"- skill references: {', '.join(skill_references) or '(none)'}",
        "- Loading and application are not established by references alone.",
        f"- counters: {stats['tool_calls']} tool calls; "
        f"{stats['repeated_tool_calls']} repeated argument signatures; "
        f"{stats['error_outputs']} error-like outputs. These are leads, not verdicts.",
        "- Excerpts may omit context and contain best-effort redactions.",
        "", "## Condensed transcript", "",
    ]
    for index, (role, text) in enumerate(entries):
        location = entries.locations[index] if isinstance(entries, TranscriptEntries) else {}
        record = f"record {location['record']}" if location.get("record") else "location unavailable"
        timestamp = f" @ {location['timestamp']}" if location.get("timestamp") else ""
        lines.extend((f"[{role}; {record}{timestamp}] {text}", ""))
    return "\n".join(lines)


def session_matches_repo(cwd, repo: Path) -> bool:
    """Match a checkout or a verified Git worktree, without basename guesses."""
    if not cwd:
        return False
    path = Path(cwd).expanduser()
    if path.resolve().is_relative_to(repo.resolve()):
        return True
    if not path.is_dir() or not repo.is_dir():
        return False
    common_dirs = []
    for checkout in (path, repo):
        try:
            result = subprocess.run(
                ["git", "-C", str(checkout), "rev-parse", "--git-common-dir"],
                capture_output=True, text=True, timeout=10,
            )
        except (OSError, subprocess.TimeoutExpired):
            return False
        if result.returncode != 0 or not result.stdout.strip():
            return False
        common_dirs.append((checkout / result.stdout.strip()).resolve())
    return common_dirs[0] == common_dirs[1]


def session_matches_repos(cwd, repos) -> bool:
    return any(session_matches_repo(cwd, repo) for repo in repos)


def infer_session_repos(sessions):
    repos = []
    seen = set()
    for session in sessions:
        cwd = session["meta"].get("cwd")
        if not cwd:
            continue
        path = Path(cwd).expanduser()
        if not path.is_dir():
            continue
        try:
            result = subprocess.run(
                ["git", "-C", str(path), "rev-parse", "--show-toplevel"],
                capture_output=True,
                text=True,
                timeout=10,
            )
        except (subprocess.TimeoutExpired, OSError):
            continue
        if result.returncode != 0 or not result.stdout.strip():
            continue
        repo = Path(result.stdout.strip()).resolve()
        if repo in seen:
            continue
        seen.add(repo)
        repos.append(repo)
    return repos


def detect_skills_from_entries(entries, skill_names):
    tool_text = "\n".join(
        text
        for role, text in entries
        if role == "skill" or role.startswith("tool:")
    ).replace("\\", "/")
    detected = set()
    for name in skill_names:
        markers = (
            f"skills/{name}/",
            f"{name}/SKILL.md",
            f'"skill": "{name}"',
            f'"name": "{name}"',
            f'"bundled_skill_id": "{name}"',
        )
        if any(marker in tool_text for marker in markers):
            detected.add(name)
    return detected


def main():
    args = parse_args()
    if args.days < 0 or args.max_sessions < 0:
        print("error: --days and --max-sessions must be nonnegative", file=sys.stderr)
        sys.exit(2)
    if args.all_conversations and args.repo:
        print(
            "error: --all-conversations cannot be combined with --repo",
            file=sys.stderr,
        )
        sys.exit(2)
    if not args.repo:
        args.all_conversations = True
    claude_home = Path(args.claude_home).expanduser()
    codex_home = Path(args.codex_home).expanduser()
    pi_home = Path(args.pi_home).expanduser()
    grok_home = Path(args.grok_home).expanduser()
    zcode_home = Path(args.zcode_home).expanduser()
    out_dir = Path(args.out).expanduser()
    transcripts_dir = out_dir / "transcripts"
    transcripts_dir.mkdir(parents=True, exist_ok=True)

    repos = [] if args.all_conversations else resolve_repos(args.repo)
    skills = discover_skills(
        repos,
        codex_home,
        args.skills_dir,
        args.include_global_skills,
        pi_home=pi_home,
        grok_home=grok_home,
        zcode_home=zcode_home,
        claude_home=claude_home,
    )
    cutoff = (datetime.now(timezone.utc) - timedelta(days=args.days)) if args.days else datetime.min.replace(tzinfo=timezone.utc)

    sessions = []
    in_scope_count = 0
    scanned_count = 0
    sources = {}

    requested_claude = args.harness in ("auto", "all", "claude")
    if requested_claude and (claude_home / "projects").is_dir():
        claude_files = find_claude_session_files(
            claude_home,
            cutoff,
            args.include_subagents,
        )
        sources["claude"] = {
            "home": str(claude_home),
            "records_in_window": len(claude_files),
        }
        scanned_count += len(claude_files)
        for mtime, path in claude_files:
            parsed = parse_claude_session(path, skills.keys(), args.include_subagents)
            if parsed is None:
                continue
            meta, stats, entries, skill_references = parsed
            if not args.all_conversations and not session_matches_repos(
                meta.get("cwd"),
                repos,
            ):
                continue
            in_scope_count += 1
            if stats["assistant_turns"] < 1:
                continue
            sessions.append({
                "harness": "claude",
                "meta": meta,
                "stats": stats,
                "skill_references": skill_references,
                "file": str(path),
                "modified_at": mtime.isoformat(),
                "_entries": entries,
            })
    elif args.harness == "claude":
        print(
            f"error: Claude Code project history not found at {claude_home / 'projects'}",
            file=sys.stderr,
        )
        sys.exit(1)

    requested_codex = args.harness in ("auto", "all", "codex")
    if requested_codex and codex_home.is_dir():
        codex_files = find_codex_session_files(codex_home, cutoff)
        sources["codex"] = {"home": str(codex_home), "records_in_window": len(codex_files)}
        scanned_count += len(codex_files)
        for mtime, path in codex_files:
            parsed = parse_codex_session(path, skills.keys(), args.include_subagents)
            if parsed is None:
                continue
            meta, stats, entries, skill_references = parsed
            if not args.all_conversations and not session_matches_repos(
                meta.get("cwd"),
                repos,
            ):
                continue
            in_scope_count += 1
            if stats["assistant_turns"] < 1:
                continue
            sessions.append({
                "harness": "codex",
                "meta": meta,
                "stats": stats,
                "skill_references": skill_references,
                "file": str(path),
                "modified_at": mtime.isoformat(),
                "_entries": entries,
            })
    elif args.harness == "codex":
        print(f"error: Codex home not found at {codex_home}", file=sys.stderr)
        sys.exit(1)

    requested_warp = args.harness in ("auto", "all", "warp")
    warp_databases = []
    if requested_warp:
        warp_databases = discover_warp_databases(args.warp_db, args.warp_data_dir)
        if warp_databases:
            warp_records, warp_scanned = find_warp_conversations(warp_databases, cutoff)
            sources["warp"] = {
                "databases": [str(path) for path in warp_databases],
                "records_in_window": warp_scanned,
                "records_after_channel_deduplication": len(warp_records),
            }
            scanned_count += warp_scanned
            for record in warp_records:
                parsed = parse_warp_conversation(
                    record,
                    skills.keys(),
                    args.include_subagents,
                )
                if parsed is None:
                    continue
                meta, stats, entries, skill_references = parsed
                if not args.all_conversations and not session_matches_repos(
                    meta.get("cwd"),
                    repos,
                ):
                    continue
                in_scope_count += 1
                if stats["assistant_turns"] < 1:
                    continue
                sessions.append({
                    "harness": "warp",
                    "meta": meta,
                    "stats": stats,
                    "skill_references": skill_references,
                    "file": f"{record['database']}#agent_conversations/"
                            f"{record['conversation_id']}",
                    "modified_at": record["modified_at"].isoformat(),
                    "_entries": entries,
                })
        elif args.harness == "warp":
            print("error: no Warp conversation databases found", file=sys.stderr)
            sys.exit(1)

    requested_pi = args.harness in ("auto", "all", "pi")
    if requested_pi and (pi_home / "sessions").is_dir():
        pi_files = find_pi_session_files(pi_home, cutoff)
        sources["pi"] = {"home": str(pi_home), "records_in_window": len(pi_files)}
        scanned_count += len(pi_files)
        for mtime, path in pi_files:
            parsed = parse_pi_session(path, skills.keys(), args.include_subagents)
            if parsed is None:
                continue
            meta, stats, entries, skill_references = parsed
            if not args.all_conversations and not session_matches_repos(
                meta.get("cwd"),
                repos,
            ):
                continue
            in_scope_count += 1
            if stats["assistant_turns"] < 1:
                continue
            sessions.append({
                "harness": "pi",
                "meta": meta,
                "stats": stats,
                "skill_references": skill_references,
                "file": str(path),
                "modified_at": mtime.isoformat(),
                "_entries": entries,
            })
    elif args.harness == "pi":
        print(f"error: Pi session home not found at {pi_home / 'sessions'}", file=sys.stderr)
        sys.exit(1)

    requested_grok = args.harness in ("auto", "all", "grok")
    if requested_grok and (grok_home / "sessions").is_dir():
        grok_files = find_grok_session_files(grok_home, cutoff)
        sources["grok"] = {"home": str(grok_home), "records_in_window": len(grok_files)}
        scanned_count += len(grok_files)
        for mtime, path in grok_files:
            parsed = parse_grok_session(path, skills.keys(), args.include_subagents)
            if parsed is None:
                continue
            meta, stats, entries, skill_references = parsed
            if not args.all_conversations and not session_matches_repos(
                meta.get("cwd"),
                repos,
            ):
                continue
            in_scope_count += 1
            if stats["assistant_turns"] < 1:
                continue
            sessions.append({
                "harness": "grok",
                "meta": meta,
                "stats": stats,
                "skill_references": skill_references,
                "file": str(path),
                "modified_at": mtime.isoformat(),
                "_entries": entries,
            })
    elif args.harness == "grok":
        print(f"error: Grok Build session home not found at {grok_home / 'sessions'}", file=sys.stderr)
        sys.exit(1)

    requested_zcode = args.harness in ("auto", "all", "zcode")
    if requested_zcode and (zcode_home / "cli" / "rollout").is_dir():
        zcode_files = find_zcode_session_files(zcode_home, cutoff)
        sources["zcode"] = {"home": str(zcode_home), "records_in_window": len(zcode_files)}
        scanned_count += len(zcode_files)
        for mtime, path in zcode_files:
            parsed = parse_zcode_session(path, skills.keys(), args.include_subagents)
            if parsed is None:
                continue
            meta, stats, entries, skill_references = parsed
            if not args.all_conversations and not session_matches_repos(
                meta.get("cwd"),
                repos,
            ):
                continue
            in_scope_count += 1
            if stats["assistant_turns"] < 1:
                continue
            sessions.append({
                "harness": "zcode",
                "meta": meta,
                "stats": stats,
                "skill_references": skill_references,
                "file": str(path),
                "modified_at": mtime.isoformat(),
                "_entries": entries,
            })
    elif args.harness == "zcode":
        print(
            f"error: ZCode model-io rollouts not found at {zcode_home / 'cli' / 'rollout'}",
            file=sys.stderr,
        )
        sys.exit(1)

    if not sources:
        print(
            "error: no supported session source found (Claude Code, Codex, Warp, Pi, Grok, or ZCode)",
            file=sys.stderr,
        )
        sys.exit(1)
    if args.all_conversations:
        repos = infer_session_repos(sessions)
        skills = discover_skills(
            repos,
            codex_home,
            args.skills_dir,
            args.include_global_skills,
            pi_home=pi_home,
            grok_home=grok_home,
            zcode_home=zcode_home,
            claude_home=claude_home,
        )
    installed_skill_names = set(skills)
    sessions.sort(key=lambda session: session["modified_at"], reverse=True)
    reference_counts = {name: 0 for name in skills}
    for index, session in enumerate(sessions):
        entries = session.pop("_entries")
        detected = detect_skills_from_entries(entries, installed_skill_names)
        session["skill_references"] = sorted(
            (set(session["skill_references"]) | detected) & installed_skill_names
        )
        for name in session["skill_references"]:
            reference_counts[name] += 1
        source_tag = hashlib.sha256(session["file"].encode()).hexdigest()[:12]
        session["key"] = f"{session['harness']}:{session['meta']['id']}:{source_tag}"
        session["selected"] = not args.max_sessions or index < args.max_sessions
        session["source"] = entries.source if isinstance(entries, TranscriptEntries) else {}
        if not session["selected"]:
            continue
        if isinstance(entries, TranscriptEntries) and entries.raw_records is not None:
            evidence_dir = out_dir / "evidence"
            evidence_dir.mkdir(exist_ok=True)
            snapshot_path = evidence_dir / f"{source_tag}.jsonl"
            snapshot_path.write_text("".join(
                json.dumps(redact_record(record), ensure_ascii=False) + "\n"
                for record in entries.raw_records
            ), encoding="utf-8")
            reader = JsonlRecords(snapshot_path)
            for _ in reader:
                pass
            session["source"] = {**reader.snapshot(), "original": session["file"]}
        transcript_path = transcripts_dir / f"{source_tag}.md"
        transcript_path.write_text(render_transcript(
            session["meta"], session["stats"], session["skill_references"], entries,
        ), encoding="utf-8")
        session["transcript_path"] = str(transcript_path.resolve())
        session["excerpt_locations"] = entries.locations if isinstance(entries, TranscriptEntries) else []

    catalog_dir = out_dir / "catalog"
    catalog_dir.mkdir(exist_ok=True)
    for skill in skills.values():
        for copy in skill["copies"]:
            snapshot = catalog_dir / f"{copy['sha256']}.md"
            content = Path(copy["path"]).read_bytes()
            if hashlib.sha256(content).hexdigest() != copy["sha256"]:
                raise RuntimeError(f"Skill changed during collection: {copy['path']}; collect again.")
            snapshot.write_text(redact_text(content.decode("utf-8", errors="replace")), encoding="utf-8")
            copy["snapshot_path"] = str(snapshot.resolve())
            copy["snapshot_is_redacted"] = True

    selected_count = sum(session["selected"] for session in sessions)
    inventory = {
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "sources": sources,
        "scope": {
            "conversation_scope": "all_projects" if args.all_conversations else "projects",
            "repos": [str(repo) for repo in repos],
            "days": args.days,
            "include_subagents": args.include_subagents,
            "include_global_skills": args.include_global_skills,
            "max_sessions": args.max_sessions,
            "selection": "newest_first" if args.max_sessions else "all_in_scope",
        },
        "skills": sorted(skills.values(), key=lambda skill: skill["name"]),
        "skill_reference_counts": reference_counts,
        "stats": {
            "records_in_window": scanned_count,
            "sessions_in_scope": in_scope_count,
            "sessions_considered": len(sessions),
            "sessions_selected": selected_count,
            "sessions_excluded_by_cap": len(sessions) - selected_count,
            "skills_found": len(skills),
        },
        "sessions": sessions,
    }
    (out_dir / "inventory.json").write_text(json.dumps(inventory, indent=2), encoding="utf-8")
    print(f"Collected {selected_count} sessions from {len(sources)} source(s); {len(skills)} skill names.")
    if args.max_sessions:
        print("The newest-first cap is explicit; this sample is not a population usage estimate.")


if __name__ == "__main__":
    main()
