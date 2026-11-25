#!/usr/bin/env python3
"""CaWaQS versioning, private to the developer's workspace (BuildSemVerAgenticC §3.3).

    pixi run bump-version minor [--dry-run]     # CaWaQS SemVer: 4.1.3 -> 4.2.0, in every copy
    pixi run bump-build libaq [--major] [--dry-run]   # a library's build: 0.74 -> 0.75
    pixi run check-version [--range A..B]       # every copy agrees; a range moves the versions it should

Names follow ComplexGitSync (bump-version, bump-build, check-version, --dry-run, output ``old -> new``).
``pixi.toml`` ``[workspace] version`` is the one SemVer of CaWaQS. Its copies: ``src/param_caw.h`` NVERSION_CAW (a string),
``src/Makefile`` V_CAW (unquoted), ``CITATION.cff`` and the README badge and sentence. A library's build (``MAJOR.XX``) has one
source, its own ``src/Makefile`` ``V_xx`` and its ``VERSION_xx`` define; cawaqs's ``src/Makefile`` repeats it for a plain make.
Every file is computed in memory first: a field found other than exactly once stops with nothing written.
The libraries are found from the ``src/lib*`` directories; nothing here lists them.
"""

from __future__ import annotations

import argparse
import datetime
import os
import re
import subprocess
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]  # .agent/.local/.dev/scripts/versioning.py -> the cawaqs root
SEMVER = re.compile(r"(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)")
BUILD = re.compile(r"(\d+)\.(\d{2})")
ANY = r"[0-9][0-9A-Za-z.+]*"


class VersioningError(SystemExit):
    """A stop with nothing written."""

    def __init__(self, message: str) -> None:
        super().__init__(f"versioning: {message}; nothing written")


@dataclass(frozen=True)
class Target:
    """One place a version is written: a file and a regex holding ``{v}`` (the version)."""

    path: str
    pattern: str
    section: str | None = None  # a TOML table the line must be in

    def _span(self, text: str) -> tuple[int, int]:
        if self.section is None:
            return 0, len(text)
        head = re.search(rf"^\[{re.escape(self.section)}\]\s*$", text, re.M)
        if not head:
            raise VersioningError(f"{self.path}: no [{self.section}] table")
        nxt = re.compile(r"^\[", re.M).search(text, head.end())
        return head.end(), nxt.start() if nxt else len(text)

    def find(self, text: str, version: str | None = None) -> list[str]:
        start, end = self._span(text)
        regex = self.pattern.format(v=re.escape(version) if version else f"({ANY})")
        return re.findall(regex, text[start:end], re.M)

    def rewrite(self, text: str, old: str, new: str) -> str:
        start, end = self._span(text)
        regex = re.compile(self.pattern.format(v=re.escape(old)), re.M)
        if len(regex.findall(text[start:end])) != 1:
            raise VersioningError(f"{self.path}: expected one match of {self.pattern!r} for {old}")
        part = regex.sub(lambda m: m.group(0).replace(old, new), text[start:end])
        return text[:start] + part + text[end:]


REFERENCE = Target("pixi.toml", r'^version = "{v}"', "workspace")
SEMVER_COPIES = (
    Target("src/param_caw.h", r'^#define NVERSION_CAW "{v}"'),
    Target("src/Makefile", r"^V_CAW={v}[ \t]*$"),
    Target("CITATION.cff", r"^version: '{v}'"),
    Target("README.md", r"Current_version-{v}-orange"),
    Target("README.md", r"the SemVer in `pixi\.toml` \(`{v}`\)"),
)


def _read(root: Path, rel: str) -> str:
    return (root / rel).read_text(encoding="utf-8")


def current(root: Path = ROOT) -> str:
    found = REFERENCE.find(_read(root, REFERENCE.path))
    if len(found) != 1 or not SEMVER.fullmatch(found[0]):
        raise VersioningError('pixi.toml needs exactly one SemVer version = "..." in [workspace]')
    return found[0]


def next_version(old: str, level: str) -> str:
    parts = SEMVER.fullmatch(old)
    if not parts:
        raise VersioningError(f"{old!r} is not SemVer")
    major, minor, patch = (int(p) for p in parts.groups())
    moved = {"patch": (major, minor, patch + 1), "minor": (major, minor + 1, 0), "major": (major + 1, 0, 0)}.get(level)
    if moved is None:
        raise VersioningError(f"level is major, minor or patch, not {level!r}")
    return ".".join(map(str, moved))


