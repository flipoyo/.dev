# .dev

*Created: 2026-09-22*

How ComplexGitSync's work gets done: the before-committing checklist with
this project's commands (`cgitsync-dev.md`), how it numbers and releases
(`Versioning.md`, with the real release script in `scripts/bump_version.py`),
and the planning surface (`DevTickets/`, with its own `README.md`).

This project's own, private and writable (`private = true, writable =
true`) — unlike `dev-sync` (`DevSpec`), which is shared, read-only, and the
same for every project. Each document here fills in a shared pattern and
opens with a `*Fills in:*` line naming it; the shared one holds the rule.
`.versioning` and `.auto` were folded into this repository (`AgenticTwoLevels`,
2026-10-08), and `DevTickets/` came here from `.localSpec`, because a ticket
is part of how the work gets done and not a specification.
