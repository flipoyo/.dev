# BeforeBeta — everything mandatory before beta, landed on main and checked by a user install

*Created: 2026-10-27*

*Branch: main*

> **Ticket review — 2026-10-27, owner's decision.** Filed at `main_1-1`.
> The owner wants it run before the frontier between cgitsync and gx4g is
> finalised (EnvConnect's deferred C1 and C6, and GX4G's E5). The owner's
> order: *"test checkout memory-dev, merge main. Implement WorkingAreRename.
> checkout main, merge memory-dev. main holds install.cgs --> cgitsync
> initialise $CGSHOME install.cgs. Check with the utmost attention .memory, and
> reports defects as well as .omniscience."* WorkingAreaRename's D1 (rename,
> or prose only) **closes on the orchestrator's demand**.
>
> **Second pass, the same day:** *"concentrate main-openTickets as much as
> mandatory in BeforeBeta. Evaluate if shortTickets should be integrated
> too."* Pile 1 is now exactly what is mandatory before beta, and this ticket
> runs all of it:
> - **Omniscience** is closed by checking its §10 on the real trees.
> - **StateLocking** is mandatory because its trigger has fired: gx4g runs
>   `cgitsync` in a developer's tree.
> - **Robustness** (Phase 0 and D1–D5) comes from the short ticket
>   `robustness`, split on the owner's word. D6–D9 are RobustnessCrash, in
>   pile 2.
> - **BranchProtection** is mandatory on the owner's word: no random user
>   deletes a branch in the beta.
>
> `pixi-global-install` stays on stand-by (owner): the beta's user route is
> clone + `pixi run`. `deletion4devOnly` closes with BranchProtection.
>
> **Correction, the same day (owner):** *"Le DevPlan Before Beta est
> incoherent il faut mettre à niveau la branch memory-dev de main en
> premier."* `memory-dev` is brought up to `main` **before** the tree is put
> on it. Checking it out first would install its 5.0.0 build, and the merge
> would then run under that build in a tree whose memory 7.0.0 wrote. S1 is
> now `cgitsync merge main --into memory-dev`. It runs under 7.0.0, and the
> merge is a fast-forward, so the tree lands on `memory-dev` already at
> `main`. S3 follows the same rule the other way: `main` is brought up to
> `memory-dev` with `cgitsync merge memory-dev --into main`, run from
> `memory-dev`, under its newer build.
>
> **Third pass, the same day (owner):** *"à ce niveau d'écart on rapatrie le
> ticket sur main, et on close la branch memory-dev."* `memory-dev` was 30
> commits behind `main` and none ahead. WorkingAreaRename moves to `main_1-3`,
> and `memory-dev` is closed. **The `memory-dev` cycle is gone from this
> ticket:** every step lands on `main`, and the two corrections above apply to
> nothing any more. They are kept as history. Closing the branch is now S1.
> On 2026-10-27, `branch check memory-dev` found only `.memory` holding commits
> of its own: 2 ledger entries and 2 States, which `branch close` keeps on
> `ancestors`. `branch close` itself was **refused, and nothing was renamed**,
> because the memory's ledger does not verify (§3, defect 3). S1 waits on
> D4.
>
> **Fourth pass, the same day (owner):** D4 answered (b), *"b option ticket
> de code verify"*. CommitLogLoss is filed at `main_1-2` and runs as **S0**,
> before S1. The rest of pile 1 moves down one rank: Omniscience `1-3`,
> WorkingAreaRename `1-4`, StateLocking `1-5`, Robustness `1-6`,
> BranchProtection `1-7`.
>
> **Fifth pass, the same day (owner):** *"Ticket review integrates
> shortTicket minimalism and modify DevPlanTickets subsequently. It adds
> constraints to the overall BeforeBeta requirements."* S0–S3 have landed
> (7.1.0, 7.1.1 for Omniscience, 7.2.0, 7.3.0), so pile 1 is compacted:
> Robustness `1-2`, then three new tickets from `minimalism`. The owner's
> answers through `AskUserQuestion`:
> - **Provider APIs.** Every call to a provider's API, read or write, is
>   gx4g's. Before beta no new one enters `cgitsync`, and the existing ones
>   wait for gx4g (ProviderMigration, `2-10`).
> - **BranchProtection is split.** That answers D3 below.
> - **The whole short ticket is before beta,** except the migration.
> - **"Disclosed" means withdrawn from the CLI.**
>
> The new order is S4 Robustness, S5 Minimalism (the map), S6 MerkleRoot,
> S7 CliReduction and S8 BranchProtection (its M5 only), then S9 the user
> install and S10 the inspection, which were S6 and S7. §2.5 is the
> constraint the short ticket puts on every step.

