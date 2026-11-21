# AnonymousProject — a project can mount the shared repositories without writing its name into them

*Created: 2026-11-21*

*Branch: data-encrypt*

> **From the owner's short ticket** [anonymous-project](../archive/.closedUserTicket/20261121_anonymous-project.md)
> (2026-11-21). Filed on `data-encrypt` at the owner's request: it serves the
> same purpose as EncryptedRepos, a private project that reveals nothing
> through the repositories it shares. Ranked 2-14 at filing; the owner
> re-ranks at the next review.

## Abstract — read this first

**The one-line version.** A new `.cgs` option, `anonymous`, makes cgitsync
file a project under an **alias** in every repository it shares with other
projects. The alias is either the first 6 hex digits of `sha256(name)`
(`"hash"`), or `anonymous-<i>` (`"sequence"`), with `-<i>` added on a
collision. The real name stays in the project's own `.cgs`.

**What this document is.** The design of the option, where the name leaks
today (§1), the steps (§3), and the decisions left to the owner (§5).

**Why it exists.** `private_local_branch` (`git_repo/git_branch.py`) names
every private/local branch after the project: `<project>` on `main`,
`<project>_<branch>` otherwise, and `ComplexGitSync_<project>_<branch>` for a
twin's memory. Those repositories (`.dev`, `.localSpec`, `.claude`,
`.memory`, `omniscience`) are shared by all the owner's projects. A project
whose very name is private (here a personal-wealth project) shows that name
to anyone who can list the branches of the shared repositories.

**Who it is for.** The worker and orchestrator who implement it, and the owner
who answers §5.

**What you need to do with it.** Answer §5, then do §3 step 1, the audit,
before any code.

```mermaid
graph LR
    N["project name<br/>(only in its own .cgs)"] -->|"anonymous = hash"| H["293f93<br/>or 293f93-1, -2 ..."]
    N -->|"anonymous = sequence"| S["anonymous-1<br/>anonymous-2 ..."]
    H --> B["every shared repo:<br/>branches, records, states"]
    S --> B

    classDef here fill:#1565C0,color:#fff,stroke:#111,stroke-width:2px;
    class B here;
```

---

## 1. Where the project's name reaches a shared repository today

| Channel | Where it is written | Example for project `P` on branch `x` |
|---|---|---|
| private/local branch names | `private_local_branch` (`git_repo/git_branch.py`, "the one place the naming rule lives") | `.dev`, `.localSpec`, `.claude`, `omniscience`: `P_x` |
| memory branch | `MemoryRepository.branch` (`tree/memory/repository.py`), via the same function | `.memory`: `P_x`, twin `ComplexGitSync_P_x` |
| self-history branch | `self-history adopt`, on the memory's branch | `.self-history`: same as memory |
| omniscience records | `omniscience_record.py`, field `project` (lines 81, 114, 174) | the record header carries `project = "P"` |
| memory content | the `.gts` States and the ledger committed into `.memory` | the project name, and every repository URL of the tree |
| commit messages and tags | commit messages written by cgitsync into private repos; tags `cgitsync tag` creates | to be measured by the audit (§3 step 1) |

The first three rows are the owner's request. The last three are the same
leak through content rather than names, and are why step 1 is an audit.

## 2. The option

```toml
project = { name = "PATRIMOINE", default_branch = "security-space", anonymous = "hash" }   # or "sequence"
```

- **An option of the project field, never a name (owner).** The user declares
  the real name, then `anonymous`. The alias is computed and is what every
  shared register receives: branches, omniscience records, memory. It is
  never typed. A `project.name` that has the shape of an alias
  (`anonymous-<i>`, or 6 hex digits with an optional `-<i>`) is refused by
  `validate`, so nobody can sit on another project's alias by hand.
- **Off by default.** Without `anonymous`, nothing changes, byte for byte.
- **The alias is computed by a pure Ring 0 function**, next to
  `private_local_branch`, and replaces `project_name` wherever a shared
  repository is named or written. The suffix rule is unchanged: `<alias>` on
  `main`, `<alias>_<branch>` otherwise, and the twin keeps its
  `ComplexGitSync_` owner.
- **`"hash"` mode.** The candidates are `t`, then `t-1`, `t-2`, …, where
  `t = sha256(name.encode()).hexdigest()[:6]`. For `PATRIMOINE`, `t` is
  `293f93`.
