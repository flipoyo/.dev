# AgenticTwoLevels — every agentic rule at two levels: the pattern in `.distant`, the fill-in in `.local`

*Created: 2026-10-08*

*Branch: main*

> **Implemented — 2026-10-08, archived on the owner's word.** The two-level
> spec tree landed in `cgitsync4.4.3`: every agentic rule is a shared
> pattern in `.agent/.distant/` with at most one local fill-in in
> `.agent/.local/`, `DevTickets/` moved to `.dev`, `.versioning` was folded
> into `.dev` and `.auto` dropped. The status note below is the last word
> on what the worker left to the owner; this archive does not restate
> whether each of those GitHub steps was done.

> **From the owner's short ticket**
> [reorg-distant-local](../archive/.closedUserTicket/20261008_reorg-distant-local.md)
> (2026-10-08): rationalise the agentic control, which is spread over too
> many files; move what is general and reusable to `.distant` and keep only
> what is strictly needed in `.local`, which "implements the additionalSpec
> for local"; SemVer versioning is the example; DevTickets belong in `.dev`,
> not `.localSpec`, because tickets are process, not specs; and the number of
> repositories is open to question.

> **Decided — owner, 2026-10-08, in conversation.** All six recommendations
> in §6 are accepted. One addition: *"consider if dogfooding is useful. For
> me the `install.cgs` being public and `project-name4dev.cgs` is a general
> convention for project development that matches the src and `.memory`
> management. So auto may be useless."* It becomes D7: the two-installs
> convention is a distant pattern, `.auto` is dropped, and `dogfooding.md` is
> not carried anywhere. The owner implements the repository changes on
> GitHub from §9. TicketTreeMove is absorbed and archived in the same pass
> (D2), and the short ticket is closed.

> **Status — 2026-10-08, worker.** WP1 to WP5 are done in the working trees
> and nothing is committed or pushed. The first orchestrator quote scored the
> work 76/100 and found defects; the worker fixed them and released 4.4.3.
> `DevSpec` and `.ticketing` carry their change as **uncommitted edits** in
> the mounts, ready for the owner to commit and push (the earlier unpushed
> commits were undone, so the mounts are no longer ahead). WP6: lint, both
> spec-tree checks and `check-ceilings` pass; the suite is 2048 passed, 0
> failed; `cgitsync status` shows `errors=0`. **Still open:** §9 steps 1, 3
> and 5 (GitHub), a fresh `bootstrap` of the new developer spec once `.dev`
> carries `DevTickets/` on GitHub, and the orchestrator's second quote and
> self-history record. Archive this ticket when those are done.

## Abstract — read this first

**The one-line version.** Each agentic topic gets exactly two documents:
the shared *pattern* in `.agent/.distant/`, and a short local *fill-in* in
`.agent/.local/` that states only what the pattern leaves open. The local
side shrinks from five repositories to three, and `DevTickets/` moves into
`.dev`.

**What this document is.** The analysis of today's agentic tree, the target
structure, the content moves file by file, the work packages in order, the
decisions taken, and the repository-by-repository map of what changes on
GitHub.

**Why it exists.** Today the same rule is often written two or three times
(versioning, the commands, the before-committing checklist, the module
table). Some generic rules sit in local files, so other projects cannot
reuse them. Several documents still describe the `.agentSpec` layout that
was retired on 2026-09-22. An agent cannot tell which copy is the real one,
and DOCSTYLE §7 (one authoritative file per purpose) is broken in many
places.

**What you will find.** §1 what is there today. §2 the two-level rule.
§3 the target structure and the repository count. §4 what moves where.
§5 the work packages, in order. §6 the decisions, all taken. §7 effect on
other tickets. §8 acceptance. §9 the GitHub map.

**Who it is for.** The owner, who sets up the repositories from §9, and the
worker and orchestrator who implement §5.

**What you need to do with it.** Owner: §9, in its order. Implementer:
follow §5 in order. WP1's link check comes before any file moves, so every
link the moves break is printed in a list instead of being found one at a
time.