## Abstract — read this first

**The one-line version.** This ticket is a beta rehearsal on the real
developer tree. It closes `memory-dev`, lands the mandatory work on `main` (a
memory-format change among it), and makes a fresh user install from `main`. Then it hunts for defects in `.memory` and `.omniscience`. It
reports what it finds; the only code it changes is through the tickets it
runs.

**What this document is.** The order of eleven steps, S0 to S10 (§1), what
to watch in each and the constraints that bind them all (§2), the defects
found (§3), the decisions (§4) and when it is done (§5). Each ticket it runs keeps its own plan and its own worker/orchestrator
pair: this ticket is the order, not the content.

**Why now.** gx4g drives `cgitsync` from another process and builds on rules
that have never run end to end on a real tree:
- the tree-wide merge that keeps the target's memory whole;
- the private branch rule (`ComplexGitSync_memory-dev`);
- the 7.0.0 install frontier and twin memories;
- the USER tree's local-only memory;
- the Omniscience register.

It also relies on things being built here. The workspace lock landed in
7.3.0 (S3). Still to come are an honest partial-failure report (S4), and a
minimal CLI that sits at the ring interfaces, with every State hash behind
one class that never hands its tree out (S5–S7). Last, a branch a USER tree
cannot remove through `cgitsync`, and a dying branch reported to the
register (S8). The provider's lock and roles are gx4g's (BranchProtection
§9). All of these must hold before gx4g's frontier is closed, and the
frontier is drawn on Minimalism's map.

**What you need to do with it.** Answer D2 (§4). D3 was answered on
2026-10-27. Then run §1 in order, filling §3 as you go, under §2.5.

```mermaid
graph TD
    S0["S0 CommitLogLoss<br/>(done, 7.1.0)"] --> S1["S1 close memory-dev<br/>(done)"]
    S1 --> S2["S2 WorkingAreaRename<br/>(done, 7.2.0)"]
    S2 --> S3["S3 StateLocking<br/>(done, 7.3.0)"]
    S3 --> S4["S4 Robustness<br/>(main_1-2)"]
    S4 --> S5["S5 Minimalism: the map<br/>(main_1-3)"]
    S5 --> S6["S6 MerkleRoot<br/>(main_1-4)"]
    S6 --> S7["S7 CliReduction<br/>(main_1-5)"]
    S7 --> S8["S8 BranchProtection, M5<br/>(main_1-6)"]
    S8 --> S9["S9 user install<br/>initialise install.cgs"]
    S9 --> S10["S10 inspect .memory, .omniscience<br/>Omniscience §10 (archived 7.1.1)"]
    S10 --> R["§3 defects<br/>YOU ARE HERE"]

    classDef here fill:#1565C0,color:#fff,stroke:#111,stroke-width:2px;
    class R here;
```

---

## 1. The script

Run it in the developer tree (`examples/complexgitsync4dev.cgs`, NESTED,
DEV), from its root, unless a step says otherwise. Each `implement` is the
ordinary worker/orchestrator pair, with its own release and its own record.
Facts as of 2026-10-27:

