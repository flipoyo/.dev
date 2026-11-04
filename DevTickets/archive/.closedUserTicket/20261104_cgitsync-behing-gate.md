I bootstraped ../atCgS/examples/cgs-opx.cgs

environment_root = "root"
environment = { tools = { python = "3.11", git = "2.30", pixi = "0.65" }, manifests = ["pixi.toml"] }

project = { name = "cgs", default_branch = "opx", fallback_branch = "CGS-ALPHA" }

repos = [
    { repository = "github:flipoyo/atCGS", relative_path = ".", nested_config = "disabled" },
    { repository = "github:flipoyo/ComplexGitSync", fallback_branch = "CGS-ALPHA", nested_config = "disabled" },

    { repository = "github:flipoyo/omniscience", relative_path = ".omniscience", fallback_branch = "main", private = true, writable = true, nested_config = "disabled" },
    { repository = "github:flipoyo/.memory", relative_path = ".cgitsync/.memory", fallback_branch = "main", private = true, writable = true, nested_config = "disabled" },

    # .distant — shared, read-only, the same for every conforming project
    { repository = "github:flipoyo/.ticketing", relative_path = ".agent/.distant/ticket", default_branch = "main", fallback_branch = "main", private = true },
    { repository = "github:flipoyo/DevSpec", relative_path = ".agent/.distant/dev-sync", default_branch = "main", fallback_branch = "main", nested_config = "disabled", private = true },
    { repository = "github:flipoyo/DocSpec", relative_path = ".agent/.distant/documentation", default_branch = "main", fallback_branch = "main", nested_config = "disabled", private = true },

    # .local — this project's own, writable
    { repository = "github:flipoyo/.dev", relative_path = ".agent/.local/.dev", fallback_branch = "main", private = true, writable = true },
    { repository = "github:flipoyo/.localSpec", relative_path = ".agent/.local/.localSpec", fallback_branch = "main", private = true, writable = true },
    { repository = "github:flipoyo/.claude", relative_path = ".agent/.local/.claude", fallback_branch = "main", private = true, writable = true },
]

And obtained flipoyo@io:~/.cgs/cgs-20261104014355/ComplexGitSync$ pixi run cgitsync status
cgshome=/home/flipoyo/.cgs/cgs-20261104014355 (from current directory) use_case=nested
source=/home/flipoyo/.cgs/cgs-20261104014355/.cgitsync/state/bdf5bd5a1ce310c920d9beef2c957ac78940788787c51000b00416efbf0fa7db.gts (from ledger)
/home/flipoyo/.cgs/cgs-20261104014355/ComplexGitSync/src/ComplexGitSync/orchestre/document_loader.py:256: UserWarning: the project is 'cgs' but its root repository is 'atCGS' on its provider; the project's name is used for its branches, tags and id.
  OperatingSpace(self.client.registry).warn_if_names_differ()
summary ready=true complete=true use_case=nested profile=dev cgitsync_branch=CGS-ALPHA repos=10 dirty=1 staged=0 ahead=0 behind=0 unmeasured=0 recorded_mismatch=0 errors=0
REPOSITORY      PATH                           SCOPE            LOCAL_BRANCH  UPSTREAM_BRANCH   LOCAL  SYNC    HEAD      RECORDED
---------------------------------------------------------------------------------------------------------------------------------
ComplexGitSync  ComplexGitSync                 project          CGS-ALPHA     origin/CGS-ALPHA  clean  synced  06c34bc6  06c34bc6
omniscience     .omniscience                   private/local    main          origin/main       clean  synced  8b4c85e0  8b4c85e0
.memory         .cgitsync/.memory              private/local    main          origin/main       clean  synced  ee601f22  ee601f22
.localSpec      .agent/.local/.localSpec       private/local    main          origin/main       clean  synced  072c3615  072c3615
.dev            .agent/.local/.dev             private/local    main          origin/main       clean  synced  c85bb1d6  c85bb1d6
.claude         .agent/.local/.claude          private/local    main          origin/main       clean  synced  8f08fa0b  8f08fa0b
.ticketing      .agent/.distant/ticket         private/distant  main          origin/main       clean  synced  a471f264  a471f264
DocSpec         .agent/.distant/documentation  private/distant  main          origin/main       clean  synced  02ee0b1f  02ee0b1f
DevSpec         .agent/.distant/dev-sync       private/distant  main          origin/main       clean  synced  56540c75  56540c75
cgs             .                              project          CGS-ALPHA     origin/CGS-ALPHA  dirty  synced  071f5e0b  071f5e0b
warning: tree is split across branches — omniscience is on 'main', expected 'cgs_CGS-ALPHA'; .memory is on 'main', expected 'ComplexGitSync_cgs_CGS-ALPHA'; .localSpec is on 'main', expected 'cgs_CGS-ALPHA'; .dev is on 'main', expected 'cgs_CGS-ALPHA'; .claude is on 'main', expected 'cgs_CGS-ALPHA'. Run 'cgitsync checkout <branch>' to put it back.
warning: split branch 'CGS-ALPHA' — cgs: live; ComplexGitSync: live; .claude: absent; .dev: absent; .localSpec: absent; .memory: absent; omniscience: absent
legend: SCOPE — project = the work itself; private = a repository that configures the project, shared with your other projects; local = yours to write, distant = read-only
READY ready=true complete=true gittree_created=true gittree_active=true

ComplexGitSync and atCGS should be on project-name_branch, but they are on branch