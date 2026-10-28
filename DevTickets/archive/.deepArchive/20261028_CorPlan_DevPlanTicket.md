# CorPlan — Theoretical–Execution consistency of the Rust kernel

*Created: 2026-07-23*

*Branch: main*

> **Dropped — 2026-10-28, owner's decision.** The owner judged CorPlan not operational and rejected it. Nothing in it is to be implemented from here. What it planned was done or superseded elsewhere: Phases 4–7 (rows C11–C17) as TypedPipeline, archived 2026-10-28; C20 (the `Apache-2.0` licence) in 0.1.0; the CLI, `pixi run gx4g` and the `{NAME, NODE, EDGE, OP}` types as EnvConnect (E0, E2, E3). Rows C01–C10, C18 and C19 and Decisions D01–D03 and D08 are not taken up by any ticket; a new one is written from the book and the code, not from this text.

> **Ticket review — 2026-10-27, filed from the public root.** This plan sat at the root of the public gx4g repository as `CorPlanTicket.md`. It is moved here unchanged below this banner, because the public repository holds no tickets. It predates the 0.1.0 documentation (the LaTeX book, the tutorials, `GX4G.md`), which already settled part of its D01–D08 and replaced `getting-started.md` by `doc/` and tutorial 02. Its links to `gettingStarted.md` and the old `doc/CGS/*.md` and `doc/GX4G/*.md` ontologies no longer resolve: those files were folded into the LaTeX book in 0.1.0. Stand-by until the owner reviews which phases are still open; end of pile 2.

> **Reorganised — 2026-10-27, owner's answer to D6 of
> BeforeCgitsyncMerge.** Rows **C11–C17** (anchor before MEM, inking, FS,
> HASH(@), the public boundary, execution order, Gateway scope) and the
> phases that fix them, **Phases 4–7**, moved to the ticket TypedPipeline.
> They stay below, unchanged, as the source text that ticket was cut from;
> do not implement them from here. This ticket keeps C01–C10 and
> C18–C20; Phases 8–10 re-read TypedPipeline's order when they start.

---

# GX4G Correction Plan Ticket

## Theoretical-Execution Consistency

**Project:** GX4G Rust Kernel  
**Status:** Compatibility audit complete; correction work not started  
**Target guide:** `getting-started.md`  
**Audience:** one first-time user and two kernel developers  
**Language:** Rust stable, edition 2024  

---

## 1. Goal

Bring the Rust kernel, its tests, its public API, and its introductory
documentation into explicit agreement with the theoretical foundations of
PRIME G, CGS, and GX4G.

The final user-facing deliverable is one executable and
**Theoretical-Execution-consistent** guide:

```text
getting-started.md
```

The guide must describe the implementation that actually exists after this
ticket. It must not compensate for implementation gaps with theoretical claims.

---

## 2. Scope and source set

This audit treats the requested `GX4D` reference as `GX4G`, because the
repository contains GX4G foundations and no GX4D definition.

### Theoretical sources

- [`doc/CGS/CGS-0prime.md`](doc/CGS/CGS-0prime.md)
- [`doc/CGS/CGS-1ontology.md`](doc/CGS/CGS-1ontology.md)
- [`doc/CGS/CGS-2graph.md`](doc/CGS/CGS-2graph.md)
- [`doc/CGS/CGS-3axiomatic.md`](doc/CGS/CGS-3axiomatic.md)
- [`doc/GX4G/GX4G-0prime.md`](doc/GX4G/GX4G-0prime.md)
- [`doc/GX4G/GX4G-1ontology.md`](doc/GX4G/GX4G-1ontology.md)
- [`doc/GX4G/GX4G-2graph.md`](doc/GX4G/GX4G-2graph.md)
- [`doc/GX4G/GX4G-3axiomatic.md`](doc/GX4G/GX4G-3axiomatic.md)
- [`README.md`](../../../../../README.md)
- [`GX4G.md`](../../../../../GX4G.md)