| Step | What | Facts going in |
|---|---|---|
| **S0** | `implement CommitLogLoss`, on `main` | **Done 2026-10-27, 7.1.0**, archived. Defect 3's cause, answered by D4 (b). |
| **S1** | `cgitsync branch close memory-dev`, after S0. **Done by the owner, 2026-10-27 03:01, under 7.1.0**: `closed/memory-dev` or `closed/ComplexGitSync_memory-dev` in all seven repositories, `.memory`'s two own commits on `ComplexGitSync_ancestors`. | `branch check` finds every repository `safe` except `.memory`, whose `ComplexGitSync_memory-dev` alone holds 2 ledger entries and 2 States; the close keeps them on `ancestors`. Refused on 2026-10-27 because the ledger does not verify (defect 3). It runs once S0 has landed. |
| **S2** | `implement WorkingAreaRename`, on `main` | **Done 2026-10-27, 7.2.0**, archived. D1: prose only, nothing renamed; `memory status` prints `folded=` and `pending=`. |
| **S3** | `implement StateLocking`, on `main` | **Done 2026-10-27, 7.3.0**, archived. `.cgitsync/.lock`, taken by every writing client method; `cgitsync unlock`. |
| **S4** | `implement Robustness`, on `main`: Phase 0 first, then D1–D5 | Phase 0's premise table (P1–P15) is re-checked against `HEAD`. Its deviations are also defects for §3. Adds no command (§2.5). |
| **S5** | `implement Minimalism`, on `main`: the map | No change to `src/` beyond a map script. It covers 27 commands, 66 leaf commands, 115 public client methods, the provider calls, the Merkle surface and the ring-interface checks. It ends with the verdict per command (its D1) and D2–D5. |
| **S6** | `implement MerkleRoot`, on `main` | Scope is fixed by Minimalism D3 and D4. Every golden vector, State name, `os_id` and `H_GLOBAL` stays byte for byte. |
| **S7** | `implement CliReduction`, on `main` | Carries out Minimalism D1. The tutorials and the user guide shrink with the CLI. Provider commands wait for ProviderMigration. |
| **S8** | `implement BranchProtection`, on `main`: M5 only, after its D7–D10 | Split on 2026-10-27. `require_dev` is kept, and M5 reports a dead GitTree-branch to the register. M0–M4 (provider protection and roles) are §9, handed to gx4g. No provider call. |
| **S9** | The user install from `main`: `git clone github:flipoyo/ComplexGitSync $CGSPATH/ComplexGitSync`, then in it `pixi run cgitsync initialise install.cgs --output-path $CGSPATH` | `initialise` takes one source, plus `--output-path`, which is CGSPATH. CGSHOME is `CGSPATH/ComplexGitSync`, so the owner's `initialise $CGSHOME install.cgs` is spelled this way. `install.cgs` mounts the tool and `docs` only, so the tree is USER: its memory is local and never pushed. |
| **S10** | The inspection in §2, in both trees, with the CLI S7 left | — |

## 2. What to watch, with the utmost attention

### 2.1 One branch, one build

With `memory-dev` closed, every step runs on `main` under the build it has
just landed; no step changes the tree's branch. Record `cgitsync --version`
for every command anyway. A ticket's release that changes behaviour shows up
as a new version between two steps, not as an older build left in the tree.

### 2.2 `.memory`, in the developer tree

- **Baseline, before S1.** `verify check` already says `corrupt`, with 27
  `COMMIT_LOG_MISMATCH` findings (§3, defect 1).
  - S10 checks that no new finding appears.
  - It also checks whether the rows 6.8.1 recorded as lost explain all 27.
- **The close (S1).**
  - `.memory`'s 2 own commits are on `ancestors`, recorded in the ledger,
    before any rename.
  - `closed/memory-dev` exists in every repository that had the branch,
    the private ones included, and nothing else moves.
  - The memory stays on `ComplexGitSync`: the tree is NESTED, so not a twin,
    and no `ComplexGitSync_ComplexGitSync` appears.
  - `.self-history` follows its memory's branch.
- **Integrity.**
  - The ledger chain gains no break.
  - Every State written before S2 still opens under its own name and still
    verifies.
  - `release load <State hash>` finds a State that only the memory holds.
- **Rename: none.** WorkingAreaRename's D1 said prose only. `memory status`
  splits the chain into `folded` and `pending`, and their sum is `entries`.
