Owner, 2026-11-03: *"write a short ticket in ComplexGitSync … I'll execute the fix from a proper env"*

Context: `cgitsync memory setup` cannot declare the memory of any project that is not on `main`. Seen in atCGS, bootstrapping `examples/cgs-opx.cgs` from `~/Programmes/ComplexGitSync` (CGS-ALPHA, `dd3472b`): the repository `flipoyo/.memory` is created, then the `declare` step refuses its own entry, and the memory stays local only.

    repos[8].default_branch = 'cgs' disagrees with the branch a private, writable
    repository takes from this project: 'cgs_opx'.

The same happens with project `ComplexGraphSync` on `CGS-ALPHA` (`'ComplexGraphSync'` against `'ComplexGraphSync_CGS-ALPHA'`).

## Cause

Two pieces of code disagree:

- `src/ComplexGitSync/tree/memory/repository.py:139`, `MemoryRepository.mount_entry`, writes `"default_branch": project_name`.
- `src/ComplexGitSync/git_repo/git_branch.py:255-256`, `declared_private_local_mismatch`, accepts only no `default_branch`, `private_local_branch(project, project_default)`, or `project.default_branch`.

`project_name` equals the derived branch only when the project is on `main`, so every other project fails. The `mount_entry` docstring already says the branch "is left to the ordinary derivation", which the code doesn't do.

## Fix

1. Drop the `"default_branch": project_name,` line from `mount_entry`. The derivation then gives `<project>_<branch>`, or `<project>` on `main`, the same as `MemoryRepository.branch`.
2. Grep `tests/` for anything that expects `default_branch` in the proposed entry, or in `memory init` / `memory setup` output, and update it.
3. Add a test: `memory setup` on a project whose `default_branch` is not `main` declares without error, and the written `.cgs` still validates.
4. `pixi run lint`, `pixi run test`.

Not checked: whether the twin branch naming (`memory_defaulted` logged `ComplexGitSync_cgs` / `ComplexGitSync_ComplexGraphSync_CGS-ALPHA`) and the non-twin rule the validator uses also disagree for a twin tree. Look at it while you are in there.

## Workaround until it lands

Declare the memory by hand without `default_branch`, as atCGS `examples/ComplexGraphSync.cgs` does, then rerun `cgitsync memory setup` so it adopts the local memory.
