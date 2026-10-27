i was able to delete a branch as a random user with a simple install.cgs. This is not secured. Only Dev can be granted deletion rights for branch or other strategic assets. It is already a large privilege. It would be good to be able to lock a branch from deletion. The problem becomes who can lock and how recognising the person who locked for granting the deletion privilege. Generally closing should be dev privilege. deleting should be maintainer privilege. But those tier are absent from cgitsync. First write a DevPlanTicket for cutting closing and deletion rights for any artefacts for simple users ie without any private repo

---

## Agent's note, 2026-10-13 — what the plan took, and what is left to investigate

*The owner's words above are unchanged. This note was added when the plan
`DevOnlyClosure` was written; the short ticket stays open until the questions
below are answered by a later ticket.*

**Taken by the plan:** the last sentence only. In a tree with no private
repository, `branch close` and `branch delete` are refused. That is an
accident guard: the profile comes from the user's own `.cgs`, so declaring one
private repository makes the tree a DEV tree, and `git push origin --delete`
needs no `cgitsync`. Only the provider's branch protection stops a determined
user.

**Not manageable yet, with what to investigate for the next ticket:**

1. **Locking a branch against deletion.** A lock `cgitsync` records can only
   be read by `cgitsync`, so it protects nothing against `git` or the
   provider. Investigate: can `cgitsync` set the provider's own protection
   (GitLab protected branches, GitHub branch protection or rulesets, Gitea
   branch protection) with the tools `provider.py` already wraps (`glab`, `gh`,
   `tea`)? Then "lock" means "protect on the provider", and the lock's owner
   is whoever the provider records. Find out per provider what the CLI can do
   and which role it needs.
2. **Who may lock, and recognising them.** `git config user.name` is not an
   identity. Investigate the provider's authenticated answer instead: with the
   user's own `glab auth` / `gh auth`, what is their role on this project
   (GitLab: Guest, Reporter, Developer, Maintainer, Owner; GitHub: read,
   triage, write, maintain, admin)? That reads a fact the provider enforces,
   instead of one the user can edit in a `.cgs`.
3. **Dev and maintainer tiers.** The owner is right that they are absent. The
   less costly route may be not to invent them: map "closing" to the provider's
   Developer role and "deleting" to Maintainer, read from the provider at run
   time (point 2), and keep the profile test of `DevOnlyClosure` as the offline
   fallback when no provider tool is signed in. Investigate what happens
   offline, on an unsupported provider, and on a self-hosted one whose roles
   differ.
4. **"Other strategic assets".** The sweep found no other command that deletes
   on a remote from a user's tree: no command deletes a tag, `memory reboot`
   has no remote in a USER tree, `pull --force` and `rm` act locally. Which
   assets does the owner mean? Candidates to ask about: tags (a release tag
   rewritten by hand), the `ancestors` branch, a shared private repository,
   the memory repository of a DEV tree. A new command that deletes any of them
   must go behind the same gate; `DevOnlyClosure` adds a test that fails when a
   caller of `delete_remote_branch` appears unguarded.
5. **A cgitsync-visible lock without the provider.** If a provider cannot
   protect a branch (a bare git server), the only record is a file in a private
   configuration repository that the DEV trees read. It is honest only as a
   convention among developers, never against a user. Decide whether that is
   worth building before point 1 is known.
6. **Who can remove a lock.** Follows from 1 and 2; leave it until those two
   are answered.

**Suggested order for the next ticket:** answer 1 and 2 by trying `glab` and
`gh` on a throwaway project (a short spike, no code in `src/`), then write the
ticket for 3 on what the spike shows.

---

## Agent's note, 2026-10-27: the lock and the tiers are gx4g's

*Added by the ticket review that integrated the short ticket `minimalism`.*
Every call to a provider's API is now gx4g's privilege (owner). Locking a
branch against deletion and recognising a developer or a maintainer both
need one, so BranchProtection was split. `cgitsync` keeps the USER-tree
refusal that DevOnlyClosure built, and reports a branch that died anyway to
the Omniscience register (BranchProtection M5). The lock and the two tiers
are the requirement handed to gx4g, in BranchProtection §9. This short
ticket closes when BranchProtection is archived.
