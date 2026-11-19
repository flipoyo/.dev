"""Bump HydrologicalTwinAlphaSeries's SemVer and write it to every copy.

Ported from ComplexGitSync's ``bump_version.py`` (SemVerPixi). It lives in the
private ``.dev`` mount, so a public-only checkout cannot cut a release.

The version is real SemVer, read from ``pixi.toml`` (what ``cgitsync`` reads)
and written to every target, all or none:

- ``pixi.toml``: ``[workspace].version``;
- ``pyproject.toml``: ``[project].version``, the build's copy;
- ``docs/hydrological_twin/HTAS_user_guide.tex``: ``\\def\\version{...}``.

MAJOR, MINOR or PATCH is a judgement about the public interface
(``AdditionalSpecs.md`` §4), so the caller says which. ``--set`` exists for
one migration only: it is accepted when the current version is not SemVer
(the old ``III.alpha.NN``), and refused otherwise, so it can never skip a level.

It ends on ``old -> new``, which ``cgitsync version bump`` reads. Exactly one
of a level, ``--pre``, ``--release`` or ``--set`` is required; ``--dry-run``
writes nothing. ``__build__`` is not a target: ``bump_build.py`` owns it.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
import tomllib
from dataclasses import dataclass, replace
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
PIXI_TOML_PATH = REPO_ROOT / "pixi.toml"
PYPROJECT_PATH = REPO_ROOT / "pyproject.toml"
GUIDE_PATH = REPO_ROOT / "docs" / "hydrological_twin" / "HTAS_user_guide.tex"
BOOTSTRAP_CGS = ".config/htas-dev-beta.cgs"

PRE_RELEASE_STAGES = ("alpha", "beta", "rc")

_SEMVER_CORE = r"(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
_SEMVER_PRERELEASE = r"(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?"
_SEMVER_BUILD = r"(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?"
VERSION_RE = re.compile(f"^{_SEMVER_CORE}{_SEMVER_PRERELEASE}{_SEMVER_BUILD}$")
_PRERELEASE_STAGE_RE = re.compile(r"^([a-zA-Z-]+)\.(\d+)$")

_TOML_VERSION_FIELD_RE = re.compile(r'(^version = ")([^"]+)(")', re.MULTILINE)
_GUIDE_VERSION_RE = re.compile(r"(^\\def\\version\{)([^}]+)(\})", re.MULTILINE)


class VersionSyncError(RuntimeError):
    """Raised when a version field can't be read or updated."""


@dataclass(frozen=True, slots=True)
class SemVer:
    """A parsed SemVer version: the parts a bump decision needs."""

    major: int
    minor: int
    patch: int
    prerelease: str | None = None

    def __str__(self) -> str:
        core = f"{self.major}.{self.minor}.{self.patch}"
        return f"{core}-{self.prerelease}" if self.prerelease else core


def is_semver(version: str) -> bool:
    """Whether *version* is SemVer."""
    return VERSION_RE.match(version) is not None


def parse_version(version: str) -> SemVer:
    """Parse *version* as SemVer, rejecting anything else."""
    match = VERSION_RE.match(version)
    if not match:
        raise VersionSyncError(f"{version!r} is not a valid SemVer version.")
    return SemVer(int(match.group(1)), int(match.group(2)), int(match.group(3)), match.group(4))


def read_current_version(pixi_toml_path: Path = PIXI_TOML_PATH) -> str:
    """Return the version recorded in *pixi_toml_path*, as written (not judged)."""
    data = tomllib.loads(pixi_toml_path.read_text(encoding="utf-8"))
    try:
        return str(data["workspace"]["version"])
    except KeyError as exc:
        raise VersionSyncError(f"{pixi_toml_path}: no [workspace].version field found.") from exc


