# atcgs-versioning — how atCGS numbers its releases

*Fills in: DevSpec/Versioning.md*

*Created: 2026-11-05*

1. **Scheme: SemVer** `MAJOR.MINOR.PATCH-alpha`, because atCGS is a tool other
   projects install as their gate (`.atcgs`) and must be able to trust. The
   `-alpha` stage stays until the owner moves it.

   **Public interface:**
   - the `pixi run cgs` command line: the selectors `OPX DEV USR PUB`, the verbs
     (`init request enrol admit revoke publish login`), the `login` operations
     per level, and the JSON keys they print;
   - the root `pixi.toml` task names (`cgs test lint contract-inspect
     identity-demo local-remote deploy-keys`);
   - the register's journal formats and the GLYPH layout (`spec/contracts.toml`);
   - the twin specs in `examples/*.cgs`.

   Not public: `@cgs/pixi.toml` (the development space), internal modules,
   tests, scripts' output text.

2. **No build counter.** The release version lives in `pixi.toml`
   `[workspace] version`.

3. **Release bump:** `pixi run bump-version major|minor|patch [--stage S] [--dry-run]`
   (`scripts/bump_version.py` in this mount). It writes `pixi.toml`,
   `@cgs/pixi.toml`, `atcgs/__init__.py`, `spec/contracts.toml` (header and
   `[contract] version`), the README title and ALPHA.md, all or none.

4. **Rebuilt after a bump:** nothing is generated; `pixi run test` checks every
   mirror (`tests/test_version.py`).

5. **Release register:** none beyond the commit subject `cgs-<version> …`; no tag.

6. **Exception** — owner, 2026-11-05: 1.9.0-alpha is MINOR although it removes
   `pixi run '@cgs'` and `examples/molonari.cgs`, because the `-alpha` command
   line was not yet declared public. From 1.9.0-alpha on, this file declares it.
