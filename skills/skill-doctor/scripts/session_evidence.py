"""Keep transcript excerpts traceable to their source records."""

import hashlib
import json
import re
from pathlib import Path


SECRET_FIELD = re.compile(
    r"(?:^|[_-])(?:password|passwd|secret|token|api[_-]?key|authorization)(?:$|[_-])",
    re.IGNORECASE,
)
SECRET_ASSIGNMENT = re.compile(
    r"(?i)(\b[\w-]*(?:password|passwd|secret|token|api[_-]?key)[\w-]*"
    r"[\"']?\s*[=:]\s*)(\"[^\"]*\"|'[^']*'|[^\s,;}]+)"
)
BEARER = re.compile(r"(?i)\bBearer\s+[A-Za-z0-9._~+/=-]+")
KNOWN_TOKEN = re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|sk-[A-Za-z0-9_-]{20,})\b")


def redact_text(text):
    """Remove common credential shapes; this is not a complete secret detector."""
    text = BEARER.sub("Bearer [REDACTED]", text)
    text = KNOWN_TOKEN.sub("[REDACTED]", text)
    return SECRET_ASSIGNMENT.sub(r"\1[REDACTED]", text)


def redact_record(value):
    if isinstance(value, dict):
        if value.get("type") in {"reasoning", "thinking", "redacted_thinking"} or value.get("channel") == "analysis":
            return {"omitted": "private reasoning"}
        return {
            key: "[REDACTED]" if SECRET_FIELD.search(key) else redact_record(item)
            for key, item in value.items()
            if key not in {"thinking", "reasoning", "encrypted_content"}
        }
    if isinstance(value, list):
        return [redact_record(item) for item in value]
    if isinstance(value, str):
        return redact_text(value)
    return value


class JsonlRecords:
    """Stream records while retaining physical line numbers and a content digest."""

    def __init__(self, path):
        self.path = Path(path)
        self.stream = self.path.open("rb")
        self.digest = hashlib.sha256()
        self.bytes_read = 0
        self.record_count = 0
        self.invalid_records = []
        self.location = {}

    def __iter__(self):
        with self.stream:
            for number, line in enumerate(self.stream, 1):
                self.digest.update(line)
                self.bytes_read += len(line)
                self.record_count = number
                try:
                    record = json.loads(line)
                except (ValueError, UnicodeDecodeError):
                    self.invalid_records.append(number)
                    continue
                if not isinstance(record, dict):
                    self.invalid_records.append(number)
                    continue
                self.location = {"record": number, "timestamp": record.get("timestamp")}
                yield record

    def snapshot(self):
        return {
            "format": "jsonl",
            "path": str(self.path.resolve()),
            "sha256": self.digest.hexdigest(),
            "bytes": self.bytes_read,
            "records": self.record_count,
            "invalid_records": self.invalid_records,
        }


class MemoryRecords:
    """Give decoded database messages the same record addressing as JSONL."""

    def __init__(self, records):
        self.records = records
        self.location = {}

    def __iter__(self):
        for number, record in enumerate(self.records, 1):
            self.location = {"record": number, "timestamp": record.get("timestamp")}
            yield record

    def snapshot(self):
        return {"format": "decoded_messages", "records": len(self.records)}


def verify_snapshot(source):
    """Allow appended records, but reject changes to the collected prefix."""
    digest = hashlib.sha256()
    remaining = source["bytes"]
    with Path(source["path"]).open("rb") as stream:
        while remaining:
            chunk = stream.read(min(remaining, 1024 * 1024))
            if not chunk:
                raise ValueError("The source is shorter than its collected snapshot; recollect it.")
            digest.update(chunk)
            remaining -= len(chunk)
    if digest.hexdigest() != source["sha256"]:
        raise ValueError("The collected source records changed; recollect before using them.")


def read_record_range(source, first, last):
    verify_snapshot(source)
    if first < 1 or last < first or last > source["records"]:
        raise ValueError("Requested records are outside the collected snapshot.")
    result = []
    with Path(source["path"]).open("rb") as stream:
        remaining = source["bytes"]
        number = 0
        while remaining and number < last:
            line = stream.readline(remaining)
            remaining -= len(line)
            number += 1
            if number < first:
                continue
            try:
                record = redact_record(json.loads(line))
            except (ValueError, UnicodeDecodeError):
                record = {"unreadable_record": True}
            result.append({"record": number, "value": record})
    return result
