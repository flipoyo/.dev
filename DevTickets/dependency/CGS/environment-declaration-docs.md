The `.cgs` keys `environment_root` and `environment = { tools, manifests }` are not documented in the README or a tutorial, and the shared examples (`cgitsync-alpha.cgs`, `cgitsync-ht-beta.cgs`, `gx4g-alpha.cgs`) copy them without saying why. A project author cannot tell what they add, given that cgitsync records the environment it runs in anyway.

What the code does today (ComplexGitSync HT-BETA, `tree/environment_spec.py`, `tree/tree_env.py`):
- `environment.tools` is a list of minimum versions, not an environment. It makes cgitsync probe those executables, so `pixi` appears in the record. It also makes `cgitsync env check` exit non-zero, with an "environment drift" warning at install and on the tree commands, when a tool is missing or older.
- `environment.manifests` adds glob patterns to the built-in list (`pixi.toml`, `pixi.lock`, `pyproject.toml`, `requirements*.txt`, `environment.yml`, `package.json`, `Makefile`, `.tool-versions`). In every example the pattern given is already built in, so the key changes nothing there.
- `environment_root` is checked against the configured repositories and recorded in the Environment record ("undeclared" when absent). It does not change where manifests are read, which is always the root repository's subtree.

Asked: document the three keys, and add a tutorial section on declaring a project's minimum environment and reading `cgitsync env show` / `env check`. Either give `environment_root` an effect or say it is a label only. Drop the redundant `manifests` entries from the examples, or say why they are kept.
