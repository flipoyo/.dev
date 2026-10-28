# RustGuide — GX4G's architecture and the Rust ideas under it, in ten diagrams

*Created: 2026-10-27*

## Abstract — read this first

**What this document is.** Ten Mermaid diagrams that explain how GX4G is
built and the Rust ideas it rests on, for someone who does not write Rust.
Each diagram has one sentence saying what to look at. The running example is
the code that exists (`Gateway`, `ExecutionContext`, `CgsError`,
`ExecutionHash`, `GitProvider`), so nothing here is invented for teaching.

**Why it exists.** The owner asked for clear diagrams of the architecture and
of the Rust concepts under it (BeforeCgitsyncMerge, short ticket
`security-robustness`). This file holds all ten. The seven that explain the
*public* architecture are redrawn in TikZ as a chapter of the book
(`doc/Text/rust_guide.tex`). The three that show the threat model stay here,
in the private `.dev`, until the owner says otherwise.

**What you will find.** Diagrams 1 to 6 explain the code and the Rust ideas.
Diagram 7 shows why a proof cannot be forged. Diagram 8 shows where a secret
lives. Diagram 9 shows the test layers. Diagram 10 follows one request.
Last, a short glossary.

**Who it is for.** The owner, and anyone new to Rust joining the project.

**What you need to do with it.** Read the diagrams in order. This file
explains and links. It does not state rules: the rules are in
[AdditionalSpecs.md](../.localSpec/AdditionalSpecs.md), and when the two
disagree, that file is right.

```mermaid
graph LR
    A["1 modules<br/>2 pipeline"] --> B["3 borrowing<br/>4 traits<br/>5 Result"]
    B --> C["6 class and interface"]
    C --> D["7 forged proof<br/>8 trust boundary"]
    D --> E["9 tests<br/>10 one request"]

    classDef here fill:#1565C0,color:#fff,stroke:#111,stroke-width:2px;
    class A here;
```

---

## 1. The module map

*Look at the two boxes: everything on the left is hidden, and only the
names on the right can be used by someone else.*

Rust code is split into **modules**. A module's contents are private unless
marked `pub`. `lib.rs` is the front door: it lists, with `pub use`, the few
names it hands out.

```mermaid
graph LR
    subgraph PRIVATE["private modules: nobody outside can reach inside"]
        gateway["gateway.rs<br/>Gateway, the context"]
        cgs["cgs.rs<br/>State, Space"]
        l0["l0.rs<br/>the moment, the anchor"]
        mem["mem.rs<br/>the ink record"]
        fs["fs.rs<br/>the store, the log"]
        hash["hash.rs<br/>ExecutionHash<br/>all the hashing"]
        emit["emit.rs<br/>GatewayOutput"]
        edge["provider.rs · repo.rs<br/>identity.rs · ring.rs<br/>secret.rs · g.rs"]
    end
    subgraph PUBLIC["lib.rs: the public surface"]
        names["G · ExecutionHash · GatewayOutput<br/>Store · FileStore · MemoryStore<br/>SystemClock · FixedAnchor · Moment<br/>GitProvider · Offline · GitRepo<br/>Ring · Access · Secret · CanonicalBytes"]
    end
    gateway -->|"only ClientGraph,<br/>ServerGraph, ContextError"| names
    cgs -->|"only CgsError"| names
    l0 --> names
    fs --> names
    hash --> names
    emit --> names
    edge --> names
    mem -.->|"nothing"| names
```

The phase functions, and every type that passes between the phases, are on
the private side and are **not** in the list on the right. `mem.rs` exports
nothing at all. That is the whole security idea of the kernel, and diagram 7
shows why.

## 2. The path, and what passes along it

*Look at the labels on the arrows: each step receives one value and hands on
one value, and only the last one leaves.*

```mermaid
graph LR
    CL["CLIENT<br/>owns EDGE"] --> L
    SV["SERVER<br/>owns NODE"] --> L
    L[".listen<br/>build_context"] -->|"ExecutionContext<br/>borrowed"| CG["@CGS<br/>compute"]
    CG -->|"State + Space<br/>borrowed"| L0["L0<br/>stamp a moment"]
    L0 -->|"AnchoredComputo<br/>borrowed + moment"| ME["MEM<br/>ink"]
    ME -->|"InkRecord<br/>OWNED bytes"| FS["FS<br/>commit to the log"]
    FS -->|"Written<br/>stored, read back"| HA["HASH(@)<br/>derived last"]
    HA -->|"ExecutionHash<br/>32 bytes, copied"| EM[".emit"]
    EM -->|"GatewayOutput<br/>the only public value"| OUT(("outside"))

    classDef pub fill:#1565C0,color:#fff,stroke:#111,stroke-width:2px;
    class OUT pub;
```

