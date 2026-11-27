# DataArchitecture — data is a capability of a repository, not a kind of repository

*Created: 2026-09-16*

*Branch: HT-BETA*

> **Ticket review — 2026-11-27, on the owner's request** *"shortTicket review and write DevPlanTickets in a proper order of execution. Merge paralell tasks in the same tickets. The goal is a CGS-HT-BETA ready for htbs."* Renumbered `data-repo_2-6` → `HT-BETA_2-6`, and the workstream moves to `HT-BETA`: no `data-repo`
> branch was ever pushed, and M1 (DataSchema, 8.14.1) and most of M2 (DataBackendContract, 8.14.2) landed on
> `HT-BETA`. The milestones are regrouped by what can run together and by what HTBS needs first (§3, rewritten):
> **DvcBackend** (the rest of M2, and DataServerAddress), then **DataRoundTrip** (the HTBS slice of M3 to M6:
> `status`, `push`, `pull`, `release freeze`, and the real-DVC test), both in pile 1. Then, in pile 2,
> **DataWorkspace** (M3 and M4, merged because they run in parallel), **DataPublication** (the rest of M5) and
> **DataAcceptance** (the rest of M6). The safety argument of *The branch* (§3) now rests on each ticket's acceptance,
> as `memory-dev`'s did when it closed: nothing lands that a Git-only tree can see.
> **Short ticket `server-ip` — 2026-11-25.** A data repository names its DVC server by an alias, `service = "<alias>"`, and its address is never written in any file cgitsync writes: [DataServerAddress](HT-BETA_1-3_DvcBackend_DevPlanTicket.md) (2-16). It lands after M2 and before M4 and M5, which need a remote. It takes the place of the "§7 C2" that `git_repo/data_spec.py` cites for `service`: no version of this ticket has that section.

> **Ticket review — 2026-11-11, owner's decision.** Renumbered `data-repo_2-1` → `data-repo_2-6`: ranked behind every other ticket: the data workstream comes later (owner: everything on data will come later). Its relative order within the seven is unchanged. The owner's priorities for the week: the MOLONARI achievement (Friday 2026-11-13) and atCGS running (`LinkAtCGS`).

> **Ticket review — 2026-10-27, seventh pass (short ticket `gitRepo`).**
> Ranks unchanged, binding all seven `data-repo` tickets. `GitRepo` becomes
> the dependency (SrcLayout's `GitRepo/`, which imports nothing back). So
> DataSchema's `DataSpec` and `GitRepo.data` (WP-S1) land in `GitRepo/`, as
> pure data with no import from the rest of the package. DataBackendContract's
> `DataManager` (WP-B2) dispatches processes and stays outside `GitRepo/`,
> under `Tree/`. The data work is in pile 2 and SrcLayout before beta, so it
> lands in the new folders.

> **Ticket review — 2026-10-27, sixth pass (short ticket `minimalism`).**
> Ranks unchanged, for all seven `data-repo` tickets; this note binds them
> all. Two constraints come from the owner's short ticket. First, any command
> the data layer adds or changes needs a row and a verdict in Minimalism's
> map, and must land at the ring interface the map names. Second, the data
> layer calls no Git host's API: a DVC remote is a storage backend, not a
> provider API. A remote that needs a provider (a host's LFS or package
> registry) is gx4g's (ProviderMigration).

> **Ticket review — 2026-10-20, owner's decision.** Renumbered `data-repo_2-3` → `data-repo_2-1`: Omniscience moved to priority 1, and pile 2 was compacted to run 1..N (TICKETLIFECYCLE §2.1). Pile 1 is the Omniscience workstream, split into Omniscience and its six milestone tickets PushAnchor, OperatingSpaceId, InclusionProofs, OmniscienceRegister, OmniscienceAppend, OmniscienceQuery (owner's short ticket `update-omniscience`). Pile 2 order: the seven data-repo tickets, WorkingAreaRename, StateLocking, BranchProtection; order unchanged within each workstream.