def next_build(old: str, major: bool = False) -> str:
    parts = BUILD.fullmatch(old)
    if not parts:
        raise VersioningError(f"{old!r} is not a build MAJOR.XX")
    number, build = int(parts[1]), int(parts[2])
    if major:
        return f"{number + 1}.00"
    if build >= 99:
        raise VersioningError(f"build {old} cannot go over .99: use --major")
    return f"{number}.{build + 1:02d}"


def plan_version(old: str, new: str, root: Path = ROOT, today: str | None = None) -> dict[Path, str]:
    texts: dict[Path, str] = {}
    for target in (REFERENCE, *SEMVER_COPIES):
        path = root / target.path
        texts[path] = target.rewrite(texts.get(path) or path.read_text(encoding="utf-8"), old, new)
    cff = root / "CITATION.cff"
    stamp = today or datetime.date.today().isoformat()
    texts[cff], count = re.subn(r"^date-released: '[^']*'", f"date-released: '{stamp}'", texts[cff], flags=re.M)
    if count != 1:
        raise VersioningError("CITATION.cff: expected one date-released")
    return texts


@dataclass(frozen=True)
class Library:
    name: str  # libaq
    acronym: str  # AQ
    dir: Path
    build: str
    header: Path | None  # the file holding its VERSION_xx define, if any

    @property
    def makefile(self) -> Path:
        return self.dir / "src" / "Makefile"


def libraries(root: Path = ROOT) -> list[Library]:
    found = []
    for lib in sorted((root / "src").glob("lib*")):
        makefile = lib / "src" / "Makefile"
        if not makefile.is_file():
            continue
        match = re.search(r"^V_([A-Z]+)=(\d+\.\d{2})\s*$", makefile.read_text(encoding="utf-8", errors="replace"), re.M)
        if not match:
            continue
        acr = match[1]
        header = next((h for h in sorted((lib / "src").glob("*.h")) if re.search(rf"^#define VERSION_{acr} ", h.read_text(encoding="utf-8", errors="replace"), re.M)), None)
        found.append(Library(lib.name, acr, lib, match[2], header))
    return found


def library(name: str, root: Path = ROOT) -> Library:
    wanted = name if name.startswith("lib") else f"lib{name}"
    for lib in libraries(root):
        if lib.name == wanted:
            return lib
    raise VersioningError(f"no library {name!r} under src/ (known: {', '.join(l.name for l in libraries(root))})")


def plan_build(lib: Library, new: str, root: Path = ROOT) -> dict[Path, str]:
    texts: dict[Path, str] = {}
    targets = [(lib.makefile, Target("", rf"^V_{lib.acronym}={{v}}[ \t]*$")), (root / "src/Makefile", Target("", rf"^V_{lib.acronym}={{v}}[ \t]*$"))]
    if lib.header:
        targets.append((lib.header, Target("", rf"^#define VERSION_{lib.acronym} {{v}}")))
    for path, target in targets:
        text = texts.get(path) or path.read_text(encoding="utf-8", errors="replace")
        if path == root / "src/Makefile" and not target.find(text, lib.build):
            continue  # cawaqs does not use this library
        if path == lib.header:  # every define: libts/param_ts.h holds VERSION_TS twice
            texts[path], count = re.subn(rf"^(#define VERSION_{lib.acronym} ){re.escape(lib.build)}", rf"\g<1>{new}", text, flags=re.M)
            if not count:
                raise VersioningError(f"{path.name}: no VERSION_{lib.acronym} {lib.build}")
            continue
        texts[path] = target.rewrite(text, lib.build, new)
    return texts


def problems(root: Path = ROOT) -> tuple[list[str], list[str]]:
    """(failures, information)."""
    bad, info, lagging = [], [], {}
    version = current(root)
    for target in SEMVER_COPIES:
        found = target.find(_read(root, target.path))
        if found != [version]:
            bad.append(f"{target.path}: {', '.join(found) or 'no version'} (pixi.toml says {version})")
    caw_make = _read(root, "src/Makefile")
    for lib in libraries(root):
        if lib.header:
            found = re.findall(rf"^#define VERSION_{lib.acronym} (\S+)", lib.header.read_text(encoding="utf-8", errors="replace"), re.M)
            if not found or set(found) != {lib.build}:
                bad.append(f"{lib.name}: Makefile V_{lib.acronym}={lib.build} but {lib.header.name} says {', '.join(found) or 'nothing'}")
        copy = re.findall(rf"^V_{lib.acronym}=(\S+)", caw_make, re.M)
        if copy and copy != [lib.build]:
            bad.append(f"src/Makefile: V_{lib.acronym}={copy[0]} but {lib.name} says {lib.build}")
        for other in libraries(root):
            if other.name != lib.name:
                theirs = re.findall(rf"^V_{lib.acronym}=(\S+)", other.makefile.read_text(encoding="utf-8", errors="replace"), re.M)
                if theirs and theirs != [lib.build]:
                    lagging[lib.name] = lagging.get(lib.name, 0) + 1
    if lagging:
        info.append("other libraries' copies behind their library (the build rewrites them): " + ", ".join(f"{k} x{v}" for k, v in lagging.items()))
    return bad, info