- **C8 ambiguity.** `ComplexGitSync_memory-dev`, and its closed name, is
  read as "ComplexGitSync, branch `memory-dev`", never as "twin of a
  project called `memory-dev`".
- **StateLocking, live.** Start two write commands at once in the developer
  tree.
  - One refuses before touching anything, and the read-only commands still
    run.
  - No ledger append is lost quietly.
  - The lock file is never folded into, committed to or pushed with the
    memory.
- **Robustness, live.** Make one repository's push fail mid-tree.
  - The report names what completed, what failed and what was not
    attempted.
  - Neither the memory nor the ledger claims the push.
  - The retry converges.
- **Status.** `cgitsync status` shows `errors=0` after every step.

### 2.3 `.memory` and branches, in the user tree (S9)

- The tree is USER, and its memory is created locally, never declared.
- Nothing is pushed, even when a remote is added by hand.
- No DEV prompt appears: neither `memory setup` nor EnvConnect C7's report.
- `initialise <a .gts>` is refused by name.
- **BranchProtection, as split:**
  - the user cannot close or delete a branch through `cgitsync`, and the
    refusal says why (`require_dev`);
  - through plain Git, the branch is protected only once gx4g has locked it
    on the provider (BranchProtection §9). Until then, a deletion is
    reported by `omniscience observe` as `vanished` (M5). S10 records which
    of the two it found.
- `status` shows `errors=0`.

### 2.4 `.omniscience`, and Omniscience §10

Neither tree mounts it today: the developer `.cgs` has no `.omniscience`
entry. Mount the register in a disposable DEV workspace, as tutorial 8 does.
Then:

- **USER tree.** `omniscience mount`, `register` and `observe` are refused
  by name before anything is touched.
- **DEV tree.** Every query (`get`, `branches`, `history`, `state`, `proof`,
  `verify`, `status`, `report`, `memory`) answers with one of the five
  statuses. None writes anything, and none turns a failed read into
  "deleted".
- **Omniscience §10.** Each of its eleven items gets a row in §3, either a
  defect or "holds". Omniscience itself was proved and archived on
  2026-10-27 against 7.1.0 (its §11); S10 reruns the same checks, after
  MerkleRoot (S6) moved every hash, so they also prove nothing moved.
- **MerkleRoot (S6).** A State's name and `os_id` are unchanged, so every
  registered record still verifies, and `omniscience proof` answers as
  Minimalism D3 decided.
- **BranchProtection.** Protecting the register's branch on the provider is
  gx4g's (§9). OmniscienceQuery keeps reporting that protection as "not
  checked", and that is not a defect. M5's findings appear in
  `omniscience status` and `report`.

### 2.5 The constraints `minimalism` puts on every step

They bind from the ticket review of 2026-10-27 on (owner). Each step's
orchestrator quotes against them, and a breach is a defect in §3.

1. **No new command or public client method** lands without a row and a
   verdict in Minimalism's map. Before S5 exists, no step adds one: S4 adds
   none by its own §6.
2. **No new call to a provider's API**, read or write. The existing calls
   (`repo create`, `memory setup`'s create step, the sign-in probe of
   `env show` and of every Environment record) are listed for
   ProviderMigration and stay until gx4g offers each one.
3. **The Merkle tree is never materialised.** No step adds code that walks,
   stores or hands out inner nodes outside the hashing modules. From S6 on,
   that means outside `MerkleRoot`.
4. **The CLI the beta ships is the reduced one.** S9 and S10, the tutorials
   and the user guide all run against the CLI that S7 left.
5. **The frontier with gx4g is drawn on the map.** What `cgitsync` hands to
   gx4g is listed in two places, ProviderMigration and BranchProtection §9.
   Nothing else crosses without a row in the map.

## 3. Defects found

One row per defect, filled in during the run. A defect is reported, not
fixed here, unless the ticket a step runs owns it (§5).