### Execution sources

- `src/gateway.rs`
- `src/cgs.rs`
- `src/mem.rs`
- `src/fs.rs`
- `src/emit.rs`
- `src/lib.rs`
- `tests/*.rs`
- `examples/*.rs`
- [`gettingStarted.md`](gettingStarted.md)

### Proposed authority order

Conflicts must be resolved before implementation. Unless a decision record
states otherwise, use this order:

```text
AXIOMATIC
    ↓
ONTOLOGY
    ↓
PRIME
    ↓
GRAPH
    ↓
README / GX4G.md
    ↓
DEVELOPMENT TICKETS
    ↓
RUST IMPLEMENTATION
```

No lower source may silently redefine a higher source.

---

## 3. Baseline

At audit time:

- 34 runtime tests pass;
- 4 compile-fail emission tests pass;
- the crate builds as a library;
- the six development modules exist;
- SHA-256 output is deterministic for the current byte inputs.

This baseline proves conformance to `Rust-DevPlanTicket.md`. It does **not**
prove conformance to the complete theoretical foundation.

---

## 4. Compatibility verdict

```text
CURRENT STATUS := PARTIALLY COMPATIBLE

THEORETICAL-EXECUTION CONSISTENT := FALSE
```

### Compatible foundations

- The Gateway borrows CLIENT and SERVER instead of owning them.
- `LEFT` and `RIGHT` preserve endpoint identity.
- The current context derives `NABLA := LEFT.EDGE`.
- The current context derives `DELTA := RIGHT.NODE`.
- Phase values expose immutable references.
- Gateway, CGS, Memory, FileSystem, and Emit are separate modules.
- FileSystem hashing is deterministic and length-delimited.
- `Gateway::emit` accepts `ExecutionHash`, not STATE or SPACE.

### Compatibility matrix

| ID | Theoretical requirement | Current Rust state | Verdict | Required correction |
| --- | --- | --- | --- | --- |
| C01 | Every Graph is `G(NAME, NODE, EDGE, OP)` | CLIENT and SERVER are unconstrained user types | Missing | Introduce a PRIME G domain model and validate exactly four ordered constituents |
| C02 | Every constituent is itself a Graph | EDGE and NODE can be arbitrary Rust values | Missing | Encode Graph closure with traits/newtypes and sealed constructors |
| C03 | `Y.NAME = Y` | No NAME or self-identity exists | Missing | Add typed Graph identity and self-name validation |
| C04 | DAG and TANGLE precede specialization | No topology types exist | Missing | Add `Dag` and `Tangle` markers; type DELTA, NABLA, L0, and FS accordingly |
| C05 | CLIENT, GATEWAY, SERVER are PRIME G identities | Roles are generic type parameters only | Partial | Add role markers and prevent invalid role placement |
| C06 | Context binds DELTA, NABLA, and the canonical OP | Context contains only NABLA and DELTA | Incompatible | Add OP after resolving the canonical CGS signature |
| C07 | CGS checks PRIME G invariants | CGS checks only missing operands | Missing | Add PRIME validation before COMPUTO |
| C08 | CGS performs COMPUTO and emits a new DELTA.STATE@ | `State` is only a reference to the input DELTA | Incompatible | Implement an operator-driven state transformation producing a new valid Graph state |
| C09 | A valid result is deterministic, valid, and replicable | Only byte-hash determinism is tested | Partial | Define and test COMPUTO validity, replay, and proof equality |
| C10 | COMPUTO is anchored by exactly one L0(@) | No L0 or Anchor type exists | Missing/blocking | Add an L0 module and make anchoring mandatory |
| C11 | Time precedes Memory; no STATE is inked without @ | `persist(state, space)` is callable before any anchor | Direct violation | Make MEM accept only `AnchoredComputo` |
| C12 | MEM permanently inks anchored execution | `FileSystem` only holds borrowed in-memory references | Incompatible | Persist an owned canonical record through a backend |
| C13 | FS materializes persistent Graph relationships | `fs::write` computes a hash but writes no filesystem record | Incompatible | Separate materialization from hashing and verify durable round trips |
| C14 | HASH(@) identifies an anchor | Current hash contains STATE and SPACE, but no @ | Direct violation | Define the canonical anchored record and derive HASH(@) from it |
| C15 | Only HASH(@) crosses PUBLIC/PRIVATE | Private types and getters are exported at crate root | Partial | Reduce the public facade and add external-crate compile-fail tests |
| C16 | Execution order is immutable | Users manually call free functions in any order | Missing | Use typestate or one orchestrating `Gateway::execute` path |
| C17 | Gateway owns communication only | Gateway methods expose private context directly | Partial | Keep phase construction internal to the orchestrator |
| C18 | Native CLI is the PUBLIC Gateway materialization | No binary or CLI parser exists | Missing | Add a CLI matching the resolved four-identifier grammar |
| C19 | Same theory maps to one canonical guide | `gettingStarted.md` prints PRIVATE state and bypasses the intended user abstraction | Incompatible | Replace it with the audience-specific `getting-started.md` |
| C20 | Apache-2.0 is the declared license | Cargo uses `Apache2` | Metadata mismatch | Use the valid SPDX identifier `Apache-2.0` |

