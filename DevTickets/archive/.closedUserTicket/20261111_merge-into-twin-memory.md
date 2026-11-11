Owner, 2026-11-11, after `cgitsync merge CGS-ALPHA --into main --all` then `cgitsync push --all`: *"why is everything not synced ?"*, then *"write the shortticket on the CGS-ALPHA branch"*.

## What happened

The tree is a bootstrap twin: its memory is filed under `ComplexGitSync_<project>`, so `.memory` and `.self-history` sit on `ComplexGitSync_ComplexGitSync_CGS-ALPHA` on `CGS-ALPHA`, and on `ComplexGitSync_ComplexGitSync` on `main`.

1. `merge CGS-ALPHA --into main --all` (the dry run, and the merge) planned both twin repositories as `ComplexGitSync <- ComplexGitSync_CGS-ALPHA (no such branch here — skipped)`. Those are the names of a non-twin private repository. They exist nowhere, so the memory was skipped and stayed on its CGS-ALPHA branch while every other repository moved to `main`. The merge ended `status: ok`.
2. `push --all` was then refused: `.memory` and `.self-history` were on the wrong branch for `main` (*branch misalignment: expected 'ComplexGitSync_ComplexGitSync', found 'ComplexGitSync_ComplexGitSync_CGS-ALPHA'*). `status` warned that the tree was split.
3. The owner fixed it by hand, in each of the two repositories: `git checkout -b ComplexGitSync_ComplexGitSync origin/ComplexGitSync_ComplexGitSync`, then `git merge --ff-only ComplexGitSync_ComplexGitSync_CGS-ALPHA`. That was a pure fast-forward: `main`'s memory had 0 commits of its own, CGS-ALPHA's 16 (`.self-history` 7). The push then went through.

## Cause

`MergeOperation.merge_source_ref` (`tree/operations/merge.py`) calls `git_branch.resolve_propagated_ref(repo, branch, project_name=...)` without `twin=`, so a twin memory's branches are derived as `<project>[_<branch>]` instead of `ComplexGitSync_<project>[_<branch>]`. `checkout` and `memory branch` already know a twin (`git_branch.is_twin_branch`, and the State's recorded target on the fallback base, MemoryMount); `merge`, `merge --into`, `merge --resolve` and `pull --private` do not. `merge_into_plan` (`orchestre/tree_commands.py`) also passes the bare project name where `merge_into_tree` passes `MountGuard.base(...)`, so the dry run and the merge can derive different names for a nested Parent's repository.

**A second defect, in the reporting.** A memory whose derived source is missing is reported "skipped", and the merge ends `ok`, although the tree is left split. The memory is the one repository a merge must never leave behind, since the next `push` refuses because of it.

## What to do

1. Derive both branch names of a twin memory, and of its `.self-history`, with the twin rule, in every caller of `merge_source_ref`. Use the one place that already decides twin status, never a second copy of the rule.
2. Make the dry run and the merge derive names the same way (`MountGuard.base` in both).
3. When a merge moves the project and its memory cannot follow, refuse before anything moves, naming the memory and the branch it lacks, rather than "skipped" with `ok`.
4. Tests: a bootstrap twin tree on `CGS-ALPHA`, with `main` behind it in the project and in the memory. `merge CGS-ALPHA --into main --all` moves the memory to `ComplexGitSync_ComplexGitSync` (kept whole, CGS-ALPHA's recorded as history, or a fast-forward when `main`'s is an ancestor), `status` shows no split, and `push --all` passes its preflight.

This changes `src/`, so it is an `implement`.

## Not decided

- **D1 — the memory's side.** When CGS-ALPHA's memory is ahead and `main`'s is an ancestor, a fast-forward loses nothing. When both have their own commits, the rule keeps the target's memory whole (`main`'s), with CGS-ALPHA's as history. Is that the right side for a merge into `main`, or should `merge --into` keep the source's memory (`memory merge --theirs`)?
- **D2 — a target memory branch only the remote holds** (`origin/ComplexGitSync_ComplexGitSync`, as here). Is it refused with the `git branch` command, as MergeIntoLocalTarget does for every other repository, or is the memory the exception, created from the remote because it must follow?