`G::execute` runs all of them in this one order and stops at the first
failure. Nothing else can run a step. Until MEM, every value *borrows* from
the caller's CLIENT and SERVER; MEM is where the bytes are *copied* into a
record the gate owns, which is why the record can be written to disk and
outlive the request.

## 3. Ownership and borrowing

*Look at the dotted arrows: the Gateway and the context point at the client
and the server, they do not hold copies. Look at the solid box: the record is
the first thing that owns its bytes.*

In Rust, every value has one **owner**. Code can instead **borrow** a value:
it gets a reference (`&`) and may look but not keep. The mark `'a` is a
**lifetime**: a promise that the reference does not outlive what it points to.

```mermaid
graph TD
    C["client: Client<br/>(owned by the caller)"]
    S["server: Server<br/>(owned by the caller)"]
    G["Gateway&lt;'a, Client, Server&gt;<br/>left: &'a Client<br/>right: &'a Server"]
    X["ExecutionContext&lt;'a, ...&gt;<br/>nabla: &'a Edge<br/>delta: &'a Node"]
    R["InkRecord<br/>state: Vec of bytes<br/>space: Vec of bytes<br/>(owned: a copy)"]
    G -.->|"borrows"| C
    G -.->|"borrows"| S
    X -.->|"borrows, no copy"| C
    X -.->|"borrows, no copy"| S
    G --> X
    X -->|"MEM copies"| R

    classDef own fill:#2e7d32,color:#fff,stroke:#111;
    class C,S,R own;
```

So until MEM nothing is copied: every step looks at the caller's original
objects, and the compiler refuses to let the Gateway outlive them.
The tests check this with `std::ptr::eq`, which asks "is it the very same
object?". After MEM the record owns its bytes, and a test drops the client and
the server and shows the record is still whole.

## 4. Generics and traits

*Look at what `G::execute` needs: not a concrete client, only "anything that
keeps the `ClientGraph` promise". Look at which promises you can keep yourself
and which only the crate can.*

A **trait** is a promise: a list of things a type can do. A **generic** such
as `G<Edge, L0, Mem>` is a recipe that works for any types that keep the
promises asked of them.

```mermaid
classDiagram
    class ClientGraph {
        <<trait, yours>>
        type Edge
        +edge() Option~Edge~
    }
    class ServerGraph {
        <<trait, yours>>
        type Node
        +node() Option~Node~
    }
    class CanonicalBytes {
        <<trait, yours>>
        TYPE_LABEL
        +canonical_bytes() bytes
    }
    class AnchorSource {
        <<trait, sealed>>
        +now() Result~Moment~
    }
    class Store {
        <<trait, sealed>>
    }
    class GitProvider {
        <<trait, sealed>>
        +host() Option~Host~
        +rights(repo) Access
    }
    class G~Edge, L0, Mem~
    G ..> GitProvider : EDGE
    G ..> AnchorSource : L0
    G ..> Store : MEM
    G ..> ClientGraph : execute needs
    G ..> ServerGraph : execute needs
    G ..> CanonicalBytes : the Edge and Node must keep it
    AnchorSource <|.. SystemClock
    AnchorSource <|.. FixedAnchor
    Store <|.. FileStore
    Store <|.. MemoryStore
    GitProvider <|.. Offline
```

You write the three traits at the top, for your own types. The three **sealed**
ones can only be kept by types inside the crate: a clock, a store or a host
that could be added from outside is one that could lie. `CanonicalBytes` also
asks each type for a **label** (`TYPE_LABEL`). The label goes into the hash,
so a `String` and a `Vec<u8>` holding the same bytes cannot be mistaken for
each other. A type that forgets its label does not compile.

## 5. Result and Option: no null, no exceptions

*Look at the exits of each box: success continues, failure becomes a named
error, and nothing is silent. Nothing after a failure runs.*

Rust has no `null` and no exceptions. A value that may be missing is an
`Option` (`Some(x)` or `None`). An operation that may fail is a `Result`
(`Ok(x)` or `Err(e)`). The `?` mark means "on error, stop here and hand the
error to my caller".