def _git(cwd: Path, *args: str) -> list[str] | None:
    done = subprocess.run(["git", "-C", str(cwd), *args], capture_output=True, text=True)
    return None if done.returncode else done.stdout.splitlines()


def range_problems(span: str, root: Path = ROOT) -> list[str]:
    """Commits of *span* that touch src/ without moving the version."""
    bad = []
    commits = _git(root, "rev-list", "--no-merges", span) or []
    for sha in commits:
        files = _git(root, "show", "--name-only", "--pretty=format:", sha) or []
        src = [f for f in files if f.startswith("src/") and not re.match(r"src/(lib[^/]+|scripts|c-rive)(/|$)", f)]
        if src and "pixi.toml" not in files:
            bad.append(f"cawaqs {sha[:8]}: touches {src[0]} without moving pixi.toml")
    for lib in libraries(root):
        for sha in _git(lib.dir, "rev-list", "--no-merges", span) or []:
            files = _git(lib.dir, "show", "--name-only", "--pretty=format:", sha) or []
            if any(f.startswith("src/") for f in files) and "src/Makefile" not in files:
                bad.append(f"{lib.name} {sha[:8]}: touches src/ without moving its build (src/Makefile)")
    return bad


def write(texts: dict[Path, str]) -> None:
    drafts = []
    for path, text in texts.items():
        draft = path.with_name(f".{path.name}.versioning")
        draft.write_text(text, encoding="utf-8")
        drafts.append((draft, path))
    for draft, path in drafts:
        os.replace(draft, path)


def _finish(texts: dict[Path, str], old: str, new: str, root: Path, dry: bool, subject: str | None) -> int:
    print(f"{old} -> {new}")
    for path in texts:
        print(f"  {path.relative_to(root) if path.is_relative_to(root) else path}")
    if dry:
        print("dry run: nothing written")
        return 0
    write(texts)
    print("written" + (f"; commit subject: {subject} …" if subject else ""))
    return 0


def main(argv: Sequence[str] | None = None, root: Path = ROOT) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = parser.add_subparsers(dest="command", required=True)
    bv = sub.add_parser("bump-version", help="the CaWaQS SemVer, in every copy")
    bv.add_argument("level", choices=("patch", "minor", "major"))
    bb = sub.add_parser("bump-build", help="a library's build, MAJOR.XX")
    bb.add_argument("lib")
    bb.add_argument("--major", action="store_true")
    for p in (bv, bb):
        p.add_argument("--dry-run", action="store_true")
    ck = sub.add_parser("check-version", help="every copy agrees")
    ck.add_argument("--range", dest="span", help="A..B: commits touching src/ must move the version")
    args = parser.parse_args(argv)
    if args.command == "check-version":
        bad, info = problems(root)
        if args.span:
            bad += range_problems(args.span, root)
        for line in info:
            print(f"info: {line}")
        if bad:
            print("check-version: FAILED")
            print("\n".join(f"  {b}" for b in bad))
            return 1
        print(f"{current(root)}: ok, {len(libraries(root))} libraries")
        return 0
    bad, _ = problems(root)
    if bad:
        raise VersioningError("fix the copies first (pixi run check-version):\n  " + "\n  ".join(bad))
    if args.command == "bump-version":
        old = current(root)
        new = next_version(old, args.level)
        return _finish(plan_version(old, new, root), old, new, root, args.dry_run, f"cawaqs-{new}")
    lib = library(args.lib, root)
    new = next_build(lib.build, args.major)
    return _finish(plan_build(lib, new, root), lib.build, new, root, args.dry_run, None)


if __name__ == "__main__":
    sys.exit(main())