```mermaid
graph LR
    subgraph D[".agent/.distant — the pattern, shared, read-only"]
        DS["dev-sync<br/>DevSpecs (+ two installs) · AgentConduct · AGENT template<br/>+ Versioning · SpecTree (new)"]
        TK["ticket<br/>TICKETLIFECYCLE<br/>+ the short-ticket loop"]
        DC["documentation<br/>DOCSTYLE · DocSpecs"]
    end
    subgraph L[".agent/.local — the fill-in, ours"]
        CL[".claude<br/>CLAUDE.md: map + digest"]
        LS[".localSpec<br/>AdditionalSpecs · AGENT · digest · manifest · audit"]
        DV[".dev<br/>checklist · Versioning · bump_version.py<br/>DevTickets/"]
    end
    DS -->|filled in by| LS
    DS -->|filled in by| DV
    TK -->|filled in by| DV
    DC -->|filled in by| LS
    CL -->|reading order| LS
    CL -->|reading order| DV

    classDef here fill:#1565C0,color:#fff,stroke:#111,stroke-width:2px;
    class DV here;
```

---

## 1. What is there today

### 1.1 Inventory

Eight agentic repositories, all declared in `examples/complexgitsync4dev.cgs`:

| Side | Mount | Repository | Holds | Lines of spec |
|---|---|---|---|---|
| distant | `ticket` | `.ticketing` | `TICKETLIFECYCLE.md` | 320 |
| distant | `dev-sync` | `DevSpec` | `DevSpecs.md`, `AgentConduct.md`, `AGENT.md` template, `AgentDataContract.md`, `legalTerms/`, `agent-contracts/` | 1 000 |
| distant | `documentation` | `DocSpec` | `DOCSTYLE.md`, `DocSpecs.md`, a Slidev theme | 350 |
| local | `.claude` | `.claude` | `CLAUDE.md`, `AGENT.md` pointer, `settings.json` | 510 |
| local | `.localSpec` | `.localSpec` | `AdditionalSpecs.md`, `AGENT.md`, `audit.md`, `digest.md`, `AgenticManifest.md`, **`DevTickets/`**, a one-off rescue script | 2 500 + tickets |
| local | `.dev` | `.dev` | `cgitsync-dev.md` | 100 |
| local | `.versioning` | `.versioning` | `Versioning.md`, `scripts/bump_version.py` | 215 + script |
| local | `.auto` | `.auto` | `dogfooding.md` | 58 |

### 1.2 The same rule written more than once

| Rule | Copies | Notes |
|---|---|---|
| Versioning (SemVer, two numbers, who bumps what, `bump-version`, release register) | `.versioning/Versioning.md` **and** `AdditionalSpecs.md` §Versioning (lines 1972–2155) | Near-verbatim; the two already differ in three paragraphs. The generic third is also partly in `DevSpecs.md` §Versioning and `AgentConduct.md` §1.3. |
| Commands and bootstrapping | `CLAUDE.md` §Commands **and** `.dev/cgitsync-dev.md` §Commands | The `.dev` copy is stale: wrong `bootstrap` arguments, `bump-build` "alone". |
| Before-committing checklist, filled in | `CLAUDE.md` §Before committing **and** `.dev/cgitsync-dev.md` | The `.dev` copy still says to add new commands to the README command table, which the owner banned on 2026-10-06. |
| Module responsibility table | `CLAUDE.md` §Architecture boundary **and** `AdditionalSpecs.md` §Responsibility boundaries | Two tables in different shapes (with and without the Ring column). |
| Testing layout | `AdditionalSpecs.md` §Testing **and** `.dev/cgitsync-dev.md` §Testing | Already different. |
| The two installs, and the tree layout | `CLAUDE.md` §Layout, `AgenticManifest.md`, `.auto/dogfooding.md`, the comment block in `complexgitsync4dev.cgs` | `dogfooding.md` says itself it is stale and still describes `.agentSpec`. |
| The short-ticket loop | `DevTickets/README.md` §2–§3a **and** `TICKETLIFECYCLE.md` §6 | Nothing in the loop is specific to this project. |
| Reading order | `.claude/AGENT.md` **and** `CLAUDE.md` abstract and graph | |

