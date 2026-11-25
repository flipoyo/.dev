# .dev

*Created: 2026-09-22*

How CaWaQS's work gets done: the before-committing checklist with this
project's commands (`cawaqs-dev.md`), how it numbers and releases
(`Versioning.md`, with the real tool in `scripts/versioning.py` and its
tests in `scripts/tests/`), and the planning surface (`DevTickets/`, with its
own `README.md`).

This project's own, private and writable (`private = true, writable =
true`) — unlike `dev-sync` (`DevSpec`), which is shared, read-only, and the
same for every project. Each document here fills in a shared pattern and
opens with a `*Fills in:*` line naming it; the shared one holds the rule.
`DevTickets/` is here because a ticket is part of how the work gets done and
not a specification. The versioning tool is private on purpose: a user
install has no `.dev` mount, so it cannot bump.
