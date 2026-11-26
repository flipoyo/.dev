A `.cgs` cannot name where a repository's data lives: `data.service` is reserved and refused until DataArchitecture §7 C2 is settled (`git_repo/data_spec.py`).

In `gitlab:htas1/ht-synthcase-1` the DVC remote (a VPS reached over SSH) is therefore written by hand in `.dvc/config`, outside the tree's description. A `.gts` State thus records the pointers to the results but not where their bytes are, and a restore on another machine works only if someone tells the user the remote. HTBS will have several such spaces (one per twin, plus a gate space), each with its own data remote.

Asked: settle C2 so that a `.cgs` entry can declare its data service (backend and remote address, never a user name or a password, which stay in `.dvc/config.local`). Record it in the `.gts` State, and check at install that the remote is reachable.

Needed by HydrologicalTwinAlphaSeries's plan HtbsFirstSpecs (steps G, C1, and the gate space). It does not block phase 1.