> **Ticket review — 2026-10-08, owner's decision.** Renumbered `data-repo_2-1` → `data-repo_2-3`: each priority is one pile counted across branches (TICKETLIFECYCLE §2), which this backlog had numbered per branch. Pile 2 order: AutofixBlindSpot, PackageHygiene, the seven data-repo tickets, Omniscience, WorkingAreaRename, StateLocking; order unchanged within its workstream.

> **Ticket review — 2026-09-22.** The seven `data-repo` tickets renumbered
> from `2-3..2-9` to `2-1..2-7` — compacting a pre-existing gap, order
> unchanged — on the owner's request to reorganise the whole backlog as:
> finalize the agentic, then what's important before data-repo, then
> data-repo, then Omniscience. `data-repo` is that third bucket: real,
> analysed work (priority 2, stand-by) that nothing outside this
> workstream is waiting on yet, ranked as a block behind the `main`-branch
> items promoted ahead of it and ahead of
> [Omniscience](../archive/20261027_Omniscience_DevPlanTicket.md).

> **The umbrella ticket of the data workstream.** Analysed from the owner's
> short ticket
> `.dev/DevTickets/archive/.closedUserTicket/20260916_DevPlanTicket_DataManager_DVC.md`,
> which is the authoritative statement of what was asked for. This ticket
> holds the decision and the shape; six milestones hold the work.

## Abstract — read this first

**The one-line version.** ComplexGitSync learns to synchronise an
application's *data* across its tree the way it already synchronises its
code — through one CGS-owned `DataManager` that dispatches per repository,
with DVC as the first backend and Git LFS as a backend it must not block.

**What this document is.** The architecture and the milestone map for the
data workstream. Nothing here has been built.

**Why it exists.** A scientific project is code plus datasets, and CGS
today only knows about the code half. The owner's example is a
hydrological twin: a model repository, a forcing repository holding
hundreds of megabytes of SAFRAN and climate data, and a private parameter
repository. Cloning that tree gives you the code and a set of dangling
pointers. Freezing a release records commits that cannot be reconstituted.
The data is the part the science depends on, and it is the part CGS drops.

**What you will find.** §1 the decision. §2 the boundary — what CGS owns
and what a backend owns. §3 the six milestones and the order they land in.
§4 the decisions the owner must make. §5 what this architecture refuses to
do. §6 acceptance for the workstream as a whole.

**Who it is for.** Whoever picks up any milestone, and the owner, who
answers §4.

**What you need to do with it.** Read this before any milestone ticket.
Answer §4 before the first one starts, because D1 and D2 change what the
first milestone writes to disk.

```mermaid
graph TD
    CLI["cgitsync command"] --> ORCH["GitTree orchestrator<br/>scope, order, preflight, release"]
    ORCH --> A["GitRepo A<br/>Git only"]
    ORCH --> B["GitRepo B<br/>data_backend = dvc"]
    ORCH --> C["GitRepo C<br/>data_backend = git-lfs<br/><i>rejected, not implemented</i>"]
    B --> DM["DataManager<br/>CGS-owned dispatch<br/>YOU ARE HERE"]
    DM --> BE["DataBackend protocol"]
    BE --> DVC["DvcBackend<br/>DVC CLI, cache, remote"]
    BE --> LFS["GitLfsBackend<br/><i>future</i>"]

    classDef here fill:#1565C0,color:#fff,stroke:#111,stroke-width:2px;
    class DM here;
```

---

## 1. The decision

**CGS gains a native data-management layer.** The orchestrator dispatches
each relevant command per Git repository to its Git operation *and* to the
data-backend operations that repository needs. DVC is the first concrete
backend; the interface is backend-neutral from the start.

**`data` is a capability of a `GitRepo`, not a third kind of repository.**
The existing `project` / `private` classification and its write permissions
are untouched. A repository can be private *and* data-backed — the owner's
example has exactly that — and nothing about data changes who may write
where.

**Data authoring is part of CGS orchestration.** A user who runs
`cgitsync add`, `rm` or `commit` does not run DVC by hand for the supported
lifecycle. This is not the same as putting DVC's CLI under `cgitsync`:
pipelines, `repro`, experiments, remotes and garbage collection stay
outside.

## 2. The boundary