```mermaid
graph TD
    A["client.edge()<br/>Option"] -->|"Some(edge)"| B["server.node()<br/>Option"]
    A -->|"None"| E1["ContextError::MissingClientEdge"]
    B -->|"Some(node)"| C["cgs::compute<br/>Result"]
    B -->|"None"| E2["ContextError::MissingServerNode"]
    C -->|"Ok"| L["L0: a moment<br/>Result"]
    C -->|"Err"| E3["CgsError"]
    L -->|"Ok"| M["MEM, FS: ink, write, read back<br/>Result"]
    L -->|"Err"| E4["AnchorError"]
    M -->|"Ok"| D["HASH(@), emit<br/>Ok(GatewayOutput)"]
    M -->|"Err"| E5["StoreError<br/>Io, Corrupt, TooLarge, Busy"]
    E1 --> X["ExecutionError::Context"]
    E2 --> X
    E3 --> Y["ExecutionError::Cgs"]
    E4 --> Z["ExecutionError::Anchor"]
    E5 --> W["ExecutionError::Store"]

    classDef bad fill:#c62828,color:#fff,stroke:#111;
    class E1,E2,E3,E4,E5,X,Y,Z,W bad;
```

The client is always checked before the server, so two missing pieces always
report the same one first. `ExecutionError` keeps its cause (`source()`), so
the chain can be read back. A missing edge stops before L0 is even asked for a
moment, and before anything is written: the tests count the calls. The
`CgsError` exit cannot happen through `execute` today, because the context
always hands CGS two operands; it stays a typed error because the CGS function
can fail on its own.

## 6. Struct, impl and trait: Rust's class and interface

*Look at the left column of the table, then at the arrows: Rust has no
`class`, but these three parts do the same job.*

| In a class language | In Rust | Here |
|---|---|---|
| class with private fields | `struct` with fields not marked `pub` | `GitRepo`, `Secret`, `ExecutionHash` |
| methods | `impl Type { fn … }` | `G::execute`, `G::access`, `GitRepo::host` |
| interface | `trait` | `GitProvider`, the EDGE of `G` |
| subclass | a type that `impl Trait for Type` (no inheritance) | `Offline`, `FileStore`, `SystemClock`; later Codeberg, GitHub, GitLab |
| constructor that checks | `fn new(…) -> Result<Self, Error>` | `Owner::new`, `GitRepo::open` |

```mermaid
classDiagram
    class G~Edge, L0, Mem~ {
        -edge: Edge
        -l0: L0
        -mem: Mem
        +new(edge, l0, mem) G
        +execute(client, server) Result~GatewayOutput~
        +verify(proof) Result~u64~
        +verify_log() Result~u64~
        +repo(spec) Result~GitRepo~
        +rights(repo) Result~Access~
        +access(ring, repo) Result~Access~
    }
    class GitProvider {
        <<trait, sealed>>
        +host() Host
        +rights(repo) Result~Access~
    }
    class GitRepo {
        -host: Host
        -owner: Owner
        -name: RepoName
    }
    class FakeProvider {
        <<test only>>
    }
    class Secret {
        -value
        +expose() str
    }
    G --> GitProvider : EDGE, the only way out
    G ..> GitRepo : builds, checked
    GitProvider <|.. FakeProvider
    FakeProvider --> Secret : holds, never prints
```

**Sealed** means no code outside the crate can add a provider: a host that
can be added from outside is a host that can lie. A `GitRepo` has private
fields and a crate-private constructor, so the only way to get one is
`G::repo`, which checks it. `G` is the one public API over the Graph.

## 7. Who can build an `ExecutionHash`

*Look at the red path on the left: in 0.1.1 anyone could walk it. Look at the
right: every way in is shut, and even a lying store gives no proof.*

```mermaid
graph LR
    subgraph BEFORE["0.1.1: every step was public"]
        b1["any bytes"] --> b2["compute_operands"] --> b3["persist"] --> b4["write"] --> b5["ExecutionHash<br/>genuine"] --> b6["emit"]
    end
    subgraph AFTER["now: one door"]
        a1["G::execute over a<br/>CLIENT and a SERVER"] --> a2["...L0, MEM, FS..."] --> a3["a record committed<br/>and read back"] --> a4["ExecutionHash"] --> a5["GatewayOutput"]
        a6["any bytes"] -.->|"does not compile"| a4
        a7["a store that lies"] -.->|"read-back differs:<br/>no proof"| a3
    end

    classDef bad fill:#c62828,color:#fff,stroke:#111;
    class b1,b2,b3,b4,b5 bad;
```

