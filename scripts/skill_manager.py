#!/usr/bin/env python3
"""Import, validate, and update vendored agent skills."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"
LOCKFILE = ROOT / "skill-sources.json"
CACHE = ROOT / ".cache" / "skill-sources"
NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
# Skills stay portable across harnesses: no Cursor paths, task-tool
# parameters, or pinned model names.
COUPLING_PATTERN = re.compile(
    r"\.cursor/|\.mdc\b|cursor-team-kit|agent-transcripts|subagent_type|run_in_background"
    r"|\b(?:grok|gpt|claude-(?:opus|sonnet|haiku))-\d"
)
FETCHED_REPOSITORIES: set[str] = set()


class SkillError(RuntimeError):
    pass


def run(*args: str, cwd: Path | None = None, capture: bool = True) -> str:
    result = subprocess.run(
        args,
        cwd=cwd,
        check=False,
        text=True,
        stdout=subprocess.PIPE if capture else None,
        stderr=subprocess.PIPE if capture else None,
    )
    if result.returncode != 0:
        detail = (result.stderr or result.stdout or "command failed").strip()
        raise SkillError(f"{' '.join(args)}: {detail}")
    return (result.stdout or "").strip()


def load_lockfile() -> dict:
    try:
        data = json.loads(LOCKFILE.read_text())
    except (OSError, json.JSONDecodeError) as error:
        raise SkillError(f"Cannot read {LOCKFILE}: {error}") from error
    if data.get("version") != 1 or not isinstance(data.get("skills"), dict):
        raise SkillError("skill-sources.json must contain version 1 and a skills object")
    return data


def save_lockfile(data: dict) -> None:
    rendered = json.dumps(data, indent=2, sort_keys=True) + "\n"
    temporary = LOCKFILE.with_suffix(".json.tmp")
    temporary.write_text(rendered)
    temporary.replace(LOCKFILE)


def cache_path(repository: str) -> Path:
    key = hashlib.sha256(repository.encode()).hexdigest()[:16]
    return CACHE / f"{key}.git"


def ensure_cache(repository: str, offline: bool) -> Path:
    target = cache_path(repository)
    if not target.exists():
        if offline:
            raise SkillError(f"No cached clone for {repository}")
        target.parent.mkdir(parents=True, exist_ok=True)
        run("git", "clone", "--mirror", repository, str(target))
    elif not offline and repository not in FETCHED_REPOSITORIES:
        run("git", "remote", "update", "--prune", cwd=target)
    FETCHED_REPOSITORIES.add(repository)
    return target


def git_value(cache: Path, revision: str) -> str:
    return run("git", "rev-parse", revision, cwd=cache)


def export_directory(cache: Path, commit: str, source_path: str, target: Path) -> Path:
    archive = subprocess.Popen(
        ["git", "archive", commit, source_path],
        cwd=cache,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert archive.stdout is not None
    extracted = subprocess.run(
        ["tar", "-x", "-C", str(target)],
        stdin=archive.stdout,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    archive.stdout.close()
    archive_error = archive.stderr.read().decode().strip() if archive.stderr else ""
    archive_status = archive.wait()
    if archive_status or extracted.returncode:
        detail = archive_error or extracted.stderr.decode().strip()
        raise SkillError(f"Could not export {source_path} at {commit}: {detail}")
    exported = target / source_path
    if not (exported / "SKILL.md").is_file():
        raise SkillError(f"{source_path} does not contain SKILL.md at {commit}")
    return exported


def directory_digest(path: Path) -> str:
    digest = hashlib.sha256()
    for item in sorted(path.rglob("*")):
        relative = item.relative_to(path).as_posix().encode()
        digest.update(relative + b"\0")
        if item.is_symlink():
            digest.update(b"link\0" + os.readlink(item).encode())
        elif item.is_file():
            mode = stat.S_IMODE(item.stat().st_mode)
            digest.update(f"file:{mode:o}\0".encode())
            digest.update(item.read_bytes())
    return digest.hexdigest()


def source_matches(name: str, record: dict, cache: Path) -> bool:
    destination = SKILLS / name
    if not destination.is_dir():
        return False
    with tempfile.TemporaryDirectory() as temporary:
        source = export_directory(
            cache, record["commit"], record["path"], Path(temporary)
        )
        return directory_digest(destination) == directory_digest(source)


def parse_github_url(value: str) -> tuple[str, str | None, str | None]:
    parsed = urlparse(value)
    if parsed.scheme not in {"http", "https"} or parsed.netloc != "github.com":
        raise SkillError("Import expects an https://github.com URL")
    parts = [part for part in parsed.path.split("/") if part]
    if len(parts) < 2:
        raise SkillError("GitHub URL must include an owner and repository")
    owner, repository_name = parts[:2]
    repository_name = repository_name.removesuffix(".git")
    repository = f"https://github.com/{owner}/{repository_name}.git"
    ref = source_path = None
    if len(parts) > 2:
        if parts[2] not in {"tree", "blob"} or len(parts) < 5:
            raise SkillError("Use a repository URL or a GitHub tree/blob URL")
        ref = parts[3]
        path_parts = parts[4:]
        if parts[2] == "blob" and path_parts[-1] == "SKILL.md":
            path_parts.pop()
        source_path = "/".join(path_parts)
    return repository, ref, source_path


def default_ref(repository: str) -> str:
    output = run("git", "ls-remote", "--symref", repository, "HEAD")
    match = re.search(r"ref: refs/heads/(\S+)\s+HEAD", output)
    if not match:
        raise SkillError(f"Could not determine the default branch for {repository}")
    return match.group(1)


def validate_record(name: str, record: object) -> list[str]:
    if not isinstance(record, dict):
        return [f"{name}: source record must be an object"]
    errors = []
    for field in ("repository", "path", "ref", "commit", "mode"):
        if not isinstance(record.get(field), str) or not record[field]:
            errors.append(f"{name}: missing {field}")
    if record.get("mode") not in {"tracked", "forked"}:
        errors.append(f"{name}: mode must be tracked or forked")
    if not re.fullmatch(r"[0-9a-f]{40}", str(record.get("commit", ""))):
        errors.append(f"{name}: commit must be a full 40-character SHA")
    return errors


def frontmatter_name(skill_file: Path) -> str | None:
    text = skill_file.read_text(errors="replace")
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    if end == -1:
        return None
    match = re.search(r"^name:\s*['\"]?([^'\"\s]+)", text[4:end], re.MULTILINE)
    return match.group(1) if match else None


def coupling_errors(skill: Path) -> list[str]:
    errors = []
    for item in sorted(skill.rglob("*")):
        if item.name == "THIRD_PARTY_NOTICES.md" or item.suffix not in {".md", ".yaml", ".sh"}:
            continue
        if not item.is_file():
            continue
        for number, line in enumerate(item.read_text(errors="replace").splitlines(), 1):
            match = COUPLING_PATTERN.search(line)
            if match:
                location = item.relative_to(SKILLS).as_posix()
                errors.append(f"{location}:{number}: harness-specific {match.group(0)!r}")
    return errors


def command_import(args: argparse.Namespace) -> None:
    repository, url_ref, url_path = parse_github_url(args.url)
    ref = args.ref or url_ref or default_ref(repository)
    source_path = args.path or url_path
    if not source_path:
        raise SkillError("Pass a GitHub tree URL or provide --path")
    cache = ensure_cache(repository, args.offline)
    commit = git_value(cache, f"refs/heads/{ref}")
    name = args.name or Path(source_path).name
    if not NAME_PATTERN.fullmatch(name):
        raise SkillError(f"Invalid skill name: {name}")
    destination = SKILLS / name
    if destination.exists():
        raise SkillError(f"{name} already exists; update or rename it explicitly")
    with tempfile.TemporaryDirectory() as temporary:
        source = export_directory(cache, commit, source_path, Path(temporary))
        shutil.copytree(source, destination, symlinks=True)
    data = load_lockfile()
    data["skills"][name] = {
        "repository": repository,
        "path": source_path,
        "ref": ref,
        "commit": commit,
        "mode": "tracked",
    }
    save_lockfile(data)
    print(f"Imported {name} from {repository}@{commit[:12]}")


def update_status(name: str, record: dict, offline: bool) -> tuple[Path, str, bool]:
    cache = ensure_cache(record["repository"], offline)
    latest = git_value(cache, f"refs/heads/{record['ref']}")
    old_tree = git_value(cache, f"{record['commit']}:{record['path']}")
    new_tree = git_value(cache, f"{latest}:{record['path']}")
    return cache, latest, old_tree != new_tree


def command_check_updates(args: argparse.Namespace) -> None:
    data = load_lockfile()
    updates = 0
    for name, record in sorted(data["skills"].items()):
        errors = validate_record(name, record)
        if errors:
            print("\n".join(errors), file=sys.stderr)
            updates += 1
            continue
        _, latest, changed = update_status(name, record, args.offline)
        if changed:
            updates += 1
            suffix = "manual merge required" if record["mode"] == "forked" else "update available"
            print(f"{name}: {record['commit'][:12]} -> {latest[:12]} ({suffix})")
    if updates == 0:
        print("All imported skills are current.")


def print_source_diff(cache: Path, record: dict, latest: str) -> None:
    subprocess.run(
        ["git", "diff", "--no-ext-diff", record["commit"], latest, "--", record["path"]],
        cwd=cache,
        check=False,
    )


def replace_skill(name: str, cache: Path, commit: str, source_path: str) -> None:
    destination = SKILLS / name
    with tempfile.TemporaryDirectory(dir=SKILLS) as temporary:
        source = export_directory(cache, commit, source_path, Path(temporary))
        replacement = Path(temporary) / name
        shutil.copytree(source, replacement, symlinks=True)
        backup = Path(temporary) / f"{name}.backup"
        destination.rename(backup)
        try:
            replacement.rename(destination)
        except Exception:
            backup.rename(destination)
            raise


def command_update(args: argparse.Namespace) -> None:
    data = load_lockfile()
    record = data["skills"].get(args.name)
    if not record:
        raise SkillError(f"{args.name} is local or unknown; it has no source record")
    errors = validate_record(args.name, record)
    if errors:
        raise SkillError("; ".join(errors))
    cache, latest, changed = update_status(args.name, record, args.offline)
    if not changed:
        print(f"{args.name} is current.")
        return
    print_source_diff(cache, record, latest)
    if not args.apply:
        print(f"Preview only. Run scripts/update-skill {args.name} --apply to update.")
        return
    if record["mode"] == "forked":
        raise SkillError(f"{args.name} is forked; merge the upstream diff manually")
    if not source_matches(args.name, record, cache):
        raise SkillError(f"{args.name} differs from its imported revision; mark it forked or merge manually")
    replace_skill(args.name, cache, latest, record["path"])
    record["commit"] = latest
    save_lockfile(data)
    print(f"Updated {args.name} to {latest[:12]}")


def command_check(args: argparse.Namespace) -> None:
    data = load_lockfile()
    errors = []
    directories = {path.name: path for path in SKILLS.iterdir() if path.is_dir()}
    for name, path in sorted(directories.items()):
        if not NAME_PATTERN.fullmatch(name):
            errors.append(f"{name}: directory name is not kebab-case")
        skill_file = path / "SKILL.md"
        if not skill_file.is_file():
            errors.append(f"{name}: missing SKILL.md")
            continue
        declared_name = frontmatter_name(skill_file)
        if declared_name != name:
            errors.append(f"{name}: frontmatter name is {declared_name!r}")
        errors.extend(coupling_errors(path))
    for name, record in sorted(data["skills"].items()):
        errors.extend(validate_record(name, record))
        if name not in directories:
            errors.append(f"{name}: source record has no skill directory")
            continue
        if args.sources and isinstance(record, dict) and not validate_record(name, record):
            cache = ensure_cache(record["repository"], args.offline)
            if record["mode"] == "tracked" and not source_matches(name, record, cache):
                errors.append(f"{name}: tracked copy differs from its imported revision")
    install = Path.home() / ".agents" / "skills"
    expected = SKILLS.resolve()
    if not install.is_symlink() or install.resolve() != expected:
        errors.append(f"{install} must be a symlink to {expected}")
    if errors:
        raise SkillError("\n".join(errors))
    print(f"Validated {len(directories)} skills ({len(data['skills'])} imported).")


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    commands = result.add_subparsers(dest="command", required=True)

    import_parser = commands.add_parser("import")
    import_parser.add_argument("url")
    import_parser.add_argument("--path")
    import_parser.add_argument("--ref")
    import_parser.add_argument("--name")
    import_parser.add_argument("--offline", action="store_true")
    import_parser.set_defaults(handler=command_import)

    updates_parser = commands.add_parser("check-updates")
    updates_parser.add_argument("--offline", action="store_true")
    updates_parser.set_defaults(handler=command_check_updates)

    update_parser = commands.add_parser("update")
    update_parser.add_argument("name")
    update_parser.add_argument("--apply", action="store_true")
    update_parser.add_argument("--offline", action="store_true")
    update_parser.set_defaults(handler=command_update)

    check_parser = commands.add_parser("check")
    check_parser.add_argument("--sources", action="store_true")
    check_parser.add_argument("--offline", action="store_true")
    check_parser.set_defaults(handler=command_check)
    return result


def main() -> int:
    try:
        args = parser().parse_args()
        args.handler(args)
    except SkillError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