- **`"sequence"` mode.** The candidates are `anonymous-1`, `anonymous-2`, …
- **Choosing a candidate (shared by both modes).** A candidate is *ours* when
  the shared repository's branch exists and carries the project's **claim**.
  It is *free* when no such branch exists. It is *taken* when the branch
  exists with another project's claim. The first candidate that is ours or
  free wins, so the choice is deterministic on every machine, with no local
  state.
- **The claim.** A one-line file, `.cgitsync-alias`, at the root of the alias
  branch, holding `sha256(name)` in full. It reveals no more than the alias
  already does in `"hash"` mode. It reveals more than nothing in `"sequence"`
  mode, hence §5 Q2.
- **Where the alias is resolved.** It is resolved once per tree, at
  `bootstrap`, `initialise` and `branch create`, then recorded in the tree's
  State. Every later command reads it from there and never searches again.
- **Coherence check.** The same alias must be used in every shared repository
  of the tree. If one repository's claim disagrees with the others, that is a
  refusal, not a new suffix.
- **Validation.** `validate` refuses an `anonymous` value other than `"hash"`
  or `"sequence"`. `named_cgs.py` is unaffected: the level-file rule reads
  the file name against `project.name`, which keeps the real name.

## 3. Steps

1. **Audit, before any code. Written: §6, for the owner to validate.** List every place a project name or a
   repository URL is written into a repository other than the project's own:
   the rows of §1, commit message templates, tags, the ledger, `.gts`
   headers, omniscience. Write the list into this ticket, row by row, each
   marked *alias* (replaced), *omit* (dropped under `anonymous`) or *keep*
   (with a reason). The owner validates the list.
2. **Ring 0.** `ProjectAlias` (its own file, `__all__`) has two methods:
   `candidates(name, mode)`, a generator, and `claim(name)`. It comes with
   unit tests: the `PATRIMOINE` → `293f93` vector, `-1` after a taken
   candidate, and the `sequence` order.
3. **Resolution.** A `GitRunner` probe reads a remote branch's
   `.cgitsync-alias` (`git ls-remote` + `git show`). Resolution runs in
   `bootstrap`, `initialise` and `branch create`, and the State records the
   alias.
4. **Naming.** `private_local_branch` and `MemoryRepository.branch` take the
   alias when the tree is anonymous. One call site decides, so no module
   composes the strings itself, as the docstring already requires.
5. **Content.** Apply the audit's *alias* and *omit* rows. In omniscience,
   `project` becomes the alias.
6. **Migration of an existing tree.** `cgitsync anonymise --dry-run` lists the
   branches `P_*` of the shared repositories and the alias branches that
   would replace them. Without `--dry-run`, it creates the alias branches at
   the same commits and pushes them. It deletes the `P_*` branches only with
   `--delete-old`, after a confirmation that names each one. History keeps
   the old name in commits already written: the command says so and does not
   rewrite history.
7. **Docs.** Add a paragraph to tutorial 05 (*private repos*), a section to
   the user guide, and a CHANGELOG entry.

## 4. Acceptance

- Unit tests: alias vectors, collision suffix, mode validation, and
  `private_local_branch` with and without an alias.
- `tests/integration/test_anonymous_project.py`, on local bare remotes:
  - two projects whose `"hash"` aliases collide (forced by monkeypatching the
    truncation) get `t` and `t-1`, on every machine, in either order;
  - a second bootstrap of the same project finds its own alias;
  - no shared repository's branch list, State, record or commit message
    contains the real name (a grep over every clone of the test tree);
  - a project without `anonymous` is byte for byte unchanged.
- `pixi run lint` and `pixi run test` are green, and module ceilings hold.
- Owner run: the PATRIMOINE tree (`compta/.config/compta-dev.cgs`:
  `name = "PATRIMOINE"`, `anonymous = "sequence"`) resolves to `anonymous-1`.
  No `PATRIMOINE` appears in the branches, records or States of `.dev`,
  `.localSpec`, `.claude`, `.memory` or `omniscience`.

## 4.1 The risk that holds until this lands

cgitsync 8.9.4 accepts `anonymous` in the project table **without a word and
ignores it** (probed 2026-11-21 with `validate`). A `.cgs` written for this
ticket, bootstrapped by a cgitsync that predates it, therefore writes the real
name into every shared register. That is the exact leak the option exists to
prevent.

Two consequences:

- `compta/.config/compta-dev.cgs` carries a *do not bootstrap* warning until
  this ticket lands.
- This ticket adds a guard for the versions that follow: a `.cgs` that
  declares `anonymous` is refused by any cgitsync that cannot honour it. The
  mechanism is §5 Q5.

