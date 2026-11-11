Owner, 2026-11-11: *"write a shortTicket to reformat the examples so that they meet the new atCGS standards on CGS-ALPHA where opx, dev, usr pub .cgs were removed. I think there is only a complexgitsync-alpha.cgs to consider."*

## The standard, as atCGS states it

atCGS's `examples/` on `CGS-ALPHA` (read with `gh`, 2026-11-11) holds `cgs-alpha.cgs`, `ComplexGraphSync.cgs`, the four `molo_*.cgs` and `registration.toml`. `cgs-dev.cgs`, `cgs-opx.cgs` and `cgs-usr.cgs` are gone. `cgs-alpha.cgs` says the rule in its header: *one branch for the whole alpha series, no level branch (opx, dev, usr)*, and its name is not a level file, because `alpha` has five characters, not three.

Its shape: `environment_root` and `environment` first, `project = { name, default_branch = "CGS-ALPHA" }` with no `fallback_branch`, inline `repos = [ ... ]`, project repositories with `fallback_branch = "CGS-ALPHA"` and `nested_config = "disabled"`, private writable mounts falling back to `main` with no branch typed, and the `.distant` and `.local` groups under their own comments.

## What is already done

`examples/cgitsync-alpha.cgs` (commit b9629a3, the owner) is ComplexGitSync's file in that standard. Note the name: `cgitsync-alpha.cgs`, not `complexgitsync-alpha.cgs`. Nothing else in `examples/` follows it yet.

## Why it is more than one file

Four level files are still here and on `origin/CGS-ALPHA`: `complexgitsync-opx.cgs`, `complexgitsync-dev.cgs`, `complexgitsync-usr.cgs`, `complexgitsync-pub.cgs`. Three are only examples. `complexgitsync-dev.cgs` is load-bearing:

| Reads it | Where |
|---|---|
| CI's tree reconstitution | `.github/workflows/ci.yml:30` |
| `check-spectree` (the manifest check) | `scripts/spec_tree.py:92` (`DEV_CGS_PATH`) |
| Tests | `test_repo_scope.py`, `test_git_branch.py`, `test_documents.py`, `test_user_dev_profile.py`, `test_pull_outside_root.py`, `test_named_cgs.py`, `test_bump_version.py` |
| A docstring | `src/ComplexGitSync/tree/memory/repository.py:306` |
| Tutorials | `tutorials/05_private_repos.md:142`, `tutorials/06_memory.md:103` |
| `nested_config` of gx4g's level files | `examples/gx4g-opx.cgs`, `examples/gx4g-dev.cgs` |
| Specs | `AgenticManifest.md`, `digest.md` line on the manifest, `install.cgs`'s header comment |

**A dead path, already today.** `bump_version.py` (`BOOTSTRAP_CGS_PATH`), `Versioning.md` (`.dev`), `cgitsync-dev.md` and `CLAUDE.md` name `examples/complexgitsync4dev.cgs`, which does not exist. `bump-version` reconstitutes `docs/` from it when `docs/` is missing, so that fallback fails now.

## What to do

1. Remove `complexgitsync-{opx,dev,usr,pub}.cgs`. Point every reader above at `examples/cgitsync-alpha.cgs`, including the `4dev` dead paths. A change to `src/` (the docstring) and `scripts/` makes it an `implement`, released at `patch` at least.
2. Check the other examples against the standard (`doccomplexgitsync.cgs`, `gx4g-*.cgs`, `template.cgs`, `normalized_template.cgs`, and the project trees `cawaqs*`, `htas`, `molonari*`) and convert only those the owner names.
3. Gates: lint, test, `check-spectree`, `status` with `errors=0`.

## Not decided

- **D1 — `gx4g-opx.cgs`, `gx4g-dev.cgs`.** They are level files too. Remove them, convert them to one `gx4g-alpha.cgs`, or keep them because gx4g is not on the alpha standard yet. `tests/integration/test_op_boundary.py` and `test_named_cgs.py` read their names.
- **D2 — the name of the developer install.** `DevSpecs.md` §Two installs (shared, read-only) calls it `<project-name>4dev.cgs`. `cgitsync-alpha.cgs` does not follow that. Either this project writes an exception, with the owner's name and date, in its fill-in, or the rule in `DevSpec` changes, which concerns every conforming project.
- **D3 — the other examples.** Which of the files in step 2 are to be converted, and which stay as they are because they describe other projects.