A hash that anyone can forge proves only "these bytes were hashed", not "the
gate ran". Now the phase functions are private, the module paths are private,
the types that pass between the steps cannot even be named, and an
`ExecutionHash` has a private field that only a committed record can fill. And
the proof is derived from what the store *returns when read back*, so a store
that says "written" and keeps nothing gives no proof either. Small programs in
`tests/ui/` try each way in and are required to fail to compile. (Any type may
still claim to be a CLIENT: that is accepted, F06 in `audit.md`.)

## 8. The trust boundary

*Look at where the key icon sits: the secret never leaves the inner box.*

```mermaid
graph LR
    REQ["a request<br/>(untrusted text)"] --> P["identity parser<br/>validates owner and name<br/>host prefix read, then checked<br/>against the EDGE; address from the type"]
    P --> G["G<br/>checks the ring"]
    subgraph INNER["inside the provider"]
        KEY["Secret token<br/>prints as redacted"]
        PR["GitProvider<br/>bounded, timed, never cached"]
        KEY --- PR
    end
    G --> PR
    PR -->|"HTTPS, later"| HOST["the host's API"]
    HOST --> PR
    PR -->|"a right, or a named error<br/>never the token"| G
    G -->|"min(ring ceiling, host right)"| ANS["answer"]

    classDef secret fill:#c62828,color:#fff,stroke:#111;
    class KEY secret;
```

Three things hold at this boundary. Input is validated before anything else
(no `..`, no `/`, no look-alike letters, and the host the text names must be the EDGE's own). The
token is a `Secret` that prints as `<redacted>` and cannot be cloned. And the
host can only **narrow** what the ring allows, never widen it.

## 9. The test layers

*Look at the "sees" column: each layer is there because it can see something
the others cannot.*

```mermaid
graph TD
    U["unit tests<br/>inside src/*.rs<br/>see private items and the order of steps"]
    I["integration tests<br/>tests/*.rs<br/>see only the public API, on disk too"]
    T["tamper tests<br/>damage records and entries<br/>each damage must be named"]
    CF["compile-fail<br/>tests/ui, trybuild<br/>what must NOT compile"]
    PR["property tests<br/>proptest<br/>random inputs"]
    CT["contract suite<br/>one function per provider<br/>the trait only"]
    D["goldens<br/>recomputed by spec.py<br/>which shares no code with the crate"]
    SUR["surface test<br/>fails when lib.rs exports change"]

    U --> OK{"all green?"}
    I --> OK
    T --> OK
    CF --> OK
    PR --> OK
    CT --> OK
    D --> OK
    SUR --> OK
    OK -->|"yes"| GATE["cargo fmt, clippy, deny, audit<br/>then the checklist"]
```

A compile-fail test passes only when the code *fails* to build, and it
records the compiler's exact message, so it cannot start passing for a
different reason. The golden hashes are computed twice, once by the Rust code
and once by a short Python program written from the specification alone: if
they agree, the encoding is what the specification says. And each of these
layers was checked the same way: a deliberate bug was introduced, and the
tests caught it.

## 10. One request, from text to a right

*Read top to bottom: the host is asked every time, and the answer is only
information, never a permit.*

```mermaid
sequenceDiagram
    participant C as caller
    participant G as G
    participant P as GitProvider
    participant H as host API
    C->>G: repo("github:flipoyo/.dev")
    G->>G: parse and validate, same host as the EDGE?
    G-->>C: GitRepo, or a named error
    C->>G: access(ring, repo)
    G->>P: rights(repo)
    P->>H: ask, with the Secret, bounded and timed
    H-->>P: a right, or an error
    P-->>G: Access, or GitError
    G->>G: min(ring.ceiling(), host right)
    G-->>C: Access, or the error unchanged
    Note over C,H: asked again next time: a right revoked a moment ago is seen
```

Reading and writing repository *content* are designed but not built: each
will have its own ring and its own step in this sequence.

## Glossary

| Word | In plain terms |
|---|---|
| crate | one Rust package: here, `gx4g` |
| module | a file or folder of code with its own privacy |
| `pub` | "others may use this"; without it, it is private |
| `struct` | a bundle of named fields, like a record |
| `enum` | one of several named cases, like `Access::Read` |
| `trait` | a promise of behaviour, like an interface |
| `impl` | the code that keeps a promise, or adds methods to a type |
| generic | code written once for any type that keeps the promises it asks for |
| `&` | a borrow: look, do not keep |
| `'a` | how long a borrow stays valid |
| `Option` | a value that may be missing |
| `Result` | an operation that may fail, with the reason |
| `?` | on failure, stop and pass the error up |
| `pub(crate)` | visible inside this crate only |
| sealed trait | a trait only this crate may implement |
| compile-fail test | a test that passes only when the code does not compile |
