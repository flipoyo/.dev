Owner, 2026-11-21: *"je ne veux pas qu'une branche patrimoine apparaisse dans le repo cgitsync. l'appeler anonymous-1. il faudrait certainement créer l'option anonymous pour que la branche "project-name" ne soit pas créée mais seulement la troncature 6 digits du sha256(project-name), et si ce nom existe déjà alors ajouter -i à la troncature pour constituer le nom de branche. Autre option anonymous-i. Écrire le ticket dans ~/.cgs/ComplexGitSync-20261120231545, branch data-encrypt."*

Context: a private project (its `.cgs` declares the project `PATRIMOINE`) mounts the shared private/local repositories `.dev`, `.localSpec`, `.claude`, `.memory` and `omniscience`. Today each gets a branch `PATRIMOINE_<branch>`, visible to anyone who can list those repositories' branches.

Owner, 2026-11-21, on the form of the option: *"anonymous ne doit pas être écrit par l'utilisateur comme project-name mais une option après la déclaration du nom de projet, qui entraîne l'écriture dans les registres comme je te l'ai indiqué."* So the user writes `project = { name = "PATRIMOINE", …, anonymous = "sequence" }` and never types an alias. cgitsync computes the alias, and that alias is what the shared registers receive: branches, omniscience records, memory.

Probed 2026-11-21: cgitsync 8.9.4 accepts `anonymous` without a word and ignores it. Until the option lands, a bootstrap of such a `.cgs` would write the real name everywhere.

The plan is [AnonymousProject](../openTickets/data-encrypt_2-14_AnonymousProject_DevPlanTicket.md), on branch `data-encrypt`.
