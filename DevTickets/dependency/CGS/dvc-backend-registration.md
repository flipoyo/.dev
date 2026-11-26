`data = { backend = "dvc" }` validates, but nothing runs it: in 8.14.2 `DataManager` registers no backend, so `dvc` answers UNSUPPORTED (`tree/data_manager.py`, "until the DvcBackend ticket registers one").

The first HTBS twin, `gitlab:htas1/ht-synthcase-1` (branch `twin-launch`), keeps its results under DVC in the root repository. Every data step is therefore typed by hand around cgitsync, in an order that matters (its report `20261125_Report_TwinLaunch.md`, steps F and G):
- `dvc add` and `dvc push` must come before `cgitsync push`, or the pushed `.dvc` pointers name data the remote does not have;
- after a restore, `dvc pull` comes after `cgitsync initialise`;
- `dvc status -c` is the only check that cache and remote agree before a State is frozen.

Asked: register the DvcBackend so that `cgitsync push`, `pull`, `status` and `release freeze` run the matching DVC phase on each repository that declares `data`, in that order. Refuse a push whose pointers name data missing on the remote. Report the data state in `status`.

Needed by HydrologicalTwinAlphaSeries's plan HtbsFirstSpecs (steps G, C1, E1). It does not block phase 1.