---

## 5. Theoretical contradictions that must be resolved first

Implementation must pause at this decision gate. The sources currently contain
semantically different contracts.

### D01 — Canonical CGS signature and order

`GX4G.md` and GX4G PRIME use:

```text
@CGS(NABLA, DELTA)
```

CGS Axiom 10 uses:

```text
@CGS(DELTA, NABLA, OP)
```

It also requires right-to-left interpretation.

**Decision required:** choose one canonical signature, ordering rule, and OP
source. Update every theoretical document and Mermaid graph to match it.

### D02 — Source of NABLA

GX4G derives:

```text
NABLA := LEFT.EDGE
```

The SERVER PRIME also declares:

```text
SERVER.EDGE : NABLA
```

**Decision required:** define whether NABLA belongs to the request CLIENT, the
SERVER environment, or is produced by `SYNC(SERVER, CLIENT)`.

### D03 — CLIENT execution

GX4G says:

```text
A Client never executes a Graph.
```

CGS ontology says:

```text
A CLIENT may execute DELTA.
```

**Decision required:** distinguish “may own/submit DELTA” from “may execute
DELTA,” or select one invariant.

### D04 — Unique anchor versus same-input hash

GX4G requires one unique `@` per COMPUTO and describes timestamp anchoring.
The current development tests require:

```text
same input → same HASH(@)
```

A unique timestamped execution normally changes HASH(@).

**Recommended resolution:**

```text
CONTENT_HASH := deterministic hash of canonical COMPUTO content

HASH(@) := hash of {
    anchor,
    content_hash,
    canonical ink record
}
```

The same content then has the same `CONTENT_HASH`, while distinct anchored
executions have distinct `HASH(@)`. Replay remains deterministic when the
recorded anchor is supplied.

### D05 — MEM, FS, and HASH order

The sources variously describe:

```text
L0 → MEM → HASH
```

```text
MEM → WRITE(FS) → HASH
```

and a MEM signature that already contains `HASH(@)`.

**Decision required:** freeze one order and define who owns canonical
serialization, durable materialization, and hash derivation.

### D06 — Meaning of persistence

The Rust Memory phase currently means “retain borrowed values in a struct.”
The theory uses “permanently inks” and “materializes in the FileSystem.”

**Decision required:** specify the minimum durability contract:

- atomic file write;
- append-only log;
- pluggable persistence trait with a filesystem reference backend;
- recovery and verification behavior.

### D07 — PUBLIC API boundary

