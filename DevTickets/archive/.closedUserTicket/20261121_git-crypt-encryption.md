Owner, 2026-11-21: *"utiliser l'encryption si compatible avec complexGitSync, et que tu me dises si cgitsync doit évoluer"*, then, on the three evolutions proposed: *"oui [rédige-les comme tickets] dans /home/flipoyo/.cgs/ComplexGitSync-20261120231545 dans lequel tu ajouteras aussi une folder .config contenant [cgitsync-encrypt.cgs]"*

Context: the PATRIMOINE project (private, outside this repository) keeps its data as CSV in repositories encrypted with git-crypt, and keeps an agent tree that is never unlocked, so the agent never sees the amounts.

Compatibility was probed on 2026-11-21 (cgitsync 8.9.4, git-crypt 0.8.0, local bare remotes, `_build_remote_url` patched as in `test_behind_gate.py`). It works with no change: `bootstrap` without the key, `status` READY whether locked or unlocked, `add`/`commit`/`push`, `release freeze`, and a commit from a locked tree. One leak was found: in a locked tree, a **new** file under an encrypted path is committed **in clear**.

Owner, 2026-11-21: *"switch [le tree] sur la branch data-encrypt et écris les cgs demandés ici en fonction"*.

The plan is [EncryptedRepos](../openTickets/data-encrypt_2-13_EncryptedRepos_DevPlanTicket.md), on branch `data-encrypt`. Its test topology is `.config/cgitsync-encrypt.cgs` at the root of the ComplexGitSync repository, and `.config/CGSenc-space.cgs` is the template of the nested space's own `.cgs`.
