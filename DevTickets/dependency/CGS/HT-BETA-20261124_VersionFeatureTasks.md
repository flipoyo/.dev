Three generic feature proposals for ComplexGitSync HT-BETA, seen with cgitsync 8.11.1 (HT-BETA 838ee24). Each stands on ComplexGitSync's own model. The workspace where the need was observed is cited only as an example: it uses ComplexGitSync as a development tool and waits for none of these. Revised 2026-11-25.

| # | Proposal | Kind |
|---|---|---|
| R1 | `version diagnose` / `bump` find a version task declared in a pixi feature | a gap in an existing command |
| R2 | The branch-naming rule, written as a stable, documented contract | documentation |
| R3 | A version kept outside `pixi.toml` | a new capability, for consideration |

## R1. Version tasks declared in a pixi feature

`cgitsync version diagnose` and `version bump` look for a repository's `bump-version` (and `bump-build`) task only in the top-level `[tasks]` of its `pixi.toml` (`VersionOperation._tasks`, `tree/operations/version.py`, about line 95). A project that keeps bumping as a developer-only act declares the task in a feature, for example `[feature.<dev>.tasks]` with an environment `<dev> = [...]`, so that a user environment has no bump task. ComplexGitSync then reports it as `task needed` and `version bump` refuses it, although `pixi run bump-version` finds the task by itself.

Observed: `bump-version` in `[feature.dev.tasks]` gives `<project> . pixi.toml 4.1.3 semver none … task needed`, and "1 other file(s) hold 4.1.3: declare a bump-version task".

- Read the tasks from `[tasks]` and from every `[feature.<name>.tasks]`.
  - When a task is defined in exactly one environment, run it as `pixi run --manifest-path <m> -e <env> bump-version <level>`, or rely on pixi's own lookup.
  - When it is defined in several, prefer the default environment, then say which one ran.
- Keep `_missing_script`. In a DEV tree whose private mount is missing, say "developer task, its script is not mounted" rather than "task needed". `version` already refuses non-DEV trees.
- Apply the same to the `BUILD` column (`bump-build`).

## R2. The branch-naming rule as a documented contract

Since RootBareBranch (8.11.1), a tree's branches follow a rule:
- the root repository is on the bare branch `<b>`;
- every other repository that is not private is on `<project>_<b>`;
- a repository whose `<project>_<b>` does not exist falls back to its `fallback_branch`, and the fallback is logged.

The rule is visible outside ComplexGitSync: anyone can clone a tree by hand, or with their own scripts, and land on the same branches with git alone. That only holds if the rule is written down.

- State the rule in the user documentation:
  - where `<project>` is read from (the `.cgs` file's project, or `[workspace] name`);
  - the separator `_`;
  - the fallback.
- Say how private repositories and the memory repository are named (e.g. `ComplexGitSync_<project>_<b>`), so that a hand-made clone knows which names to leave alone.
- Treat a change to the rule as a breaking change, announced in the release notes.

## R3. A version kept outside `pixi.toml` — for consideration

`VersionScheme` reads only `pixi.toml`. A nested repository with no manifest is reported as `not versioned`, even when it carries a version of its own. A common C case is a build number `MAJOR.XX` kept in a `Makefile` variable and repeated in a header `#define`. Repositories shared between several projects often cannot take a `pixi.toml`.

A possible shape, in `VersionScheme`'s own terms (`read`, `next`, `moved_by`):
- a `build` scheme: `MAJOR.XX`, with `next` giving `+0.01`, or `(MAJOR+1).00` for a major bump;
- where the fields sit is declared per repository, in the `.cgs` spec or in the root's manifest, never in the shared repository. ComplexGitSync reads them and checks that they agree;
- `version diagnose` shows such a repository with its scheme, instead of `not versioned`;
- `version bump` either writes the fields itself, or runs the root's task with the repository's path. That is a design choice for ComplexGitSync.

Until such a feature exists, a workspace keeps this in its own private script, so nothing waits on it.