The theoretical boundary can mean either:

1. only `GatewayOutput` is public to external crates; or
2. internal values are public Rust APIs but only `emit` models protocol
   publication.

**Recommended resolution:** select option 1. Expose a small public facade and
keep context, COMPUTO, STATE, SPACE, anchors, and ink records crate-private or
sealed.

### D08 — Canonical CLI grammar

CGS Axiom 3 defines four ordered identifiers:

```text
NAME NODE EDGE OP
```

README describes the CLI as the PUBLIC Gateway materialization, but no request
grammar or output contract is implemented.

**Decision required:** freeze argument semantics, validation errors, exit
codes, and the rule that stdout contains only HASH(@).

### Decision-gate deliverable

Create:

```text
doc/Theoretical-Execution-Contract.md
```

It must contain the accepted decisions D01–D08, one canonical execution
equation, and a glossary. No corrective Rust phase starts before this contract
is approved.

---

## 6. Target execution contract

Subject to D01–D08, the target pipeline is:

```text
CLI / CLIENT.EDGE.PUBLIC
    ↓
Gateway::listen
    ↓
SYNC / build validated PRIME execution context
    ↓
@CGS(DELTA, NABLA, OP)
    ↓
COMPUTO → new DELTA.STATE@
    ↓
L0 → exactly one Anchor(@)
    ↓
MEM → ink anchored execution
    ↓
FS → atomically materialize canonical record
    ↓
HASH(@) → prove anchored record
    ↓
Gateway::emit
    ↓
GatewayOutput { HASH(@) }
```

Only the first request and final proof belong to PUBLIC. Every intermediate
value belongs to PRIVATE.

### Target Rust mapping

| Theory | Target Rust concept |
| --- | --- |
| PRIME G | validated `Graph<Name, Node, Edge, Op>` or equivalent sealed trait |
| DAG / TANGLE | topology marker types |
| CLIENT / SERVER / GATEWAY | identity role markers |
| DELTA / NABLA | topology-checked Graph specializations |
| OP | explicit deterministic operator type |
| Execution context | validated private type containing the resolved CGS operands |
| COMPUTO | private operator result |
| STATE@ | new PRIME-conforming DELTA state |
| L0 | isolated anchoring module |
| @ | opaque, unique `Anchor` |
| MEM | accepts only anchored results |
| FS | persistence backend and canonical record |
| HASH(@) | immutable proof of the anchored canonical record |
| GATEWAY output | the only public execution result |

---

## 7. Sequential correction phases

Every phase ends with executable tests. No phase begins before the previous
phase and the theoretical contract pass.

### Phase 0 — Reconcile the foundation

**Owners:** Developer 1 + Developer 2  

Tasks:

- resolve D01–D08;
- correct contradictions across PRIME, ontology, graph, axiomatic, README, and
  `GX4G.md`;
- define the canonical vocabulary and equation;
- ensure every Mermaid diagram uses that same equation;
- record whether multiple DELTA/NABLA operands are current scope or future
  scope.

Tests:

- all internal Markdown links resolve;
- all Mermaid blocks parse;
- no conflicting CGS signatures remain;
- no conflicting MEM/FS/HASH order remains;
- the glossary defines PRIME G, DAG, TANGLE, OP, COMPUTO, STATE@, L0, @, MEM,
  FS, CONTENT_HASH, and HASH(@).

Deliverable:

```text
doc/Theoretical-Execution-Contract.md
```

### Phase 1 — PRIME G and topology types

**Owner:** Developer 1 — Graph/COMPUTO track  

Tasks:

- add the PRIME G representation;
- enforce four ordered constituents;
- enforce `Y.NAME = Y`;
- introduce DAG and TANGLE topology markers;
- introduce CLIENT, GATEWAY, and SERVER roles;
- specialize DELTA, NABLA, L0, and FS without weakening PRIME G.

Tests:

