# RobustnessCrash — a killed command leaves a state the next one names or resumes

*Created: 2026-10-27*

*Branch: main*

> **Ticket review — 2026-10-27, sixth pass (short ticket `minimalism`).**
> Rank unchanged. There are two consequences. A killed command now also leaves
> the workspace lock behind (StateLocking, 7.3.0). The next writing command
> already names it as stale and points to `cgitsync unlock`, which D6–D9 count
> as "named". And D7's `memory reboot` gets a verdict in Minimalism's map
> before D7 is built. If the map withdraws the command, D7 goes with it.

> **From the owner's short ticket `robustness` (closed 2026-10-27 as
> [archive/.closedUserTicket/20261027_robustness.md](../archive/.closedUserTicket/20261027_robustness.md)).**
> The second half of its split, on the owner's decision of 2026-10-27: D6–D9,
> not mandatory before beta. It builds on Robustness, whose harness (D1),
> report contract (§3) and decisions (§2, Q1–Q7) it uses and does not
> restate.

## Abstract — read this first

**The one-line version.** A killed process, an interrupted `memory reboot` or
a remote that moves mid-run never leaves a silent or doubled history. Each
outcome is named by an existing finding, resumed, or refused with its shape
named.

**What this document is.** Steps D6–D9 of the original plan, with their part
of the Definition of Done.

**Why it exists.** Robustness makes an *error* honest. This ticket does the
same for a *crash*, which runs no `finally`, and for a race with a remote.

**What you need to do with it.** Start only after Robustness has landed, then
run D6–D9 in order.

```mermaid
graph LR
    R["Robustness<br/>harness + report"] --> D6["D6 crash windows<br/>kill mode"]
    D6 --> D7["D7 memory reboot<br/>resume or refuse"]
    D7 --> D8["D8 remote races"]
    D8 --> D9["D9 real trees<br/>YOU ARE HERE"]

    classDef here fill:#1565C0,color:#fff,stroke:#111,stroke-width:2px;
    class D9 here;
```

---

## 1. Steps

Robustness's P-numbers (P6, P10, P11) and §3 are cited, not repeated.

**D6 — ADD crash-window tests** (`kill` mode), one per window. Each states its
observable outcome explicitly: an existing `Finding` when Memory is
inconsistent; otherwise `verify` clean **plus** the expected live-tree
condition.

| Window | Expected after kill | Retry |
|---|---|---|
| repo mutation done, before State write | `verify` clean (Memory is consistent); live tree ahead of the last State, visible in `status` | records the new State |
| State renamed, before ledger write | `ORPHAN_STATE` | same State file name (no duplicate), one new entry, finding gone |
| ledger linked, before `HEAD` update | `HEAD_STALE` | `verify repair` recomputes `HEAD`; chain intact |
| during State temp write, before `replace` | `verify` clean; at most a `.…gts.tmp` (P6), invisible to `state_files()` | retry writes the State; the stray file is never read |
| after local fold, before memory push | local memory ahead of its remote; no remote success reported | `memory push` publishes once |

**D7 — CHANGE `memory reboot` to resume or diagnose an interruption (P11).**
Kill tests at each of the four Git mutations in P11 first; then make each
resulting shape recognisable at the start of the next `memory reboot`:

| Interrupted after | Remote | Local | Required behaviour |
|---|---|---|---|
| `push_ref_as` | current + archived | current | resume: delete remote current, continue |
| `delete_remote_branch` | archived only | current (upstream gone) | resume from rename |
| `rename_branch` | archived only | archived only | resume from orphan creation |
| orphan created, genesis not pushed | archived only | new orphan | resume: write genesis, push |

Anything not matching one of these shapes is refused with the observed
shape named. A finished reboot leaves exactly one genesis on origin; two
competing geneses are impossible by construction (each resume step is
idempotent on the named branch).

**D8 — ADD remote-race tests** with local bare repositories:
remote advances after preflight and before push → that repository is the
`failed` outcome (non-fast-forward), nothing forced; memory remote advances
between fold and memory push → memory push refuses, project push unaffected
(P10); a repository disappears after preflight → `failed`, the rest
`not_attempted`.

**D9 — Real-tree validation** (manual, disposable workspaces only):
`examples/molonari-light.cgs` and `examples/cawaqs.cgs` — bootstrap, add
local-only work in one child, confirm `pull --force` refuses or preserves it,
make one remote diverge, confirm no overwrite, synchronise normally, `verify`
clean, compare commits and State digests with a fresh bootstrap.

---

## 2. Definition of Done

1. Every D6 crash window has an explicitly specified observable outcome — an existing `Finding` when Memory is inconsistent, otherwise clean `verify` plus the expected live-tree/`status` condition — proven in `kill` mode.
2. An interrupted `memory reboot` is resumed or refused with its shape named; never two geneses.
3. No remote race leads to a forced or silent overwrite.
4. MOLONARI-light and CaWaQS pass D9.