### 1.3 Generic rules sitting on the local side

These hold for any project that follows DevSpec, so other projects cannot
reuse them while they stay local:

- **Versioning pattern.** It is a judgement, never CI. It uses two numbers
  with two rhythms (a release version and a build counter). The worker bumps
  the build and the orchestrator chooses the level. Every build is released,
  `patch` at least. A follow-up fix gets its own patch. "Patch" from the
  owner means this rule. Today all of this sits in `.versioning/Versioning.md`.
- **The short-ticket loop.** The owner writes a short ticket. One pass
  brings every open ticket and spec into line with it. The short ticket is
  then stamped and closed, and never edited again. Today this sits in
  `DevTickets/README.md`.
- **The spec-tree pattern.** `digest.md` is loaded in full every session.
  It has one line per MUST/NEVER rule, each with a citation. A manifest
  lists the mounts and their spec files, and a check keeps both honest.
  Today this sits in `AdditionalSpecs.md` §Spec tree. The pattern answers an
  incident that any agent-driven project can have (SpecTree §1).
- **The two installs** (D7). The public repository carries `install.cgs`,
  the user install (the project's own repositories: source and
  documentation). It also carries `<project-name>4dev.cgs`, the developer
  install: the same, plus every agentic mount and the project's `.memory`.
  That split is the same one the tool draws between project repositories and
  the private repositories that configure them. Today it sits in `CLAUDE.md`
  §Layout and `.auto/dogfooding.md`.
- **Workstream branches.** A workstream gets its own branch when it
  migrates a stored format, not because of its subject matter. Only the
  general idea is distant; the list of branches stays local.

### 1.4 Stale or misplaced on either side

| Where | Problem |
|---|---|
| `DevSpecs.md` preface and §Planning (distant) | Still describes tickets in an `AgentSpec/` directory inside the project's own repository, and the `.agentSpec` bundle. This contradicts `TICKETLIFECYCLE.md` §1.1, which keeps tickets private. |
| `TICKETLIFECYCLE.md` §4, §7 (distant) | Links to `DevSpec/DOCSTYLE.md`, a path that no longer exists. Uses `.localSpec/DevTickets/` as its example. |
| `DevSpec/README.md` (distant) | Still describes mounting inside `.agentSpec`. |
| `DocSpec/slidev/themes/piren-seine` (distant) | One project's theme in a shared repository. Out of scope here; noted for a later ticket. |
| `.localSpec/README.md` | Describes the `.agentSpec` split, and a `scripts/` folder that moved to `.versioning`. |
| `DevTickets/TicketSummary.md` | Lists tickets that no longer exist (`UserDevProfile`, `LocalRunLogs`). Breaks `DevTickets/README.md` §1 ("`DevTickets/` holds nothing else"). |
| `.localSpec/scripts/rescue_20260922_memory_ledger_splice.py` | A one-off repair from 2026-09-22, kept beside the specs. |
| `.claude/settings.local.json.tmp.15108.*` | A stray temporary file. |
| `AdditionalSpecs.md` §Branches | Says `.agentSpec` sits on `main`. |
| `github:flipoyo/.dev` | Has only a `ComplexGitSync` branch, yet `complexgitsync4dev.cgs` gives it `fallback_branch = "main"`. A fresh project mounting it would find no fallback. |

### 1.5 What is *not* a problem

- **`AgentConduct.md`** is already split correctly: the shape is distant,
  and each project's fill-ins are in `CLAUDE.md`. It is the model to copy.
- **`agent-contracts/`** sits in the distant `DevSpec` repository on
  purpose (the AgentContract ticket, archived). The attestation is per
  provider and per owner, not per project. It stays where it is.
- **`.agent/` is a plain directory and not a repository** (AgentMountSplit).
  That rule stays: every mount is declared directly.

## 2. The two-level rule

Every agentic topic has **one pattern and at most one fill-in**:

- **The pattern** (in `.agent/.distant/`, on `main`) states the rule, why it
  exists, and the choices it leaves open. It names no project, no path
  inside a project, and no command of a specific tool.
