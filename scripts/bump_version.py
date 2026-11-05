#!/usr/bin/env python3
"""Bump atCGS's release version and sync it into every file that mirrors it.

    pixi run bump-version minor             # 1.8.0-alpha -> 1.9.0-alpha
    pixi run bump-version patch --dry-run   # print the plan, write nothing
    pixi run bump-version major --stage beta

**This script lives in atCGS's private mount** (`.agent/.local/.dev`, branch
`cgs_CGS-ALPHA` of `flipoyo/.dev`), not in the public atCGS repository: a public
checkout, a project's read-only gate included, cannot cut a release (DevSpec
Versioning.md §6). The level is the caller's judgement against the public
interface stated in `atcgs-versioning.md` next to this file; nothing here
computes it.

`pixi.toml` `[workspace] version` is the reference. The same value is written into
`@cgs/pixi.toml`, `atcgs/__init__.py` `__version__`, `spec/contracts.toml` (header
and `[contract] version`), the README title and two lines of ALPHA.md. Every file
is read and rewritten in memory first; a missing file or a field found other than
exactly once stops the bump with nothing on disk changed.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

# .agent/.local/.dev/scripts/bump_version.py -> the atCGS root
ROOT = Path(__file__).resolve().parents[4]
SEMVER = re.compile(r"(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)(?:-(?P<stage>[0-9A-Za-z.-]+))?")


@dataclass(frozen=True)
class Target:
    path: str
    pattern: str  # must contain {v}: the current version, escaped

    def rewrite(self, text: str, old: str, new: str) -> str:
        regex = re.compile(self.pattern.format(v=re.escape(old)), re.M)
        found = regex.findall(text)
        if len(found) != 1:
            raise SystemExit(f"bump-version: {self.path}: expected one match of {self.pattern!r}, found {len(found)}; nothing written")
        return regex.sub(lambda m: m.group(0).replace(old, new), text)


TARGETS = (
    Target("pixi.toml", r'^version = "{v}"'),
    Target("@cgs/pixi.toml", r'^version = "{v}"'),
    Target("atcgs/__init__.py", r'^__version__ = "{v}"'),
    Target("spec/contracts.toml", r"^# atCGS {v} "),
    Target("spec/contracts.toml", r'^version = "{v}"'),
    Target("README.md", r"^# atCGS — ComplexGraphSync {v}$"),
    Target("ALPHA.md", r"^Inner version: `{v}`"),
    Target("ALPHA.md", r"# ComplexGraphSync {v} \(local"),
)


def current(root: Path = ROOT) -> str:
    match = re.search(r'^version = "([^"]+)"', (root / "pixi.toml").read_text(encoding="utf-8"), re.M)
    if not match:
        raise SystemExit("bump-version: no [workspace] version in pixi.toml")
    return match.group(1)


def next_version(old: str, level: str, stage: str | None = None) -> str:
    parts = SEMVER.fullmatch(old)
    if not parts:
        raise SystemExit(f"bump-version: {old!r} is not SemVer")
    major, minor, patch = (int(parts[k]) for k in ("major", "minor", "patch"))
    if level == "major":
        major, minor, patch = major + 1, 0, 0
    elif level == "minor":
        minor, patch = minor + 1, 0
    elif level == "patch":
        patch += 1
    else:
        raise SystemExit(f"bump-version: level is major, minor or patch, not {level!r}")
    label = parts["stage"] if stage is None else stage
    return f"{major}.{minor}.{patch}" + (f"-{label}" if label else "")


def plan(old: str, new: str, root: Path = ROOT) -> dict[Path, str]:
    """Every rewritten file's new text, all computed before any is written."""
    texts: dict[Path, str] = {}
    for target in TARGETS:
        path = root / target.path
        if not path.is_file():
            raise SystemExit(f"bump-version: {target.path} is missing; nothing written")
        texts[path] = target.rewrite(texts.get(path, path.read_text(encoding="utf-8")), old, new)
    return texts


def write(texts: dict[Path, str]) -> None:
    drafts = []
    for path, text in texts.items():
        draft = path.with_name(f".{path.name}.bump")
        draft.write_text(text, encoding="utf-8")
        drafts.append((draft, path))
    for draft, path in drafts:
        os.replace(draft, path)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("level", choices=("major", "minor", "patch"))
    parser.add_argument("--stage", help="pre-release label (default: keep the current one, e.g. alpha); '' drops it")
    parser.add_argument("--dry-run", action="store_true", help="print the plan, write nothing")
    args = parser.parse_args(argv)
    old = current()
    new = next_version(old, args.level, args.stage)
    texts = plan(old, new)
    print(f"{old} -> {new}")
    for path in texts:
        print(f"  {path.relative_to(ROOT)}")
    if args.dry_run:
        print("dry run: nothing written")
        return 0
    write(texts)
    print(f"written; commit subject: cgs-{new} …")
    return 0


if __name__ == "__main__":
    sys.exit(main())
