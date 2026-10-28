# Rust — the GX4G kernel, six sequential phases

*Created: 2026-07-22*

*Branch: main*

> **Archived — 2026-10-27, owner.** The six phases are built: `src/gateway.rs`, `cgs.rs`, `mem.rs`, `fs.rs`, `emit.rs`, their tests in `tests/`, and `examples/phase5.rs`, `phase6.rs`. The owner closed the ticket in gx4g commit `fe2b6e4`. It predates the pair rule, so it carries no orchestrator's record.

---

# DevPlanTicket.md

# GX4G Rust Kernel

## Sequential Gateway Implementation

**Project:** @GX4G

**Language:** Rust (stable)

**Architecture:** Sequential deterministic pipelines

**Goal**

Implement the GX4G kernel exactly as specified by the ontology.

Each development phase must end with executable tests.

No phase starts before the previous one passes all tests.

---

# Global Invariants

The execution order is immutable.

```text
.listen

↓

build_context

↓

@CGS

↓

@MEM

↓

FS

↓

HASH(@)

↓

.emit
```

Only `HASH(@)` is allowed to leave the Gateway.

Every module owns exactly one responsibility.

Modules communicate only through immutable values.

---

# Phase 1 — Gateway

## Goal

Implement the communication boundary.

Files

```text
src/

    gateway.rs
```

Responsibilities

* receive a request
* expose `.listen()`
* create the execution context
* connect CLIENT and SERVER

Public API

```rust
Gateway::listen()

Gateway::build_context()
```

Expected result

```text
LEFT := CLIENT

RIGHT := SERVER
```

### Beginner Tests

* Gateway can be instantiated.
* `.listen()` returns success.
* `LEFT` points to CLIENT.
* `RIGHT` points to SERVER.
* No allocation leaks.
* `cargo test` passes.

Deliverable

```text
gateway.rs
gateway_tests.rs
```

---

# Phase 2 — Context Builder

## Goal

Build the execution operands.

Files

```text
src/

    gateway.rs
```

Responsibilities

Derive

```text
NABLA := LEFT.EDGE

DELTA := RIGHT.NODE
```

Expected result

```text
ExecutionContext {

    nabla,

    delta

}
```

### Beginner Tests

* Context builds successfully.
* NABLA equals CLIENT.EDGE.
* DELTA equals SERVER.NODE.
* Context is immutable.
* Invalid Graphs are rejected.
* `cargo test` passes.

Deliverable

```text
ExecutionContext
```

---

# Phase 3 — CGS Kernel

## Goal

Implement

```text
@CGS(
    NABLA,
    DELTA
)
```

Files

```text
src/

    cgs.rs
```

Responsibilities

Receive

```text
NABLA

DELTA
```

Produce

```text
STATE

SPACE
```

No persistence.

No FileSystem.

No hashing.

### Beginner Tests

* CGS accepts a valid context.
* CGS returns STATE.
* CGS returns SPACE.
* Returned values are immutable.
* Invalid inputs return an error.
* `cargo test` passes.

Deliverable

```text
State

Space
```

---

# Phase 4 — Memory

## Goal

Persist execution.

Files

```text
src/

    mem.rs
```

Responsibilities

Implement

```text
MEM(

    STATE,

    SPACE

)
```

Produce

```text
FS
```

### Beginner Tests

* Memory accepts STATE.
* Memory accepts SPACE.
* FileSystem object created.
* Nothing emitted publicly.
* `cargo test` passes.

Deliverable

```text
FileSystem
```

---

# Phase 5 — FileSystem

## Goal

Write execution.

Files

```text
src/

    fs.rs
```

Responsibilities

Implement

```text
WRITE(FS)
```

Produce

```text
HASH(@)
```

### Beginner Tests

* FileSystem writes successfully.
* Hash is deterministic.
* Same input → same HASH(@).
* Different input → different HASH(@).
* Hash remains immutable.
* `cargo test` passes.

Deliverable

```text
HASH(@)
```

---

# Phase 6 — Emit

## Goal

Publish the execution proof.

Files

```text
src/

    emit.rs
```

Responsibilities

Implement

```text
.emit(
    HASH(@)
)
```

Only

```text
HASH(@)
```

may leave the Gateway.

### Beginner Tests

* Emit accepts HASH(@).
* Emit rejects STATE.
* Emit rejects SPACE.
* Emit rejects DELTA.
* Emit rejects NABLA.
* Only HASH(@) is published.
* `cargo test` passes.

Deliverable

```text
Gateway Output
```

---

# Integration Tests

Execute the complete kernel.

```text
.listen

↓

build_context

↓

@CGS

↓

MEM

↓

WRITE

↓

HASH(@)

↓

.emit
```

### Beginner Tests

* Full execution succeeds.
* Every phase executes exactly once.
* Execution order is respected.
* Outputs are deterministic.
* No mutable data crosses module boundaries.
* Only HASH(@) is emitted.
* `cargo test` passes.

---

# Acceptance Criteria

The ticket is complete when:

* All six modules compile.
* All unit tests pass.
* All integration tests pass.
* The execution order is deterministic.
* No module owns more than one responsibility.
* No PUBLIC artifact other than `HASH(@)` is emitted.
* The kernel compiles cleanly with:

```bash
cargo fmt
cargo clippy -- -D warnings
cargo test
cargo build --release
```

At this stage, the GX4G Rust kernel constitutes the minimal executable implementation of the ontology.