- **The fill-in** (in `.agent/.local/`, on the project's branch) opens with
  a line `*Fills in: <path to the pattern>*`. It states **only**:
  1. which open choice the project made, and why;
  2. the project's own names: commands, paths, files, branches;
  3. any exception the project makes, with the owner's name and date.

  It never restates the pattern. When the pattern needs a change, the
  change goes in the pattern.

A project with no exception and no choice to make needs no fill-in. That
is the "strict necessary" the short ticket asks for. The two installs (D7)
are the first case: the pattern names the file `<project-name>4dev.cgs`, and
the only local fact left is the folder it sits in, which is one line in
`CLAUDE.md`'s map.

`scripts/spec_tree.py` checks this mechanically (D5). Every `*Fills in:*`
line must name a file that exists on the distant side. Every local spec
listed in `AgenticManifest.md` must carry such a line, or be marked
`standalone` (product specs such as most of `AdditionalSpecs.md`, `audit.md`
and `digest.md`).

## 3. Target structure

### 3.1 How many repositories

| Option | Distant | Local | Total | Verdict |
|---|---|---|---|---|
| A — today | 3 | 5 | 8 | `.versioning` holds one document and one script, and `.auto` one stale document. Five local mounts for three questions. |
| **B — decided (D1, D7)** | 3 | 3 | 6 | Each local repository answers one question. `.claude`: what an agent is handed at session start. `.localSpec`: how the product is built (specs). `.dev`: how work gets done (checklist, versioning, tickets). `.versioning` is folded into `.dev`. `.auto` is dropped: its one real rule is the two-installs convention, which becomes a distant pattern. Each distant repository keeps one topic that other projects can mount alone. `DocSpec` is already mounted by documentation-only projects. |
| C — one distant repository | 1 | 3 | 4 | Folds `.ticketing` and `DocSpec` into `DevSpec`. Fewer mounts, but it undoes AgentSkillsSplit. A project that only writes documents would have to mount the whole development philosophy. Not now. |
| D — one repository per topic, `main` = pattern, project branch = fill-in, mounted twice | — | — | 3 | It looks elegant, but `cgitsync` clones a repository once per identifier (see the `.cgs` comment on mounting a repository twice). Every pattern change would also need a merge into every project's branch. Rejected. |

`.claude` stays separate from `.localSpec`. Its `main` branch carries the
`settings.json` baseline that every project inherits, and Claude Code
expects `CLAUDE.md` at a fixed path, reached through the root symlink.

### 3.2 Pairing, topic by topic

| Topic | Pattern (distant) | Fill-in (local) |
|---|---|---|
| Development philosophy | `dev-sync/DevSpecs.md` | `.localSpec/AdditionalSpecs.md` (standalone product spec, plus a short fill-in section for the choices `DevSpecs.md` leaves open: lifecycle states, versioning scheme pointer, documentation additions) |
| The two installs | **new** `dev-sync/DevSpecs.md` §Two installs | none: one line in `CLAUDE.md`'s map says the developer spec is `examples/complexgitsync4dev.cgs` |
| Agent conduct: checklist, commit message, attribution, pair rule | `dev-sync/AgentConduct.md` | `.dev/cgitsync-dev.md`: the 8 steps with this project's commands, project name `cgitsync`, the README *LLM assistance* section, the `vendor-name`/`model-name` rule |
| Agent roles | `dev-sync/AGENT.md` (template) | `.localSpec/AGENT.md` |
| Versioning | **new** `dev-sync/Versioning.md` | `.dev/Versioning.md`: SemVer chosen, positions mapped to the CLI contract, the five files `bump-version` syncs, `scripts/bump_version.py`, the release register and `freeze_release` |
| Data contract | `dev-sync/AgentDataContract.md` + `legalTerms/` | `CLAUDE.md` §Whose data this is (unchanged, already a fill-in) |
| Spec tree and digest | **new** `dev-sync/SpecTree.md` | `.localSpec/digest.md`, `.localSpec/AgenticManifest.md`, `scripts/spec_tree.py` |
| Tickets | `ticket/TICKETLIFECYCLE.md`, **extended** with the short-ticket loop | `.dev/DevTickets/README.md`: where `DevTickets/` lives, and this project's branches (moved from `AdditionalSpecs.md` §Branches) |
| Documents | `documentation/DOCSTYLE.md`, `DocSpecs.md` | the root-README exception and the `.tex` paths, in `AdditionalSpecs.md` |
| Session entry | — (Claude Code specific; baseline on `.claude`'s `main`) | `.claude/CLAUDE.md`: what the project is, load `digest.md`, the two-level map (§3.3), the reading order |

### 3.3 Target tree

```
.agent/
├── .distant/                         shared, read-only, branch main
│   ├── dev-sync/      (DevSpec)      DevSpecs (+ §Two installs) · AgentConduct · AGENT template
│   │                                 Versioning (new) · SpecTree (new)
│   │                                 AgentDataContract · legalTerms/ · agent-contracts/
│   ├── ticket/        (.ticketing)   TICKETLIFECYCLE (+ the short-ticket loop)
│   └── documentation/ (DocSpec)      DOCSTYLE · DocSpecs · slidev/
└── .local/                           ours, writable, branch ComplexGitSync
    ├── .claude/                      CLAUDE.md · AGENT.md · settings.json
    ├── .localSpec/                   AdditionalSpecs · AGENT · audit · digest · AgenticManifest
    └── .dev/                         cgitsync-dev · Versioning · scripts/bump_version.py
                                      DevTickets/{README, shortTickets, openTickets, archive}
```

`.claude/AGENT.md` stays as a symlink target, because the root `AGENT.md`
points at it. It shrinks to three lines pointing at `CLAUDE.md`'s reading
order, so the order is stated only once.

## 4. What moves where

### 4.1 To the distant side (pattern extracted, local copy reduced to a fill-in)

| From | To | Content |
|---|---|---|
| `.versioning/Versioning.md` §Two numbers, §Who bumps what, the three "agents got this wrong" cases | `dev-sync/Versioning.md` | Stated without `cgitsync`, `pyproject.toml` or `__build__`: "the packaging manifest", "the build counter". `DevSpecs.md` §Versioning shrinks to the choice of scheme and a link. |
| `CLAUDE.md` §Layout (the `install.cgs` / `complexgitsync4dev.cgs` paragraph) and `.auto/dogfooding.md` §Two specs | `dev-sync/DevSpecs.md` §Two installs (new) | `install.cgs` at the public repository's root, the user install: the project's own repositories only. `<project-name>4dev.cgs`, the developer install: the same, plus every agentic mount and the project's `.memory`. It is what the project manages its own tree with and what CI reconstitutes. Where a `.cgs` sits never changes the tree it describes. D7. |
| `DevTickets/README.md` §2, §3, §3a | `ticket/TICKETLIFECYCLE.md` §6 (extended) | The loop and the closing rule. §6 already holds half of it. |
| `AdditionalSpecs.md` §Spec tree (the idea, not the script) | `dev-sync/SpecTree.md` | Digest loaded every session, one line per rule with a citation, a manifest of mounts, a check that fails on drift, and the "fills in" line from §2. |
| The two-level rule itself (§2 above) | `DevSpecs.md` preface, replacing its stale `.agentSpec`/`AgentSpec/` text | One paragraph, plus a link to `SpecTree.md`. |
| `DevSpecs.md` §Planning (stale) | Rewritten as three lines pointing at `TICKETLIFECYCLE.md` | Removes the contradiction in §1.4. |

### 4.2 Within the local side

| From | To | Why |
|---|---|---|
| `.localSpec/DevTickets/` | `.dev/DevTickets/` | Tickets are process, not specs (the short ticket; TicketTreeMove §6). |
| `.versioning/*` | `.dev/Versioning.md`, `.dev/scripts/bump_version.py` | D1. |
| `AdditionalSpecs.md` §Versioning | deleted; a single link to `.dev/Versioning.md` | Duplicate (§1.2). |
| `AdditionalSpecs.md` §Testing | merged into `.dev/cgitsync-dev.md` §Testing | Duplicate. |
| `AdditionalSpecs.md` §Branches and ticket topics | `.dev/DevTickets/README.md` | It is process, not product. The `.agentSpec` line is corrected on the way. |
| `CLAUDE.md` §Commands, §Bootstrapping, §Before committing bodies | `.dev/cgitsync-dev.md` | D3. `CLAUDE.md` keeps the step titles. |
| `CLAUDE.md` module table | removed; `AdditionalSpecs.md` §Responsibility boundaries is the only copy | D4. |
| `CLAUDE.md` §Layout mount list | removed; `AgenticManifest.md` is the only list | Already the authoritative file, by its own abstract. |

### 4.3 Deleted

- `.auto/dogfooding.md`, with nothing carried over except the two-installs
  rule (D7). The rest describes a layout that no longer exists.
- `DevTickets/TicketSummary.md` (D6).
- `.claude/settings.local.json.tmp.*`.

The rescue script moves to `.dev/DevTickets/archive/` beside the ticket it
served (D6). `.localSpec/README.md` is rewritten, not deleted, because every
repository keeps a README.

The `.versioning` and `.auto` repositories on GitHub are **archived by the
owner**, not deleted (§9). States already recorded in `.memory` name them,
and an archived repository can still be cloned to restore one. No agent
deletes a remote repository.

## 5. Work packages, in order

Each WP is its own commit, or its own commit per repository. No WP mixes a
`MOVE` with a `CHANGE` (`dev-sync/AGENT.md`, handoff rules).

**WP1 — the link check first** (absorbed from TicketTreeMove §1 and §3, D2).
Fix the stale ticket citations listed in TicketTreeMove §1. Add the check
from its §3 to `pixi run check-ceilings` (TicketTreeMove's D2: not on the
commit path). Widen it from `.localSpec/DevTickets/` to every `.agent/` path
cited in `src/`, `tests/` and `scripts/`, plus the relative links inside
tickets. Cite an open ticket by name only (TicketTreeMove's D1). The check
skips, and does not fail, when the private mounts are absent. Run it and
record the baseline.

**WP2 — distant patterns** (D4: the worker prepares, the owner pushes). One
commit per distant repository, never bundled with the project's own commit:
- `DevSpec`: new `Versioning.md` and `SpecTree.md`; `DevSpecs.md` preface
  rewritten as the two-level rule; new §Two installs (D7); §Planning and
  §Versioning shortened to pointers; README corrected.
- `.ticketing`: `TICKETLIFECYCLE.md` §6 extended with the loop; dead
  `DevSpec/DOCSTYLE.md` links fixed; project-specific examples made
  generic.
- `DocSpec`: no change in this ticket.

**WP3 — local structure** (moves only, no rewording). Starts once §9 steps 1–3
are done on GitHub. Create `.dev/DevTickets/` and move the tree into it.
Fold `.versioning` into `.dev`. Then update:
- `examples/complexgitsync4dev.cgs`: remove the `.versioning` and `.auto`
  entries and update the comment block;
- `AgenticManifest.md`: two mounts and their spec files removed;
- `pixi.toml`: the `bump-version` task path;
- `scripts/spec_tree.py` constants;
- `tests/unit/test_repo_scope.py`, `test_documents.py` and
  `test_git_branch.py`, which list the mounts by name;
- `tutorials/05_private_repos.md`: the status output and the scope table
  name `.versioning` and `.auto`;
- every `.localSpec/DevTickets/` citation in `src/` and `tests/` (about 80),
  rewritten with the WP1 check as the list;
- the relative links inside tickets, one level deeper.

Run `pixi run bump-build`, then `bump-version patch`, because docstrings in
`src/` and a pixi task changed.

**WP4 — local content** (rewording only). Rewrite each local file as a
fill-in per §2, using §4.2's table:
- `cgitsync-dev.md` absorbs `CLAUDE.md`'s command and checklist bodies,
  and the stale copy is dropped;
- `.dev/Versioning.md` keeps only the project's choices;
- `DevTickets/README.md` keeps only the location and the branches;
- `AdditionalSpecs.md` loses §Versioning, §Testing and §Branches;
- `CLAUDE.md` becomes the map from §3.3 plus the digest pointer and the
  data-contract and attribution fill-ins, under 150 lines;
- `.claude/AGENT.md` shrinks to a pointer.

**WP5 — clean-up and the check.** Delete the files in §4.3. Add the
`*Fills in:*` check to `spec_tree.py` (D5). Update every `digest.md`
citation that moved, with one line each for the two-level rule and the two
installs.

**WP6 — prove it.** Run, from a **fresh** `bootstrap` of
`examples/complexgitsync4dev.cgs` as well as from this tree:
- `pixi run lint` and `pixi run test`;
- `pixi run check-spectree` (`--check` and `--check-digest`);
- `pixi run check-ceilings`;
- `cgitsync status` (it must show `errors=0`).

Then deliver **one** commit message, the same for every touched repository
(`AgentConduct.md` §2): the project, `.claude`, `.localSpec`, `.dev`, `DevSpec`
and `.ticketing`. After that the
owner does §9 step 5.

## 6. Decisions — all taken, owner, 2026-10-08

| D | Question | Decided |
|---|---|---|
| **D1** | How many local repositories? | **Three**: `.claude`, `.localSpec`, `.dev`. `.versioning` is folded into `.dev`, and its GitHub repository is archived. |
| **D2** | What happens to TicketTreeMove? | **Absorbed.** Its citation fix and check become WP1, and its move becomes WP3. It was archived as superseded on 2026-10-08, in the pass that accepted this ticket. |
| **D3** | How much stays in `CLAUDE.md`? | **The map, the digest pointer, the 8 checklist step titles (one line each), and the data-contract and attribution fill-ins.** Command and step bodies move to `.dev/cgitsync-dev.md`. Target: under 150 lines, from 477. |
| **D4** | How are the distant repositories edited? | **The worker prepares each distant change as its own commit in a separate clone. The owner reviews and pushes it.** Never `writable = true` on the mount, not even for a short time: that changes the tree's scope and the `.gts` that attests it. |
| **D5** | Does `spec_tree.py` enforce the `*Fills in:*` line? | **Yes, in `--check`.** |
| **D6** | `TicketSummary.md` and the rescue script? | **`TicketSummary.md` is deleted. The rescue script moves** into `.dev/DevTickets/archive/` beside the ticket it served. |
| **D7** | Is dogfooding (`.auto`) useful? | **No, not as a mount.** "`install.cgs` public, `<project-name>4dev.cgs` for development" is a general convention, and it matches the split between the project's source and its `.memory`. It becomes `DevSpecs.md` §Two installs. `.auto` is removed from the developer spec and its GitHub repository is archived. |

## 7. Effect on other tickets

- **TicketTreeMove**: absorbed and archived as superseded, 2026-10-08 (D2).
  Ranks in pile 2 are not renumbered now; the next Ticket review compacts
  them (TICKETLIFECYCLE §2.1).
- **WorkingAreaRename**, **Omniscience**, every **data-repo** ticket: their
  relative links change depth in WP3. The change is mechanical and covered
  by WP1's check, and their content does not change.
- **PackageHygiene**: no overlap. It is about the public package, not the
  agentic tree.
- The short ticket **reorg-distant-local** was closed on 2026-10-08, in the
  same pass.

## 8. Acceptance

- Every agentic topic has one pattern in `.agent/.distant/` and at most one
  fill-in in `.agent/.local/`. Every fill-in opens with `*Fills in:*`, and
  `spec_tree.py --check` fails if one points nowhere.
- No rule in §1.2 exists twice: a `grep` for each of its key sentences
  finds one file.
- `.agent/.local/` holds three mounts. `DevTickets/` is at
  `.agent/.local/.dev/DevTickets/`, and a fresh bootstrap of
  `examples/complexgitsync4dev.cgs` produces it.
- `DevSpecs.md` states the two installs. No `.cgs` in this project declares
  `.versioning` or `.auto`.
- `DevSpecs.md`, `TICKETLIFECYCLE.md` and every local README describe the
  current layout. No document describes `.agentSpec` or an `AgentSpec/`
  directory as current.
- `CLAUDE.md` is under 150 lines (D3).
- No `.agent/` path cited in `src/`, `tests/`, `scripts/` or any open ticket
  fails to resolve. The check passes in a checkout without the private
  mounts.
- `pixi run lint`, `pixi run test`, `check-spectree`, `check-ceilings` pass,
  and `cgitsync status` from the tree's own root shows `errors=0`.

## 9. The GitHub map — what the owner does, repository by repository

Read it in step order. Steps 1–3 must land before WP3 changes the `.cgs`,
because a bootstrap of the new `.cgs` reads these branches. Step 5 comes
only after `main` of `ComplexGitSync` no longer declares the two
repositories.

| Step | Repository | Branch | What changes | Who |
|---|---|---|---|---|
| 1 | `flipoyo/.dev` | **new `main`** | Create it with a README only: "each project gets its own branch, named after the project; `main` carries nothing project-specific". The `.cgs` already gives `.dev` `fallback_branch = "main"`, and today no `main` exists. This is the same convention `.localSpec` and `.claude` follow. | Owner |
| 2 | `flipoyo/DevSpec` | `main` | WP2: `Versioning.md` and `SpecTree.md` added; `DevSpecs.md` preface, §Two installs, §Planning and §Versioning; README. One commit. It reaches every project that mounts `DevSpec`. | Worker prepares, owner pushes |
| 2 | `flipoyo/.ticketing` | `main` | WP2: `TICKETLIFECYCLE.md` §6 extended with the loop, dead links fixed. One commit. | Worker prepares, owner pushes |
| 3 | `flipoyo/.dev` | `ComplexGitSync` | WP3 receives: `DevTickets/` (copied from `.localSpec`), `Versioning.md` and `scripts/bump_version.py` (copied from `.versioning`). WP4 then rewrites `cgitsync-dev.md` and the README. | Worker, committed through `cgitsync commit --private` |
| 4 | `flipoyo/.localSpec` | `ComplexGitSync` | WP3 removes `DevTickets/` and `scripts/`. WP4 trims `AdditionalSpecs.md` and rewrites the README. WP5 updates `digest.md` and `AgenticManifest.md`. | Worker |
| 4 | `flipoyo/.claude` | `ComplexGitSync` | WP4: `CLAUDE.md` slimmed, `AGENT.md` reduced to a pointer, the stray `.tmp` file deleted. | Worker |
| 4 | `flipoyo/ComplexGitSync` | `main` | WP1 check; WP3 `.cgs` entries removed, `pixi.toml` task path, `spec_tree.py`, citations in `src/` and `tests/`, three test files, tutorial 05. It is released as a patch. | Worker |
| 5 | `flipoyo/.versioning` | — | **Archive** (Settings → Danger Zone → Archive this repository). Do not delete it: recorded States name it. | Owner |
| 5 | `flipoyo/.auto` | — | **Archive**, same reason. | Owner |
| — | `flipoyo/DocSpec`, `flipoyo/.memory`, `flipoyo/DocComplexGitSync` | — | No change. | — |

**Moving files between repositories.** A plain copy is enough. The history
stays readable in the source repository, which is archived (`.versioning`)
or keeps its own past commits (`.localSpec`). The receiving commit names
the source commit it copied from. To carry the history across instead, use
`git subtree split --prefix=DevTickets` in `.localSpec` and merge the result
into `.dev`. That only adds commits; it rewrites nothing in either repository.

**After the change, six agentic repositories remain:**

| Mount | Repository | Branch | Side |
|---|---|---|---|
| `.agent/.distant/dev-sync` | `DevSpec` | `main` | distant |
| `.agent/.distant/ticket` | `.ticketing` | `main` | distant |
| `.agent/.distant/documentation` | `DocSpec` | `main` | distant |
| `.agent/.local/.claude` | `.claude` | `ComplexGitSync` | local |
| `.agent/.local/.localSpec` | `.localSpec` | `ComplexGitSync` | local |
| `.agent/.local/.dev` | `.dev` | `ComplexGitSync` | local |