- valid PRIME G construction succeeds;
- missing or reordered constituents fail;
- an identity/name mismatch fails;
- DAG cannot be substituted for TANGLE where topology is fixed;
- invalid identity-role specialization fails at compile time where possible.

### Phase 2 — Gateway and validated execution context

**Owner:** Developer 1  

Tasks:

- make request and server Graphs PRIME-conforming;
- implement the resolved SYNC/NABLA rule;
- include DELTA, NABLA, and OP according to D01;
- prevent arbitrary construction of a valid execution context;
- introduce typestate or an internal orchestration token so `build_context`
  cannot precede `listen`.

Tests:

- LEFT and RIGHT remain immutable;
- PUBLIC request data cannot directly access SERVER PRIVATE state;
- every context operand maps to its normative Graph position;
- invalid PRIME Graphs are rejected;
- phase order violations fail to compile.

### Phase 3 — CGS COMPUTO

**Owner:** Developer 1  

Tasks:

- implement the resolved CGS signature and interpretation order;
- run PRIME G invariant checks;
- execute an explicit OP;
- produce a new PRIME-conforming DELTA.STATE@ rather than aliasing input DELTA;
- define deterministic replay and proof-of-equality behavior.

Tests:

- the same validated context and OP produce the same COMPUTO;
- changing DELTA, NABLA, or OP changes the appropriate result;
- invalid PRIME input produces VOID/error;
- output is a new valid DELTA state;
- CGS performs no communication, anchoring, persistence, or emission.

### Phase 4 — L0 anchoring

**Owner:** Developer 2 — Time/Memory/Public-boundary track  

Tasks:

- add `src/l0.rs`;
- define opaque `Anchor` and `AnchoredComputo`;
- inject an anchor provider/clock so tests remain reproducible;
- guarantee exactly one anchor per COMPUTO;
- prevent L0 from owning STATE or performing persistence.

Tests:

- every COMPUTO receives exactly one anchor;
- a second anchor operation on the same COMPUTO is impossible;
- deterministic fixture anchors reproduce exactly;
- distinct live executions receive distinct anchors;
- MEM rejects unanchored COMPUTO at compile time.

### Phase 5 — MEM inking and FS materialization

**Owner:** Developer 2  

Tasks:

- make MEM accept only `AnchoredComputo`;
- convert borrowed execution values into an owned canonical ink record;
- define a persistence backend trait;
- implement an atomic filesystem reference backend;
- separate MEM inking from FS materialization;
- support reload and validation of the materialized record.

Tests:

- no STATE is persisted without @;
- persisted data outlives CLIENT and SERVER values;
- write/read round trips preserve the canonical record;
- partial writes do not become valid records;
- MEM does not compute;
- FS does not anchor or emit.

### Phase 6 — CONTENT_HASH and HASH(@)

**Owner:** Developer 2  

Tasks:

- version the canonical encoding;
- include all theoretically required Graph constituents;
- implement the D04 distinction between content identity and execution proof;
- derive HASH(@) from the anchor and inked canonical record;
- add verification and corruption detection.

Tests:

- the same canonical COMPUTO produces the same CONTENT_HASH;
- the same anchored record produces the same HASH(@);
- distinct anchors produce distinct HASH(@);
- a changed NAME, NODE, EDGE, OP, STATE, or anchor changes the expected proof;
- ambiguous concatenation cannot collide through framing;
- corrupted persisted bytes fail verification.

### Phase 7 — Strict Gateway emission boundary

**Owner:** Developer 2  

Tasks:

- expose only request construction, execution, and `GatewayOutput` to first
  users;
- make all PRIVATE phase values crate-private or sealed;
- prevent construction of HASH(@) outside the verified hashing path;
- ensure `Gateway::emit` accepts only a verified HASH(@);
- prevent emission through formatting or alternate public functions.

Tests:

