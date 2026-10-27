The CLI is very reach. It would be wise to reduce it to the minimal. Security comes from there because it reduces the attack surface. Among all class methods many may be unused or depricated. It would be interesting to map class and methods by ring and see which ones are exposed through the CLI. with the objective that the CLI lands mostly at ring interfaces. This is a mapping ticket for further decisions and Security and consistency reinforcement of the project. The Merkle Tree of MerkleRoot must never be accessible by cgitsync nor gx4g. It is the interface never materialised.

From this map CLI cmd may be kept, reinforce, adapted or disclosed.

Reorganise Class around this MerkleTree. ComplexGitSync is the Gate of GitTree. WorkingGitTree is the Operating Space. .cgs is the API of USER. .gts is the API of DEV, OperatingSpace is the API of OPX. @gx4g is the UNIVERSAL API-GATE. cgitsync is therefore the Tree Operator of the infrastructure. Check that the Ring API is OK gx4g outer ring API, .cgs ring3<->4 API, .gts ring 2<->3 API, OperatingSpace ring 1<->2

Les interaction GitRepo en ecriture sont le privilege de gx4g. cgitsync n'est qu'un executant. Cela veut dire qu'il faut un diagnostic de toutes les methodes faisant appel aux API GitProvider pour les faire migrer vers gx4g. La migration vers gx4g se fera grace au hash256(MerkleRoot) des states et GitRepo concernés. MerkleRoot doit ainsi devenir une classe à part entière et les methodes de calcul des hash d'état doivent lui etre deleguées. A terme cette classe deviendra certainement un repo à part entière 

---

## Agent's note, 2026-10-27: where each part went

*The owner's words above are unchanged. Closed by the ticket review of
2026-10-27, which made every open ticket agree with it. The owner answered
four questions through `AskUserQuestion`: every provider API call, read or
write, migrates to gx4g; BranchProtection is split; everything here is
before beta except the migration; "disclosed" means withdrawn from the CLI.*

| The owner's request | Where it went |
|---|---|
| Map classes and methods by ring, see what the CLI exposes, the CLI at ring interfaces, unused and deprecated methods | **Minimalism** (`main_1-3`), BeforeBeta S5 |
| The ring APIs to check: gx4g outer, `.cgs` 3↔4, `.gts` 2↔3, OperatingSpace 1↔2; the roles of ComplexGitSync, WorkingGitTree, `cgitsync` | Minimalism §1 and §4 (the check), MerkleRoot §3 (written into the code), `AdditionalSpecs.md` *Architecture rules* |
| MerkleRoot a class of its own, the State hashes delegated to it, the tree never materialised, later its own repository | **MerkleRoot** (`main_1-4`), BeforeBeta S6; the rule in `AdditionalSpecs.md` and `digest.md` |
| Commands kept, reinforced, adapted or withdrawn | **CliReduction** (`main_1-5`), BeforeBeta S7 |
| GitRepo writes are gx4g's privilege; every provider API method migrates, addressed by hash256(MerkleRoot) | **ProviderMigration** (`main_2-10`); BranchProtection split (`main_1-6`, its M0–M4 handed to gx4g as §9); the rule in `AdditionalSpecs.md` and `digest.md` |
| Constraints on the whole of BeforeBeta | BeforeBeta §2.5, and its D3 answered |
