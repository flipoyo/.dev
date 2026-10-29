Since the start of BeforeBeta the github CI reports always failing GoldenVector tests. cgitsync must be multi-os before beta.

Here is the CI report of the latest push : 
CI / golden-vectors (macos-latest) (push) Failing after 18s
Details

CI / golden-vectors (ubuntu-latest) (push) Failing after 13s
Details

CI / golden-vectors (windows-latest) (push) Failing after 35s
Details

CI / test (push) Failing after 6m
Details

CI / versioning (push) Successful in 17s
Details

---

## Closed 2026-10-29: turned into a plan

Planned as FixGoldenVector, then merged the same day into `openTickets/main_1-2_alpha2beta_DevPlanTicket.md` (Part B), run by BeforeBeta as S10b. What the CI logs
show:
- **`golden-vectors`** has run no test since 8.0.1. It names `tests/unit/test_gts_integrity.py`, which MerkleRoot
  deleted, so pytest exits with "file or directory not found" on all three systems.
- **`test`** has failed since 8.3.0 on the two `examples/gx4g-*.cgs` files, whose first lines are notes, not TOML.

The owner's words above are unchanged.