- external-crate compile-fail tests reject COMPUTO, STATE, SPACE, DELTA, NABLA,
  Anchor, ink records, and raw hashes;
- only verified HASH(@) constructs `GatewayOutput`;
- public rustdoc exposes no PRIVATE execution getter;
- Gateway owns no STATE, COMPUTO, DELTA, or persistence backend.

### Phase 8 — Native CLI

**Owner:** Developer 2  

Tasks:

- add a binary target;
- implement the resolved four-identifier grammar;
- route every request through the same Gateway orchestrator used by the library;
- print only HASH(@) to stdout;
- send diagnostics to stderr with stable non-zero exit codes;
- add a deterministic replay fixture for documentation.

Tests:

- a valid request emits one HASH(@) line;
- invalid arity and invalid Graphs fail without PRIVATE output;
- stdout never contains STATE, DELTA, NABLA, paths, or timestamps;
- CLI and library produce the same proof for the same recorded anchor;
- execution order is observed exactly once.

### Phase 9 — Full protocol integration

**Owners:** Developer 1 + Developer 2  

Tasks:

- test the entire canonical pipeline;
- instrument phase entry for test builds;
- test failure boundaries and recovery;
- audit module responsibility and public API visibility.

Tests:

```text
listen
    < build_context
    < CGS
    < L0
    < MEM
    < FS
    < HASH(@)
    < emit
```

- every phase executes exactly once;
- no phase can be skipped or reordered;
- failures prevent all later phases;
- replay of an anchored record is deterministic;
- only HASH(@) crosses PUBLIC;
- PRIVATE records remain recoverable and verifiable.

### Phase 10 — Produce `getting-started.md`

**Owners:** Developer 1 + Developer 2  

Replace the current camel-case guide with:

```text
getting-started.md
```

Do not keep two independently maintained getting-started guides. Either remove
`gettingStarted.md` after migration or replace it with a short compatibility
link.

The new guide is written only after Phases 0–9 pass.

---

## 8. Two-developer work contract

### Developer 1 — Graph and COMPUTO

Owns:

- PRIME G;
- topology and identity types;
- Gateway context construction;
- CGS validation and OP execution;
- DELTA.STATE@;
- theoretical mapping for Graph and COMPUTO.

Must not implement:

- clocks or anchors;
- persistence;
- hashing;
- public emission.

### Developer 2 — Time, Memory, proof, and interface

Owns:

- L0 and Anchor;
- MEM and persistence backend;
- FS materialization;
- canonical encoding and hashes;
- emission boundary;
- CLI and first-user execution path.

Must not implement:

- Graph computation;
- DELTA transformations;
- PRIME G validation rules.

### Shared frozen interfaces

Both developers agree on these contracts at Phase 0:

```text
ValidatedExecutionContext
    ↓
ComputoResult
    ↓
AnchoredComputo
    ↓
InkedExecution
    ↓
VerifiedExecutionHash
    ↓
GatewayOutput
```

Changes to a shared contract require:

- an updated theoretical decision;
- tests from both owning sides;
- review by the other developer.

---

## 9. Required structure of `getting-started.md`

### Track A — First-time user

The first screen must answer:

1. What is GX4G?
2. What enters PUBLIC?
3. What remains PRIVATE?
4. What is the single output?

Then provide a path that takes less than ten minutes:

```text
install
    ↓
build
    ↓
run one canonical CLI request
    ↓
receive HASH(@)
    ↓
verify or replay the proof
```

Requirements:

- no Rust source editing;
- no printing of STATE, SPACE, DELTA, NABLA, Anchor, or filesystem internals;
- one copy/paste command using the canonical four identifiers;
- one expected stdout line containing only HASH(@);
- a short explanation of deterministic content versus anchored execution;
- a rendered Mermaid diagram matching the actual Rust pipeline.

### Track B — Developer 1

Explain:

