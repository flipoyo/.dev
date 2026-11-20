# htas-dev — building, testing and finishing a change in HydrologicalTwinAlphaSeries

*Created: 2026-11-19*

*Fills in: ../../.distant/dev-sync/AgentConduct.md*

## Abstract — read this first

**What this document is.** This project's own fill-in for the
before-committing checklist, the pair rule and the testing section that
`DevSpecs.md` and `AgentConduct.md` state in general: which commands, which
repository, which paths, which choices. It restates none of their rules.

**Why it exists.** The shape of "finish a change" is the same for every
project, so it is written once in `AgentConduct.md`. The commands are this
project's, and this is the only place that holds them; `CLAUDE.md` keeps
the step titles. It was seeded from ComplexGitSync's `cgitsync-dev.md` and
cut down to what HydrologicalTwinAlphaSeries actually has.

**What you will find.** The Pixi commands, how to bootstrap a working
checkout, the eight checklist steps with this project's commands, the
doc-impact map that step 7 reads, the pair
rule's fill-in, the attribution fill-ins, and the testing layout.

**Who it is for.** Anyone — human or agent — changing code or docs in this
repository. End users only need [README.md](../../../README.md).

**What you need to do with it.** Follow it before every commit.

```mermaid
graph TD
    AC["AgentConduct.md<br/>the shape (shared)"] -->|"filled in by"| ME["htas-dev.md<br/>YOU ARE HERE"]
    ME --> V["Versioning.md<br/>steps 2, 4, 5"]
    ME --> T["DevTickets/<br/>the pair rule"]
    CLAUDE["CLAUDE.md<br/>the eight step titles"] -->|"points here"| ME

    classDef here fill:#1565C0,color:#fff,stroke:#111,stroke-width:2px;
    class ME here;
```

---

## Commands

This project is laid out as ComplexGitSync is (owner, 2026-11-19): a root
`pixi.toml`, the Pixi manifest that holds the version, beside a
`pyproject.toml` kept for the Python build and the `htas` console script. Never bare `pip`/`venv`.

```bash
pixi install                         # create/update the environment
pixi run test                        # pytest, tests/unit + tests/integration
pixi run lint                        # ruff check src tests
pixi run run                         # smoke test of the package entry point
cgitsync version diagnose            # how the tree is versioned; reads only
cgitsync version bump <level>        # orchestrator: runs pixi run bump-version
pixi run bump-version <level>        # writes pixi.toml, pyproject.toml, the guide
pixi run bump-build                  # worker: bumps __build__
```

**There is no CI** (owner, 2026-11-20, DocsOnTheFly D4): the agent runs
the gate on its own machine before every commit and push with `cgitsync`.
The gate is `pixi run lint`, `pixi run test` (which holds the QGIS-free
guard, `tests/unit/test_qgis_free.py`, and the documentation drift tests,
`tests/unit/test_docs_sync.py`) and `pixi run run`. The smoke test on the
CaWaQS test case runs when `CWAQS_FIXTURE_ROOT` points to a sparse clone of
`gitlab.com/cawaqs/gtest/testcases` (tag `v0.1-cwv-gis-smoke-CI`; the
recipe is in `tests/README.md`), and skips otherwise.

### Bootstrapping a working checkout

A plain `git clone` gets the code but neither `docs/hydrological_twin` nor
any agentic mount. Bootstrap the developer spec, `.config/htas-dev-beta.cgs`;
its header lists the install commands in order (bootstrap, `branch create
HT-BETA --private`, `checkout HT-BETA`, `self-history adopt`, `push`).

```bash
pixi run cgitsync bootstrap .config/htas-dev-beta.cgs HydrologicalTwinAlphaSeries
export CGSHOME=...      # copy it from bootstrap's own output
cd "$CGSHOME" && pixi install
```

The private/local mounts (`.agent/.local/*`, `.omniscience`) are on
`HydrologicalTwinAlphaSeries_HT-BETA`, derived by `cgitsync` from the tree;
the distant ones stay on `main`; ComplexGitSync, the tool, stays on
`CGS-ALPHA` and is never written from this tree.

## Before committing — this project's own fill-ins

Do all of these as part of the change, not as a follow-up. The shape is
[AgentConduct.md](../../.distant/dev-sync/AgentConduct.md) §1.

1. **`pixi run lint` and `pixi run test` must both pass**, with the
   QGIS-free guard (`test_qgis_free.py`: no `qgis`, `qgis.PyQt`, `PyQt5`
   import anywhere under `src/`) and the drift tests (`test_docs_sync.py`)
   inside the test run. Lint shows no new error: the errors it reported
   before the change are listed in the report, not hidden. Tests needing the
   CaWaQS fixture skip without `CWAQS_FIXTURE_ROOT`; say so in the report
   when they did.
2. **`pixi run bump-build` for any change under `src/`**,
   the worker's step. It is never the last versioning step: see step 4.
3. **`cgitsync status`, run from this tree's own root, must show
   `errors=0`.** Fix a repository the change left unreadable before calling
   the task finished.
4. **`cgitsync version bump {patch,minor,major}`, from the tree's root,
   for every change under `src/`** and every change to what a task does,
   `patch` at least. Run it with `--dry-run` first. The
   level is the orchestrator's call ([Versioning.md](Versioning.md)). Never
   hand-edit a version field: `bump-version` writes every copy, all or
   none. Nothing automatic writes one.
5. **Rebuild the user guide** after every bump and every change to
   `docs/hydrological_twin` (its version is a `bump-version` target).