| CGS owns | The backend owns |
|---|---|
| Which repositories a command touches, and in what order | Content hashes |
| Path ownership: Git-owned source versus backend-owned data | Its cache and its metadata format |
| Preflight, refusal, and what a failure means | Remote transfers and credentials |
| Reporting, and what a release may advertise | Its own CLI semantics |

Two rules keep that line from eroding:

**One subprocess boundary.** Data backends run processes; the project
already has exactly one module allowed to (`git_runner.py`). Whatever the
milestones decide, they must not scatter `subprocess` calls into `cli/`,
the `.cgs` parser, or the domain model. Argument arrays, explicit
`cwd=repo.root`, no shell interpolation.

**No backend verbs in the CLI.** The existing commands are extended. There
is no `cgitsync data-add`. A capability that needs a new verb is a sign the
capability was modelled wrong.

One thing crosses into the memory workstream: **a backend must be able to
say which version of itself it is.** The memory system records the
toolchain of every entry it writes — cgitsync, git, pixi, and dvc or
git-lfs where they were used — so `DataBackend` grows a `version()` that
answers cheaply and says `none` when the tool is not installed.
[DataBackendContract](HT-BETA_2-11_DataBackendContract_DevPlanTicket.md) D6
owns the mechanism;
[OneRegister](../archive/20260916_OneRegister_DevPlanTicket.md) §3.1 owns what is
recorded.

## 3. The milestones, and the tickets that carry them

*Rewritten at the ticket review of 2026-11-27.* The six milestones M1–M6 stay the architecture. The tickets that
carry them are regrouped so that what can run together is in one ticket, and what HTBS needs comes first.

| Order | Ticket | Milestones | What lands | Needs |
|---|---|---|---|---|
| done | [DataSchema](HT-BETA_2-10_DataSchema_DevPlanTicket.md) | M1 | `data = { backend = "dvc" }` in `.cgs`, `DataSpec`, the `.gts` carrying it (8.14.1) | — |
| done | [DataBackendContract](HT-BETA_2-11_DataBackendContract_DevPlanTicket.md) | M2, WP-B2/B4/B6/B7 | `DataManager`, the protocol, the results, the fake backend, the client seam (8.14.2) | M1 |
| 1 | [DvcBackend](HT-BETA_1-3_DvcBackend_DevPlanTicket.md) | rest of M2, and DataServerAddress | the process boundary, `DvcBackend` registered, the `dvc` Pixi feature and CI job; `service = "<alias>"` and no address in clear | M2, MergeDataEncrypt |
| 2 | [DataRoundTrip](HT-BETA_1-4_DataRoundTrip_DevPlanTicket.md) | the HTBS slice of M3–M6 | `status` column, `push` publishes first, `bootstrap`/`initialise`/`pull`/restore materialise last, `release freeze` verifies; the real-DVC scenario | DvcBackend |
| 3 | [DataWorkspace](HT-BETA_2-7_DataWorkspace_DevPlanTicket.md) | rest of M3 and M4, in parallel | `add`/`rm`/`commit` routing, offline `checkout`, `merge`, `launch-release`, the destructive preflight | DataRoundTrip |
| 4 | [DataPublication](HT-BETA_2-8_DataPublication_DevPlanTicket.md) | rest of M5 | `tag` verification, revalidation, the retry path, `artefact:data` | DataWorkspace |
| 5 | [DataAcceptance](HT-BETA_2-9_DataAcceptance_DevPlanTicket.md) | rest of M6 | the private-repository scenario, the tutorial, the gate before `HT-BETA` merges into `CGS-ALPHA` | DataPublication |

**The branch.** Every ticket lands on `HT-BETA`, where M1 and M2 already are. The reason the workstream had a
branch of its own still holds: a half-built data layer must not stage a two-gigabyte NetCDF file into Git by
accident. Each ticket now carries that guarantee in its acceptance (a Git-only tree is unchanged byte for byte),
as `memory-dev`'s tickets did after that branch closed. `HT-BETA` is a working branch, not the mirror: nothing
reaches `main` before DataAcceptance's gate.

