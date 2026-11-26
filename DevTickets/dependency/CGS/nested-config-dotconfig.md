`nested_config = "auto"` reads only the `*.cgs` at a repository's root (`tree/discovery.py`, `_resolve_nested_config_path`). The projects that conform to the agentic layout now keep theirs in `.config/`: CaWaQS 4X (`.config/cawaqs.cgs`, `.config/cawaqs-dev-4X.cgs`), HydrologicalTwinAlphaSeries (`.config/htas-dev-beta.cgs`) and MOLONARI1D (`.config/molonari.cgs`).

The result is silent. In `gitlab:htas1/ht-synthcase-1`, cawaqs is mounted with `auto` (the default). On 4X its root holds no `.cgs`, so the entry resolves to a plain leaf, and the 17 libraries CaWaQS needs to build are never cloned, with no warning. The opposite happens to HTAS, mounted the same way: its root still holds `htas-beta.cgs`, which `auto` grafts, bringing ComplexGitSync and `github:flipoyo/.memory` under `postProc/`.

Asked: either let `auto` find a single `.config/*.cgs` when the root has none, or warn when an `auto` entry resolves to a leaf while its repository holds `.config/*.cgs`, naming the files and the `nested_config = "<file>.cgs"` spelling. Document which of the two is the rule, and show both cases in a tutorial on mounting another project's repository.

Needed by HydrologicalTwinAlphaSeries's plan HtbsFirstSpecs (D3, steps P1 and C1).