6. **Update [AdditionalSpecs.md](../.localSpec/AdditionalSpecs.md)** if a
   module's responsibility moved between layers: its layer table and
   diagram, in the same change. A deferred clean-up goes in
   `docs/TODO.md` or a ticket, never only in a commit message.
7. **Update every document the doc-impact map names for the change**
   (below), in the same change. `src/` is the reference: a document names
   no path, module, class, method, keyword, verb, `kind`, task or command
   that `src/` does not have (owner, 2026-11-20). `test_docs_sync.py`
   catches a name that drifted; the map catches a document left silent. The
   root `README.md` is the user's front page, at most 250 lines, on
   ComplexGitSync's model: no method or command table, no developer
   material (that is `docs/developer_guide.md`).
8. **Deliver one commit message** and use it unchanged in every repository
   the change touched: `HydrologicalTwinAlphaSeries-<version>`, plain
   English, three lines at most, the version read from `pixi.toml` after
   step 4 (`cgitsync commit` checks it). Deliver it as text; committing and pushing are the owner's call.

## The doc-impact map — step 7

A change to the left-hand column updates, in the same change, every
document on its right.

| A change to | Updates |
|---|---|
| `ht/client/`: a method, a `*Result` | `docs/api_capabilities.md` (*Client operations*), `docs/api_examples.md`, the user guide (`HTAS_user_guide.tex`, *The client*), the README *Use cases* row that uses it |
| `ht/developer/`: a verb, a `kind`, a `*Request` field | `docs/api_capabilities.md` (its verb's section lists every kind), `docs/api_examples.md`, the user guide (*The façade*), `docs/canonical_monolith.md` and White Book chapter 5 when a verb is added or removed |
| `cli/`: a command, an option, an exit code | `docs/api_capabilities.md` (*Command line*), the user guide (*The command line*, whose *Command reference* `test_user_guide_cli.py` holds to the parsers: a command or an option it does not name fails), README *Getting help*, the tutorial that uses it |
| `ht/developer/kinds.py`: a kind | `docs/api_capabilities.md`, the user guide's table of `htas-dev` kinds (`test_user_guide_cli.py` fails without it) |
| `domain/` | `docs/domain_model.md` |
| A package or module added, moved or removed | `docs/developer_guide.md` §2–§3, `AdditionalSpecs.md` §2 (step 6), White Book chapter 5 (*Package layout*) |
| `services/private/` or what reaches it | `src/HydrologicalTwinAlphaSeries/services/SECURITY.md` |
| A new use case | A README *Use cases* row |
| `pixi.toml` tasks, the install | README *Installation*, `docs/developer_guide.md` §1, `tests/README.md` |
| `tests/` layout, the fixture | `tests/README.md` |
| What HTAS implements of the White Book's target | White Book chapters 5 and *Current Development*, and the chapter that described it as target |

A chapter of the White Book that describes the HydrologicalTwin target,
which HTAS does not implement, opens with `\htastarget`; only there may it
use the target's vocabulary, listed in `test_docs_sync.py`'s `TARGET_NAMES`.
Everything it says about HTAS itself is held to `src/`.

## The pair rule — this project's fill-in

The rule in full is [AgentConduct.md](../../.distant/dev-sync/AgentConduct.md)
§4. Implementing a ticket from [DevTickets/openTickets/](DevTickets/openTickets/)
takes a worker agent that makes the change and an independent orchestrator
agent that quotes it against this checklist, runs step 4
(`cgitsync version bump`), and writes the
record with `cgitsync self-history add` once `self-history adopt` has been
run. Drafting, ranking or closing a ticket is orchestration already. **The
orders are in [CLAUDE.md](../.claude/CLAUDE.md)**, *When the owner says
`implement <ticket>`*.

This project has no `check-tickets` task: the gate is `cgitsync commit`'s
own refusal of a planning ticket archived without its orchestrator's
record, and the orchestrator's re-quote.

## Attribution — this project's fill-ins

[AgentConduct.md](../../.distant/dev-sync/AgentConduct.md) §3 states the
rules; [AgentDataContract.md](../../.distant/dev-sync/AgentDataContract.md)
the owner's intent.

- **No agent credit on a commit**, merge or pull request, in any repository
  of the tree.
- **Public front.** The project's own repositories are
  `HydrologicalTwinAlphaSeries` and `hydrological_twin` (`docs/hydrological_twin`).
  An example there that needs an agent's vendor or model writes
  `vendor-name` and `model-name`. The README has no *LLM assistance*
  section yet; adding one is the owner's decision.
- **Private repositories** (`.localSpec`, `.claude`, `.dev`, `.omniscience`,
  `.memory`, `.self-history`) name the real vendor and model.
- **Accounting.** What an agent did goes in `.cgitsync/.memory/.self-history`
  only, never into a public repository.

## Testing — this project's own layout

[DevSpecs.md](../../.distant/dev-sync/DevSpecs.md) *Testing* is the rule.

- Unit tests: `tests/unit/` (with `services/` and `tools/` subpackages);
  integration tests: `tests/integration/` (facade lifecycle, smoke runs on
  real CaWaQS meshes).
- `pytest` runs with `pythonpath = ["src"]`; the `slow` marker deselects
  long runs (`-m "not slow"`).
- Tests that need real CaWaQS data skip cleanly when it is absent: the
  test case through `CWAQS_FIXTURE_ROOT` (`tests/README.md`), the large
  real meshes of `test_aq_boundary_faces_real_meshes.py` by path. No test
  reaches the network.
