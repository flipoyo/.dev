# cgitsync-dev — building, testing and linting ComplexGitSync itself

*Created: 2026-09-21*

This project's own fill-ins for the checklist shape `dev-sync` (the
shared skill) states in general. Read `dev-sync` first if you have not —
this file says only what is specific to ComplexGitSync: which commands,
which repository, which paths. It restates none of `dev-sync`'s own
rules.

## Commands

This project uses Pixi, not bare `pip`/`venv`.

```bash
pixi install         # create/update the environment (run after touching pixi.toml or dependencies)
pixi run test        # pytest, tests/unit + tests/integration
pixi run lint        # ruff check .
pixi run bump-version  # orchestrator: bump SemVer and sync every manifest and doc (see below)
pixi run bump-build    # worker: bump the __build__ counter alone (see below)
```

CI (`.github/workflows/ci.yml`) runs both `lint` and `test` on push/PR to
`main`/`lechat`. Run both locally before pushing.

### Bootstrapping a working checkout

ComplexGitSync manages itself as a multi-repo tree: a fresh `git clone`
alone gets you the code but not `docs/`, or the mounts under `.agent/`.
Use `bootstrap` pointed at **`examples/complexgitsync4dev.cgs`** — the
developer spec — to get a fully populated, independently live-editable
checkout. (The root `install.cgs` is the *user* install: the tool and
its documentation only. Bootstrapping that one leaves you without the
specs you are reading.)

```bash
git clone https://github.com/flipoyo/ComplexGitSync.git
cd ComplexGitSync
pixi install

pixi run cgitsync bootstrap examples/complexgitsync4dev.cgs ComplexGitSync
# Copy the export command from bootstrap's own output, or use:
export CGSHOME=/home/user/.cgs/CGS20260831131233/ComplexGitSync

cd "$CGSHOME"       # this *is* the freshly cloned ComplexGitSync checkout —
pixi install        # bootstrap clones a plain checkout, so it needs its own
                     # pixi environment before you can run cgitsync from here
```

`pixi.toml`'s `complexgitsync = { path = ".", editable = true }` makes
this checkout self-editable the moment that second `pixi install`
finishes: edit any file under `src/ComplexGitSync/`, then
`pixi run cgitsync ...` from inside `$CGSHOME` picks up the change
immediately — no reinstall step, no separate `pip install -e .`.

## Before committing — this project's own fill-ins

`dev-sync`'s checklist shape, filled in:

1. **`pixi run lint` and `pixi run test`**, both.
2. **`pixi run bump-build`** for any change under `src/` — see
   `AdditionalSpecs.md`, *Versioning*, *Who bumps what*.
3. **`cgitsync status`, run from this tree's own root, must show
   `errors=0`.**
4. **`pixi run bump-version {major,minor,patch}`** when wrapping up a
   feature branch — see `AdditionalSpecs.md`, *Versioning*. Syncs
   `pyproject.toml` (authoritative), `pixi.toml`,
   `src/ComplexGitSync/__init__.py`'s `__version__`, the README title,
   and the `\cgsversion` macro in `docs/Setup/Shortcuts.tex` and
   `docs/preamble.tex`.
5. **Rebuild the docs if you changed them**: `cd docs && latexmk -pdf
   MASTER.tex` (plus each `c_*.tex` you touched) — `bump-version`
   rewrites `.tex` sources but does not regenerate the tracked PDFs.
6. **Update `AdditionalSpecs.md`'s architecture section** if module
   responsibility moved.
7. **Document any new CLI command** in the README command table and
   `docs/Text/user_guide.tex`, and its client method in
   `docs/Text/api_python.tex`. The README half is enforced by
   `tests/unit/test_cli_smoke.py::test_readme_documents_every_cli_command`.
8. **This project's name is `cgitsync`**, so a commit message reads
   `cgitsync3.1.0` (run `bump-version` first, so the version it reads is
   current) — `dev-sync`'s own commit-message rule, filled in.

## Testing — this project's own layout

- Unit tests: `tests/unit/`
- Integration tests: `tests/integration/`
- Integration suite includes: CGSi topology expansion checks, local
  file-remote `clone_cgs` / `launch_release` lifecycle restoration, and a
  CLI-first READY `.gts` git command cycle
  (`add → commit → push → tag → freeze`) mirrored in the Python API.
- Run: `pixi run test` from the repository root.
- Tests must not depend on network access or live git remotes.
- **A test that asserts on a date injects the date.** Every dated fact a
  command writes goes through `ClockProtocol` (`memory/ledger_entry.py`)
  — real by default (`orchestre.SystemClock`), fake by injection — so a
  test asserting on one supplies a fixed clock rather than reaching for
  `monkeypatch` on the real one. See `AdditionalSpecs.md`'s own citation
  of the ticket that established this (`ClockSeam`).