| # | Step | Command and build | Observed | Expected | Severity |
|---|---|---|---|---|---|
| 1 | before S1 | `cgitsync verify check`, 7.0.0 | `status=corrupt`: 27 `COMMIT_LOG_MISMATCH` (seq 3–55, odd entries), "entry records a commit log whose rows are gone" | `ok`, or every finding explained as the loss recorded in 6.8.1 | fixed by S0: a recorded loss, `incomplete` |
| 2 | known | Robustness P2 and P3 | A failed `push` reports one error and loses what completed; a `tag` retry can never converge | §3 of Robustness | fixed by S4 |
| 3 | S1 | `cgitsync branch close memory-dev`, 7.0.0 | Refused, nothing renamed: "the ledger does not verify (seq=3 COMMIT_LOG_MISMATCH; …)". `verify repair` heals only a stale HEAD, never a chain, and 6.8.1 said the lost rows are not recovered. So this memory can never verify again, and every `branch close` and `branch delete` in this tree is refused for good. | A loss already recorded as unrecoverable does not refuse forever; a documented way through exists | fixed by S0 (CommitLogLoss, 7.1.0): `verify check` now says `incomplete`, 27 `COMMIT_LOG_LOST` |
| 4 | S1 | `cgitsync branch close memory-dev`, 7.0.0, refused at 01:35 | Before refusing, it had already kept `ComplexGitSync_memory-dev` on `ComplexGitSync_ancestors` and pushed it (`99c6515`), written a State and ledger entry 69 (`branch_close_keep`). Only then did `_assert_history_holds` run. Its message, "nothing was renamed or deleted", is true but says nothing of the push and the record. | A history already corrupt before the command is refused before anything moves; a refusal after a step says which steps ran | to report (D2); the S1 close itself was then run by the owner at 03:01, under 7.1.0, and succeeded |

## 4. Decisions for the owner

| D | Question | Recommendation |
|---|---|---|
| **D1** | Withdrawn on 2026-10-27, third pass: with `memory-dev` closed, no step changes the tree's branch. | — |
| **D2** | Where each defect goes once it is reported. | **One short ticket each, in `shortTickets/`**, ranked by the next ticket review, unless a ticket this one runs owns it. |
| **D3** | BranchProtection: whose job is it? EnvConnect §5 gives GitRepo rights on a host to gx4g, through the providers' APIs. | **Answered 2026-10-27, through the short ticket `minimalism` (owner): split the other way.** Every provider API call is gx4g's, so the provider's protection and the roles go to gx4g (BranchProtection §9). `cgitsync` keeps `require_dev` and M5. The first recommendation, which had `cgitsync` keep the provider's protection, is overturned. |

| D | Question | Options |
|---|---|---|
| **D4** | Defect 3: how is `memory-dev` closed, given a ledger that can never verify? | **Answered (b), owner 2026-10-27:** a code ticket, CommitLogLoss, run as S0. `memory reboot` (a) and waiting (c) were not chosen. |

WorkingAreaRename's D1 is not asked here: it closes on its orchestrator's
demand (owner, 2026-10-27).

## 5. Done when, and what this refuses

**Done when:**
- S0 to S9 have run, and S10's inspection has its rows.
- CommitLogLoss, WorkingAreaRename, StateLocking, Robustness, Minimalism,
  MerkleRoot, CliReduction and BranchProtection are each archived with their
  own orchestrator's record.
- Every step was quoted against §2.5.
- ProviderMigration and BranchProtection §9 are handed to gx4g as its
  requirements. They are not done here: ProviderMigration stays in pile 2
  until gx4g offers each call.
- Every check in §2, and each of Omniscience §10's eleven items, has a row in
  §3, even if the row says "holds".
- Both trees show `cgitsync status` with `errors=0`, or the row in §3 that
  says why not.
- BeforeBeta is archived with its orchestrator's record. Omniscience was
  archived on its own record on 2026-10-27. Pile 1 is then empty, and the
  frontier with gx4g can be finalised.

**Refuses:**
- **To fix anything outside the tickets it runs.** Every other defect is
  reported (D2).
- **To rewrite history.** No reset, rebase or force-push to recover a step
  that went wrong: a failed step is a finding.
- **To push without the owner's word.**