def next_version(
    current: str,
    *,
    level: str | None = None,
    pre: str | None = None,
    release: bool = False,
    set_to: str | None = None,
) -> str:
    """Return the next version after *current*.

    Exactly one of *level* (with an optional *pre* to start a pre-release
    cycle), *pre* alone (advance a pre-release), *release* (finalise one) or
    *set_to* (migration only: *current* must not be SemVer) is required.
    """
    if set_to is not None:
        parse_version(set_to)
        if is_semver(current):
            raise VersionSyncError(f"--set is for leaving a non-SemVer version; {current!r} is SemVer, so name a level.")
        return set_to
    parsed = parse_version(current)
    if level is not None:
        if level == "major":
            parsed = SemVer(parsed.major + 1, 0, 0)
        elif level == "minor":
            parsed = SemVer(parsed.major, parsed.minor + 1, 0)
        elif level == "patch":
            parsed = SemVer(parsed.major, parsed.minor, parsed.patch + 1)
        else:
            raise VersionSyncError(f"Unknown bump level {level!r}.")
        return str(replace(parsed, prerelease=f"{pre}.1") if pre else parsed)
    if pre is not None:
        if parsed.prerelease is None:
            raise VersionSyncError(f"{current!r} is not a pre-release; pass a level with --pre to start one.")
        stage = _PRERELEASE_STAGE_RE.match(parsed.prerelease)
        count = int(stage.group(2)) + 1 if stage and stage.group(1) == pre else 1
        return str(replace(parsed, prerelease=f"{pre}.{count}"))
    if release:
        if parsed.prerelease is None:
            raise VersionSyncError(f"{current!r} is not a pre-release; nothing to finalise.")
        return str(replace(parsed, prerelease=None))
    raise VersionSyncError("Specify a level (major/minor/patch), --pre, --release or --set.")


def _rendered(path: Path, pattern: re.Pattern[str], new_version: str) -> str:
    """Return *path*'s text with its version set; reads and checks only."""
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise VersionSyncError(f"{path}: missing; cannot update its version field.") from exc
    if not os.access(path, os.W_OK):
        raise VersionSyncError(f"{path}: not writable; cannot update its version field.")
    new_text, count = pattern.subn(rf"\g<1>{new_version}\g<3>", text, count=1)
    if count != 1:
        raise VersionSyncError(f"{path}: could not find a version field to update.")
    return new_text


def apply_version(
    new_version: str,
    *,
    pixi_toml_path: Path = PIXI_TOML_PATH,
    pyproject_path: Path = PYPROJECT_PATH,
    guide_path: Path = GUIDE_PATH,
    dry_run: bool = False,
) -> None:
    """Write *new_version* to every target: all of them or none.

    With *dry_run*, every target is still read and checked, so a dry run fails
    exactly where the real run would, and nothing is written.
    """
    if not guide_path.parent.is_dir():
        raise VersionSyncError(
            f"{guide_path.parent} is missing: bootstrap {BOOTSTRAP_CGS} to mount docs/hydrological_twin. Nothing was changed."
        )
    targets = [
        (pixi_toml_path, _TOML_VERSION_FIELD_RE),
        (pyproject_path, _TOML_VERSION_FIELD_RE),
        (guide_path, _GUIDE_VERSION_RE),
    ]
    rewritten = [(path, _rendered(path, pattern, new_version)) for path, pattern in targets]
    if dry_run:
        return
    for path, text in rewritten:
        path.write_text(text, encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("level", nargs="?", choices=("major", "minor", "patch"), default=None, help="which SemVer position to bump")
    parser.add_argument("--release", action="store_true", help="finalise the current pre-release into its base version")
    parser.add_argument("--pre", choices=PRE_RELEASE_STAGES, default=None, help="pre-release stage; with a level starts a cycle at .1, alone advances it")
    parser.add_argument("--set", dest="set_to", metavar="VERSION", default=None, help="migration only: set a SemVer version when the current one is not SemVer")
    parser.add_argument("--dry-run", action="store_true", help="print the version change without writing any file")
    args = parser.parse_args(argv)

    if args.release and (args.pre or args.level or args.set_to):
        parser.error("--release takes no level, --pre or --set.")
    if args.set_to and (args.pre or args.level):
        parser.error("--set takes no level or --pre.")
    if not (args.level or args.pre or args.release or args.set_to):
        parser.error("Specify a level (major/minor/patch), --pre, --release or --set.")

    try:
        current = read_current_version()
        new = next_version(current, level=args.level, pre=args.pre, release=args.release, set_to=args.set_to)
        apply_version(new, dry_run=args.dry_run)
    except VersionSyncError as exc:
        print(f"bump-version: {exc}", file=sys.stderr)
        return 1
    print(f"{current} -> {new}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