- PRIME G representation;
- DAG/TANGLE and role markers;
- context derivation;
- CGS signature, OP, validation, and DELTA.STATE@;
- tests owned by the Graph/COMPUTO track;
- compile-time invariants and extension rules.

Include one internal development example that does not claim to be PUBLIC API.

### Track C — Developer 2

Explain:

- L0 and anchor injection;
- anchored-only MEM;
- FS backend and canonical record;
- CONTENT_HASH versus HASH(@);
- verified emission;
- CLI boundary and tests.

Include one deterministic fixture workflow and one temporary-directory
persistence workflow.

### Shared guide sections

- authoritative theory links;
- theory-to-Rust mapping table;
- module responsibility table;
- canonical execution sequence;
- error and troubleshooting table;
- validation commands;
- “what is intentionally not public” section;
- contribution handoff between Developer 1 and Developer 2.

---

## 10. Documentation validation

All commands shown in `getting-started.md` must run from a clean checkout.

Required automated checks:

```bash
cargo fmt --check
cargo clippy --all-targets --all-features -- -D warnings
cargo test
cargo test --doc
cargo build --release
cargo run -- <canonical four identifiers>
```

Add a documentation smoke test that:

- executes every shell command marked as executable;
- validates the expected CLI stdout;
- checks local links;
- parses Mermaid blocks;
- fails when the guide references a missing module, command, or file.

Examples in the guide must use a fixed test anchor when exact output is shown.
Live clock output must never be presented as a stable literal.

---

## 11. Migration rules

- Treat the correction as an alpha API redesign; do not preserve an API that
  violates the theory.
- Record breaking changes in a migration section.
- Replace free-function sequencing with the canonical orchestrator.
- Do not call an in-memory borrowed struct “persistent.”
- Do not call a content-only hash `HASH(@)`.
- Do not expose PRIVATE values merely to make examples easy.
- Keep cryptographic encoding versioned and documented.
- Correct Cargo license metadata to `Apache-2.0`.
- Keep theoretical equations identical across all source documents.

---

## 12. Risks

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Theory remains contradictory | Code cannot be proven conformant | Phase 0 is a hard gate |
| Timestamp anchoring breaks deterministic examples | Unreproducible tests and docs | Inject and record anchors |
| Borrowed values are mistaken for persistence | Data disappears with endpoints | MEM creates an owned canonical record |
| Public Rust exports leak PRIVATE state | Violates core boundary | Facade plus external compile-fail tests |
| Hash meaning changes silently | Proof incompatibility | Version canonical encoding and distinguish hash types |
| Two developers duplicate responsibilities | Protocol overlap | Enforce ownership table and frozen handoff types |
| Guide is written before behavior exists | Documentation becomes speculative | Guide is Phase 10 only |

---

## 13. Final acceptance criteria

This correction ticket is complete only when:

- D01–D08 are resolved and reflected in every theoretical source;
- PRIME G closure, identity, topology, and specialization are encoded or
  explicitly justified where runtime validation is required;
- CGS accepts the canonical operands including OP;
- CGS produces a new valid DELTA.STATE@;
- every COMPUTO receives exactly one L0 anchor;
- MEM cannot accept unanchored execution;
- FS materializes an owned canonical record durably;
- HASH(@) proves the anchored record;
- execution phases cannot be skipped or reordered;
- external callers cannot obtain PRIVATE execution values;
- the native CLI emits only HASH(@);
- full integration and compile-fail tests pass;
- `getting-started.md` contains the first-user, Developer 1, and Developer 2
  tracks;
- every command in the guide is executable from a clean checkout;
- `gettingStarted.md` is removed or reduced to a redirect;
- formatting, linting, tests, docs, and release build all pass.

At that point:

```text
THEORETICAL FOUNDATION
    =
RUST TYPE SYSTEM
    =
EXECUTION ORDER
    =
PUBLIC DOCUMENTATION
```

and `getting-started.md` may be described as
**Theoretical-Execution-consistent**.
