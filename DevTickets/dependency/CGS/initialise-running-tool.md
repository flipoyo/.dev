`cgitsync initialise` deletes and re-clones every dependency whose destination already holds files, once it has checked that none holds unpushed work (`orchestre/installer.py`). Nothing exempts the ComplexGitSync clone that is running the command. In nested mode that clone sits inside the tree, so declaring it in the `.cgs` makes `initialise` delete the tool it is running from.

Every nested install works around it the same way, and says so in a comment: ComplexGitSync is not declared, it is cloned by hand and gitignored. The workaround appears in `gitlab:htas1/ht-synthcase-1` (`.config/*.cgs`, which cite it as "BUGS.md #2") and in `gitlab:cawaqs/cawaqs` 4X (`install.sh`, `.config/cawaqs.cgs`). The tool's version is therefore missing from the tree's description and from its States, which a bit-for-bit resimulation needs to record.

Asked: when a declared entry is the running installation, adopt it in place (check its remote and branch, never delete it), or refuse with a message saying so. Then a nested `.cgs` can declare ComplexGitSync like any other dependency.

Needed by HydrologicalTwinAlphaSeries's plan HtbsFirstSpecs (steps P1 and C1, which pin every tool of the resimulation).