*The table before 2026-11-27, for history:* M1 DataSchema, M2 DataBackendContract, M3 DataAuthoring and M4
DataMaterialisation (parallel), M5 DataPublication, M6 DataAcceptance, each on `data-repo`.

## 4. Decisions — your call

### D1. Is `data_backend` the key, and is `"dvc"` its only value now?

The short ticket proposes `data_backend = "dvc"` on a repository entry,
with `"git-lfs"` reserved in the type contract but **rejected at parse
time** as not implemented. Recommendation: yes to both. Reserving the name
while refusing the value is what stops a user's `.cgs` from silently
behaving like plain Git. M1 cannot start until this is settled — it is the
key that goes into every `.cgs` and every `.gts` from then on.

### D2. Does `data_paths` stay a routing rule rather than a manifest?

`data_paths` says which *new, untracked* paths CGS may enroll in the
backend. It is not a list of datasets and it holds no hashes — DVC's own
metadata stays authoritative for what is tracked. Recommendation: keep it
exactly that narrow. The moment CGS keeps its own idea of which files are
data, it owns a second source of truth that will disagree with DVC's.

### D3. Is DVC optional at runtime?

**Settled by the short ticket (§3.1):** `DvcBackend` requires the `dvc`
executable; the CGS Pixi workspace SHOULD provide an optional `dvc` feature
carrying a tested version; DVC MUST NOT be in the mandatory runtime. A
Git-only project installs no DVC. Confirm the version pin (`>=3.67,<4`)
when M2 starts, since it will be months old by then.

### D4. Is a seven-ticket workstream the right size?

This is the second-largest thing in the pile after the memory workstream,
and the two now sit side by side at priority 2 with eleven tickets between
them. Two honest alternatives: cut M6 down to the round-trip test and drop
the documentation into M5, or defer M4's `merge` handling into a ticket of
its own. Recommendation: keep the six and re-rank the pile at the next
Ticket review rather than shrinking the analysis.

### D5. Where does the data workstream sit against memory?

Both are large, both are on their own branch, and both change what a `.gts`
must carry. M1 writes a new field into the snapshot; the memory
workstream's StateIdentity renames the state directory and redefines the
snapshot's content hash. **They must not be in flight at the same time
without one knowing about the other.** Recommendation: memory first, as
ranked today, and M1 reads StateIdentity before it touches `.gts`.
StateIdentity is archived; the hash work in flight is now
[GtsHashRepoPrecision](../archive/20261008_GtsHashRepoPrecision_DevPlanTicket.md),
and M1 reads that instead.

## 5. What this architecture refuses to do

* **Own a second repository hierarchy.** No `DataRepo`, no separate
  discovery, no second dispatcher.
* **Compute its own content hashes.** No CGS-owned DVC hashes, no
  object-level manifests in `.gts`, no `state(hash)_i` for data.
* **Store credentials.** Never in `.cgs`, `.gts`, `.cgitsync` or a log.
  Backend-native credential configuration only.
* **Install anything silently.** A selected DVC repository with no `dvc`
  executable is a precise per-repository error, never an auto-install.
* **Claim atomicity it cannot deliver.** Independent Git and object-store
  remotes give no cross-repository transaction. A partial publication is
  reported as one, in detail, with an idempotent retry.
* **Run pipelines.** No `dvc repro`, no experiments, no garbage collection,
  no data transformation.
* **Implement Git LFS.** The contract must accommodate it; this workstream
  must not enable it.

## 6. Acceptance for the workstream

The milestones carry their own criteria. The workstream is done when:

- A tree mixing Git-only, DVC-backed and private DVC-backed repositories is
  cloned, authored, published, frozen and restored by `cgitsync` alone,
  with no hand-run DVC command in the supported lifecycle.
- A Git-only project's behaviour is byte-for-byte what it is today, and its
  environment holds no `dvc`.
- The orchestration tests pass against a fake backend that never imports
  DVC — the proof that the orchestrator is not DVC-shaped.
- A release that cannot produce its data fails as not-ready rather than
  reporting success.
- `pixi run lint`, `pixi run test` and `pixi run check-ceilings` pass, and
  `data-repo` merges into `main`.