## 5. Decisions for the owner

- **Q1: default mode.** Recommended: `"sequence"`.
  - `"hash"` is deterministic, but it can be **tested against a guess**:
    anyone who suspects the name `PATRIMOINE` can compute `293f93` and confirm
    it.
  - `"sequence"` reveals nothing about the name.
  - Alternative: a salted hash, with the salt in the owner's Bitwarden
    vault. That is stronger but needs the salt on every machine.
- **Q2: the claim in `"sequence"` mode.** With `sequence`, should the claim
  be `sha256(name)` (recommended: it is needed to tell our branch from
  another project's) or an HMAC with a salt?
- **Q3: content leaks.** Should repository URLs inside States written to
  `.memory` be aliased too, or is the project allowed to show its repository
  names while hiding its own name? This depends on the audit of step 1.
- **Q4: migration.** Is the `--delete-old` step of `anonymise` wanted, or are
  the old branches deleted by hand?
- **Q5: refusing an option the tool does not know.** How should an older
  cgitsync refuse a `.cgs` that declares `anonymous`?
  - (a) `validate` and `bootstrap` refuse **any** unknown key in the project
    table from now on. This is strict, and may break `.cgs` files that carry
    keys of their own.
  - (b) A minimum version in `environment.tools`
    (`cgitsync = "<version that ships this>"`), checked before cloning.
  - Recommended: (b) for this project, plus (a) for the `project` table
    only, after an audit of the checked-in `.cgs` files.

## 6. Audit, 2026-11-21 (step 1)

Method: a tree of project `ZQXSECRET` was bootstrapped on local bare remotes
with a private `.localSpec` and a `.memory`; the private branches were made,
then `commit --private`, `push --private`, `memory push` and `tag --private`
ran. Every shared repository (branches, remote branches, tags, commit
messages, every blob of every commit) was searched for the name. The
omniscience record and the `.gts` writers were read in the code, since no
omniscience repository was mounted. A name that only appears because the
real project's **root repository** is called after it is the user's own
choice of repository name, and is noted under Q3.

| # | Channel | Found | Decision |
|---|---|---|---|
| A1 | private/local branch (`.localSpec`, `.dev`, `.claude`, `omniscience`) | `ZQXSECRET`, `ZQXSECRET_<branch>` on the local and the remote | **alias** (`private_local_branch`) |
| A2 | memory branch (`.memory`) and its twin | `ComplexGitSync_ZQXSECRET` (remote too) | **alias** (`MemoryRepository.branch`, same function) |
| A3 | memory commit message | `ZQXSECRET memory, <date>: N state(s), M ledger entr(ies)` (`tree/memory/repository.py:193`) | **alias** |
| A4 | memory `state/<sha>.gts` | `name = "ZQXSECRET"` twice, `project_name`, `repo_name`, the tree outline (`ZQXSECRET (root) ...`), `br=<private branch>` in the outline, `fallback_reason`, `target_ref`, `ref` | **alias** for every field naming the project or a private branch. The root's `repo_name` is the root repository's own name: see Q3 |
| A5 | memory `state/<sha>.gts`: `root_absolute_path` | the local checkout path, which usually ends in the project's name | **omit** under `anonymous` (a path of the owner's machine, written into a shared register) |
| A6 | memory `commit-logs/<sha>.toml` | `branch = "ZQXSECRET"`, `ref = "refs/heads/ZQXSECRET"` | **alias** |
| A7 | memory `lgr/`, `env/`, `README.md` | no occurrence found | **keep** |
| A8 | omniscience record header (`omniscience_record.py` lines 81, 114, 174, 194): field `project` | the project name, and an `os_id` that is the **full SHA-256 of the name** | **alias** for `project`. `os_id` can be tested against a guessed name exactly like the 6-digit hash, so it must be derived from the alias, not the name: see Q7 |
| A9 | omniscience branch (`OmniscienceRepository.branch`, `private_local_branch`) | `<project>[_<branch>]` | **alias** (same function as A1) |
| A10 | commits and tags of private/local repositories | `commit --private`, `push --private`, `tag --private`: no occurrence (the user's own commit message and tag name are the user's) | **keep** |
| A11 | `register_filename = f"{project_name}.lgr"` (`orchestre/document_loader.py:349`) | the register file is local to the root, not shared | **keep** (local) |
| A12 | the project's own `.cgs` and the root repository | the real name | **keep**: that is where the real name lives |
| A13 | `self-history` records (written on the memory's branch) | not probed; the record holds the ticket and the role, read in code | **keep**, to be re-checked by the acceptance grep |

What this changes in the plan. Step 4 (naming) covers A1, A2, A9 through one
function, and is cheap. Steps 5 and 6 are where the work is: the `.gts`
writer (A4, A5), the memory commit message (A3), the commit-log (A6) and the
omniscience record (A8) each need an alias-aware writer, and the memory's
past commits keep the old name in history.

## 7. Decisions raised by the audit

- **Q3 (now concrete): the repository names inside a State.** A4 writes every
  repository's `project_owner_name`, `repo_name` and the `gitprovider` into
  `.memory`. Recommended: alias only what names the **project** (the project
  name, the root's `repo_name` when it equals the project name, and every
  private branch), and keep the other repositories' names, which belong to
  the shared repositories themselves. The alternative aliases every URL
  component and makes a State unusable to re-clone a tree.
- **Q7: `os_id`.** Derive it from the alias under `anonymous` (recommended:
  the record then reveals nothing a guess can confirm, but the project's
  `os_id` changes with the mode and the alias), or leave it, which keeps a
  testable fingerprint of the name in `omniscience`.
- **Q8: `root_absolute_path` (A5).** Omit under `anonymous` (recommended), or
  keep.

## 8. Answered by the owner, 2026-11-21

- **Q1:** `"sequence"` is the default mode.
- **Q2:** the claim is `sha256(name)`.
- **Q4:** `anonymise` has `--delete-old`, with a confirmation that names each
  branch.
- **Q5:** (b) a minimum version in `environment.tools`, checked before
  cloning, plus (a) refusal of any unknown key in the `project` table only,
  after an audit of the checked-in `.cgs` files.

- **Q3, Q7, Q8 and the audit (owner, 2026-11-21):** the audit of §6 is validated as written. Q3: alias only
  what names the project (its name, the root's `repo_name` when it equals it, every private branch) and keep the
  other repositories' names. Q7: `os_id` is derived from the alias. Q8: no machine path in a State.
- **Q9: ceilings (raised, owner, 2026-11-21):** `cli/expert.py` 2219 to 2229 (and 2518 to 2530 in the OO
  baseline), `cli/help_text.py` 209 to 210, `orchestre/client.py` 1418 to 1422, `orchestre/document_loader.py` 357
  to 358, `orchestre/installer.py` 715 to 716, `tree/operations/branch.py` 609 to 612, `tree/registry.py` 459 to 470.

## 9. What was built, and what was not (worker's report, 2026-11-21)

Built: `ProjectAlias` (Ring 0), the `anonymous` option and the refusals of §2 (`tree/project_table.py`), the
resolution against the claim (`orchestre/anonymous_install.py`), the claim stamp at `branch create` and
`memory branch` (`tree/operations/project_claim.py`), the tree named by its alias, the State written with the alias
and no path (`tree/anonymous_state.py`), the memory's commit messages, `cgitsync anonymise` with `--dry-run` and
`--delete-old`, and the docs. `tests/integration/test_anonymous_project.py` greps every shared repository, remote
included, for the real name after `bootstrap`, `branch create`, `push --private` and `memory push`: none.

Deviations and limits, for the owner:

- **Q5 (b) cannot protect a released cgitsync.** An unmodified 8.10.x accepts an unknown key in the `project` table
  and an unknown top-level key without a word (probed), and `env check` never blocks. No `.cgs` form makes it
  refuse. Q5 (a) is done: from this version, an unknown `project` key is refused. The warning on
  `compta/.config/compta-dev.cgs` therefore stays until every machine runs this version or a later one.
- **A re-clone of the root from a State alone is not possible** when the root repository carries the project's
  name: the State says the alias. Every other repository re-clones as before. This is the cost of Q3.
- **Not exercised on a mounted omniscience repository.** The record's `project` and `os_id` come from the tree's
  name, which is the alias; the acceptance grep must be run on the real tree (§4, owner run), which also covers
  `.self-history`, `.dev` and `.claude`.
- **History keeps the old name** after `anonymise`: commits already written and the States already in the memory.
- **Open after the orchestrator's review (non-blocking, 8.11.0):** the `<name>_` prefix match in `anonymise` can
  pick up another project's `<name>_x` branches (the dry run lists every pair, `--delete-old` confirms each by
  name); `ProjectClaim.stamp` commits whatever is already staged, does not restore a detached HEAD, and its
  checkout can fail on a dirty worktree that differs between branches. The ticket stays open for the owner run of
  section 4 on the real tree.

