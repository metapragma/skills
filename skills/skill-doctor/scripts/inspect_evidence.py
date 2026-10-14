#!/usr/bin/env python3
"""Retrieve a redacted record range from a collected session snapshot."""

import argparse
import json
import sys
from pathlib import Path

from session_evidence import read_record_range


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inventory", type=Path)
    parser.add_argument("--session", required=True, help="session key from inventory.json")
    parser.add_argument("--record", type=int, required=True)
    parser.add_argument("--context", type=int, default=2)
    parser.add_argument("--max-chars", type=int, default=12000, help="output limit; 0 disables it")
    args = parser.parse_args()
    if args.record < 1 or args.context < 0 or args.max_chars < 0:
        parser.error("record must be positive; context and max-chars must be nonnegative")
    try:
        inventory = json.loads(args.inventory.read_text(encoding="utf-8"))
        session = next((item for item in inventory["sessions"] if item["key"] == args.session), None)
        if session is None:
            raise ValueError("Session key was not found in this inventory.")
        source = session["source"]
        if not 1 <= args.record <= source["records"]:
            raise ValueError("The requested record is outside the collected snapshot.")
        records = read_record_range(
            source,
            max(1, args.record - args.context),
            min(source["records"], args.record + args.context),
        )
        output = json.dumps(records, indent=2, ensure_ascii=False)
        if args.max_chars and len(output) > args.max_chars:
            output = output[:args.max_chars] + "\n[output truncated; increase --max-chars for needed context]"
        print(output)
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
