I ran 

nflipo@zagros-fon:~/APOUB/ComplexGitSync$ pixi run cgitsync bootstrap examples/complexgitsync-dev.cgs 
{"operation": "CGS-BOOTSTRAP", "event": "command_start", "command": "bootstrap", "source_path": "/home/nflipo/APOUB/ComplexGitSync/examples/complexgitsync-dev.cgs", "project_root": "/home/nflipo/.cgs/ComplexGitSync-20261030150348"}
git_command=git clone (executed per repo)
{"operation": "GT-CLONE", "event": "repo_state_transition", "repo_name": "ComplexGitSync", "absolute_path": "/home/nflipo/.cgs/ComplexGitSync-20261030150348", "previous_repo_lifecycle_state": "DECLARED", "repo_lifecycle_state": "READY", "previous_sync_state": "PENDING", "sync_state": "ALIGNED", "current_ref_kind": "branch", "current_ref_name": "main", "target_ref_kind": "branch", "target_ref_name": "main", "resolved_ref_kind": "branch", "resolved_ref_name": "main", "commit_sha": "8b59e42300d3b75b4746c4ceb98218578d704b1e", "fallback_branch": "main", "fallback_reason": null}
{"operation": "GT-CLONE", "event": "repo_state_transition", "repo_name": "DocComplexGitSync", "absolute_path": "/home/nflipo/.cgs/ComplexGitSync-20261030150348/docs", "previous_repo_lifecycle_state": "DECLARED", "repo_lifecycle_state": "READY", "previous_sync_state": "PENDING", "sync_state": "ALIGNED", "current_ref_kind": "branch", "current_ref_name": "main", "target_ref_kind": "branch", "target_ref_name": "main", "resolved_ref_kind": "branch", "resolved_ref_name": "main", "commit_sha": "ed83921b73e45af40b15ef417d6a0798c36aa440", "fallback_branch": "main", "fallback_reason": null}
{"operation": "CGS-RUN", "event": "fallback_applied", "repo_name": ".memory", "absolute_path": "/home/nflipo/.cgs/ComplexGitSync-20261030150348/.cgitsync/.memory", "target_ref_kind": "branch", "target_ref_name": "ComplexGitSync_ComplexGitSync", "resolved_ref_kind": "branch", "resolved_ref_name": "main", "fallback_branch": "main", "fallback_reason": "branch 'ComplexGitSync_ComplexGitSync' not found on remote; cloned 'main' instead"}
{"operation": "GT-CLONE", "event": "repo_state_transition", "repo_name": ".memory", "absolute_path": "/home/nflipo/.cgs/ComplexGitSync-20261030150348/.cgitsync/.memory", "previous_repo_lifecycle_state": "DECLARED", "repo_lifecycle_state": "FALLBACK_READY", "previous_sync_state": "PENDING", "sync_state": "FALLBACK_APPLIED", "current_ref_kind": "branch", "current_ref_name": "main", "target_ref_kind": "branch", "target_ref_name": "ComplexGitSync_ComplexGitSync", "resolved_ref_kind": "branch", "resolved_ref_name": "main", "commit_sha": "ee601f22905339e51f02c87d95eb437b27ea59f3", "fallback_branch": "main", "fallback_reason": "branch 'ComplexGitSync_ComplexGitSync' not found on remote; cloned 'main' instead"}
{"operation": "GT-CLONE", "event": "repo_state_transition", "repo_name": "DevSpec", "absolute_path": "/home/nflipo/.cgs/ComplexGitSync-20261030150348/.agent/.distant/dev-sync", "previous_repo_lifecycle_state": "DECLARED", "repo_lifecycle_state": "READY", "previous_sync_state": "PENDING", "sync_state": "ALIGNED", "current_ref_kind": "branch", "current_ref_name": "main", "target_ref_kind": "branch", "target_ref_name": "main", "resolved_ref_kind": "branch", "resolved_ref_name": "main", "commit_sha": "56540c7504f45a2e7bb2264a3ad3601caa02f959", "fallback_branch": "main","fallback_reason": null}
{"operation": "GT-CLONE", "event": "repo_state_transition", "repo_name": "DocSpec", "absolute_path": "/home/nflipo/.cgs/ComplexGitSync-20261030150348/.agent/.distant/documentation", "previous_repo_lifecycle_state": "DECLARED", "repo_lifecycle_state": "READY", "previous_sync_state": "PENDING", "sync_state": "ALIGNED", "current_ref_kind": "branch", "current_ref_name": "main", "target_ref_kind": "branch", "target_ref_name": "main", "resolved_ref_kind": "branch", "resolved_ref_name": "main", "commit_sha": "02ee0b1f8b0edd66501ec4a22af373c677d09f59", "fallback_branch": "main", "fallback_reason": null}
{"operation": "GT-CLONE", "event": "repo_state_transition", "repo_name": ".ticketing", "absolute_path": "/home/nflipo/.cgs/ComplexGitSync-20261030150348/.agent/.distant/ticket", "previous_repo_lifecycle_state": "DECLARED", "repo_lifecycle_state": "READY", "previous_sync_state": "PENDING", "sync_state": "ALIGNED", "current_ref_kind": "branch", "current_ref_name": "main", "target_ref_kind": "branch", "target_ref_name": "main", "resolved_ref_kind": "branch", "resolved_ref_name": "main", "commit_sha": "a471f2644742c6a19f14c6dcc81a7f810f52c44e", "fallback_branch": "main", "fallback_reason": null}
{"operation": "GT-CLONE", "event": "repo_state_transition", "repo_name": ".claude", "absolute_path": "/home/nflipo/.cgs/ComplexGitSync-20261030150348/.agent/.local/.claude", "previous_repo_lifecycle_state": "DECLARED", "repo_lifecycle_state": "READY", "previous_sync_state": "PENDING", "sync_state": "ALIGNED", "current_ref_kind": "branch", "current_ref_name": "ComplexGitSync", "target_ref_kind": "branch", "target_ref_name": "ComplexGitSync", "resolved_ref_kind": "branch", "resolved_ref_name": "ComplexGitSync", "commit_sha": "ce8b4dbd9cbdae68e2029d31e7aab271d9698f9a","fallback_branch": "main", "fallback_reason": null}
{"operation": "GT-CLONE", "event": "repo_state_transition", "repo_name": ".dev", "absolute_path": "/home/nflipo/.cgs/ComplexGitSync-20261030150348/.agent/.local/.dev", "previous_repo_lifecycle_state": "DECLARED", "repo_lifecycle_state": "READY", "previous_sync_state": "PENDING", "sync_state": "ALIGNED", "current_ref_kind": "branch", "current_ref_name": "ComplexGitSync", "target_ref_kind": "branch", "target_ref_name": "ComplexGitSync", "resolved_ref_kind": "branch", "resolved_ref_name": "ComplexGitSync", "commit_sha": "97566ea004a0e490164a4a828a89e643aaaa3216", "fallback_branch": "main", "fallback_reason": null}
{"operation": "GT-CLONE", "event": "repo_state_transition", "repo_name": ".localSpec", "absolute_path": "/home/nflipo/.cgs/ComplexGitSync-20261030150348/.agent/.local/.localSpec", "previous_repo_lifecycle_state": "DECLARED", "repo_lifecycle_state": "READY", "previous_sync_state": "PENDING", "sync_state": "ALIGNED", "current_ref_kind": "branch", "current_ref_name": "ComplexGitSync", "target_ref_kind": "branch", "target_ref_name": "ComplexGitSync", "resolved_ref_kind": "branch", "resolved_ref_name": "ComplexGitSync", "commit_sha": "5f02062b0781858b43a0a4f517ab9ae882c399bc", "fallback_branch": "main", "fallback_reason": null}
{"operation": "CGS-RUN", "event": "private_branch_missing", "repo": ".memory", "path": "/home/nflipo/.cgs/ComplexGitSync-20261030150348/.cgitsync/.memory", "wanted": "ComplexGitSync_ComplexGitSync", "landed": "main", "config": "config-memory.cgs", "command": "cgitsync memory branch --project-branch main", "project_branch": "main"}
{"operation": "CGS-RUN", "event": "gts_write", "snapshot_path": "/home/nflipo/.cgs/ComplexGitSync-20261030150348/.cgitsync/state/0bd7127bf4dce67b16bffca19628a6203a64654dcd0e02489d66e396b655495a.gts", "source_cgs_path": "/home/nflipo/APOUB/ComplexGitSync/examples/complexgitsync-dev.cgs", "tree_lifecycle_state": "READY"}
{"operation": "CGS-RUN", "event": "ledger_append", "register_path": "/home/nflipo/.cgs/ComplexGitSync-20261030150348/.cgitsync/lgr", "seq": 1, "state_id": "state(0bd7127bf4dce67b16bffca19628a6203a64654dcd0e02489d66e396b655495a)", "command": "clone"}
{"operation": "GT-CLONE", "event": "tree_state_transition", "previous_tree_state": "UNLOADED", "tree_lifecycle_state": "READY", "reason": "clone_cgs"}
READY ready=true complete=true gittree_created=true gittree_active=true root=/home/nflipo/.cgs/ComplexGitSync-20261030150348

To use this workspace, run:
  export CGSHOME=/home/nflipo/.cgs/ComplexGitSync-20261030150348

Or for the current command:
  CGSHOME=/home/nflipo/.cgs/ComplexGitSync-20261030150348 pixi run cgitsync <command>
warning: .memory has no branch 'ComplexGitSync_ComplexGitSync' yet, so it was cloned on 'main', which does not hold its config-memory.cgs. Do not commit to it there: a writable repository left on a fallback branch would write to that branch.
to create it, run: cgitsync memory branch --project-branch main
Run it now? (y/N) [n]: y
{"operation": "CGS-RUN", "event": "self_history_adopt", "mount": "/home/nflipo/.cgs/ComplexGitSync-20261030150348/.cgitsync/.memory/.self-history", "branch": "ComplexGitSync_ComplexGitSync"}
{"operation": "CGS-RUN", "event": "self_history_push", "mount": "/home/nflipo/.cgs/ComplexGitSync-20261030150348/.cgitsync/.memory/.self-history", "branch": "ComplexGitSync_ComplexGitSync", "committed": false}
{"operation": "CGS-MEM", "event": "memory_push", "mount": "/home/nflipo/.cgs/ComplexGitSync-20261030150348/.cgitsync/.memory", "branch": "ComplexGitSync_ComplexGitSync", "committed": true, "pushed": true}
{"operation": "CGS-MEM", "event": "memory_branch", "mount": "/home/nflipo/.cgs/ComplexGitSync-20261030150348/.cgitsync/.memory", "branch": "ComplexGitSync_ComplexGitSync", "created": true, "set_up": true}
branch=ComplexGitSync_ComplexGitSync set_up=yes pushed=yes
{"operation": "CGS-BOOTSTRAP", "event": "command_end", "command": "bootstrap", "status": "ok", "tree_lifecycle_state": "READY"}
log_file=/home/nflipo/.cgs/ComplexGitSync-20261030150348/.cgitsync/logs/clone-20261030T150429820782Z.log
nflipo@zagros-fon:~/APOUB/ComplexGitSync$ pixi run cgitsync status
cgshome=/home/nflipo/.cgs/ComplexGitSync-20261030093858 (from $CGSHOME) use_case=standalone
source=/home/nflipo/.cgs/ComplexGitSync-20261030093858/.cgitsync/state/012aba49cf46e383dcb60ee330cd80f96a7f7b86c0426a4d35c299acff64dcc4.gts (from ledger)
warning: CGSHOME (/home/nflipo/.cgs/ComplexGitSync-20261030093858) does not contain the current directory (/home/nflipo/APOUB/ComplexGitSync).
warning: $CGSHOME is set and outranks the current directory, so this command reads and writes that workspace, not this one. Run 'unset CGSHOME', or pass --search-dir /home/nflipo/APOUB/ComplexGitSync, to work here instead.
summary ready=true complete=true use_case=standalone profile=user cgitsync_branch=CGS-ALPHA repos=2 dirty=0 staged=0 ahead=0 behind=0 unmeasured=2 recorded_mismatch=0 errors=0
REPOSITORY         PATH  SCOPE    LOCAL_BRANCH  UPSTREAM_BRANCH  LOCAL  SYNC         HEAD      RECORDED
-------------------------------------------------------------------------------------------------------
DocComplexGitSync  docs  project  CGS-ALPHA     -                clean  no-upstream  ed83921b  ed83921b
ComplexGitSync     .     project  CGS-ALPHA     -                clean  no-upstream  5b0a120c  5b0a120c
warning: split branch 'docs/molonari-cgs-8-5-0' — ComplexGitSync: live; DocComplexGitSync: absent
info: closed branch 'alpha-tech' — ComplexGitSync: closed; DocComplexGitSync: absent
info: closed branch 'memory-dev' — ComplexGitSync: closed; DocComplexGitSync: closed
legend: SYNC — synced/ahead/behind/diverged are measured against the upstream branch; no-upstream = this branch was never pushed, so there is nothing to measure; unknown = it names an upstream that does not resolve, which 'cgitsync pull' or 'cgitsync push' repairs
READY ready=true complete=true gittree_created=true gittree_active=true

Then nflipo@zagros-fon:~/.cgs/ComplexGitSync-20261030150348$ pixi run cgitsync status
cgshome=/home/nflipo/.cgs/ComplexGitSync-20261030093858 (from $CGSHOME) use_case=standalone
source=/home/nflipo/.cgs/ComplexGitSync-20261030093858/.cgitsync/state/012aba49cf46e383dcb60ee330cd80f96a7f7b86c0426a4d35c299acff64dcc4.gts (from ledger)
warning: CGSHOME (/home/nflipo/.cgs/ComplexGitSync-20261030093858) does not contain the current directory (/home/nflipo/.cgs/ComplexGitSync-20261030150348).
warning: $CGSHOME is set and outranks the current directory, so this command reads and writes that workspace, not this one. Run 'unset CGSHOME', or pass --search-dir /home/nflipo/.cgs/ComplexGitSync-20261030150348, to work here instead.
summary ready=true complete=true use_case=standalone profile=user cgitsync_branch=CGS-ALPHA repos=2 dirty=0 staged=0 ahead=0 behind=0 unmeasured=2 recorded_mismatch=0 errors=0
REPOSITORY         PATH  SCOPE    LOCAL_BRANCH  UPSTREAM_BRANCH  LOCAL  SYNC         HEAD      RECORDED
-------------------------------------------------------------------------------------------------------
DocComplexGitSync  docs  project  CGS-ALPHA     -                clean  no-upstream  ed83921b  ed83921b
ComplexGitSync     .     project  CGS-ALPHA     -                clean  no-upstream  5b0a120c  5b0a120c
warning: split branch 'docs/molonari-cgs-8-5-0' — ComplexGitSync: live; DocComplexGitSync: absent
info: closed branch 'alpha-tech' — ComplexGitSync: closed; DocComplexGitSync: absent
info: closed branch 'memory-dev' — ComplexGitSync: closed; DocComplexGitSync: closed
legend: SYNC — synced/ahead/behind/diverged are measured against the upstream branch; no-upstream = this branch was never pushed, so there is nothing to measure; unknown = it names an upstream that does not resolve, which 'cgitsync pull' or 'cgitsync push' repairs
READY ready=true complete=true gittree_created=true gittree_active=true
nflipo@zagros-fon:~/.cgs/ComplexGitSync-20261030150348$ pixi run cgitsync fetch
cgshome=/home/nflipo/.cgs/ComplexGitSync-20261030093858 (from $CGSHOME) use_case=standalone
source=/home/nflipo/.cgs/ComplexGitSync-20261030093858/.cgitsync/state/012aba49cf46e383dcb60ee330cd80f96a7f7b86c0426a4d35c299acff64dcc4.gts (from ledger)
warning: CGSHOME (/home/nflipo/.cgs/ComplexGitSync-20261030093858) does not contain the current directory (/home/nflipo/.cgs/ComplexGitSync-20261030150348).
warning: $CGSHOME is set and outranks the current directory, so this command reads and writes that workspace, not this one. Run 'unset CGSHOME', or pass --search-dir /home/nflipo/.cgs/ComplexGitSync-20261030150348, to work here instead.
git_command=git fetch --prune origin
fetched ComplexGitSync: origin
fetched DocComplexGitSync: origin
fetched=2 skipped=0
nflipo@zagros-fon:~/.cgs/ComplexGitSync-20261030150348$ pixi run cgitsync status
cgshome=/home/nflipo/.cgs/ComplexGitSync-20261030093858 (from $CGSHOME) use_case=standalone
source=/home/nflipo/.cgs/ComplexGitSync-20261030093858/.cgitsync/state/012aba49cf46e383dcb60ee330cd80f96a7f7b86c0426a4d35c299acff64dcc4.gts (from ledger)
warning: CGSHOME (/home/nflipo/.cgs/ComplexGitSync-20261030093858) does not contain the current directory (/home/nflipo/.cgs/ComplexGitSync-20261030150348).
warning: $CGSHOME is set and outranks the current directory, so this command reads and writes that workspace, not this one. Run 'unset CGSHOME', or pass --search-dir /home/nflipo/.cgs/ComplexGitSync-20261030150348, to work here instead.
summary ready=true complete=true use_case=standalone profile=user cgitsync_branch=CGS-ALPHA repos=2 dirty=0 staged=0 ahead=0 behind=0 unmeasured=2 recorded_mismatch=0 errors=0
REPOSITORY         PATH  SCOPE    LOCAL_BRANCH  UPSTREAM_BRANCH  LOCAL  SYNC         HEAD      RECORDED
-------------------------------------------------------------------------------------------------------
DocComplexGitSync  docs  project  CGS-ALPHA     -                clean  no-upstream  ed83921b  ed83921b
ComplexGitSync     .     project  CGS-ALPHA     -                clean  no-upstream  5b0a120c  5b0a120c
warning: split branch 'docs/molonari-cgs-8-5-0' — ComplexGitSync: live; DocComplexGitSync: absent
info: closed branch 'alpha-tech' — ComplexGitSync: closed; DocComplexGitSync: absent
info: closed branch 'memory-dev' — ComplexGitSync: closed; DocComplexGitSync: closed
legend: SYNC — synced/ahead/behind/diverged are measured against the upstream branch; no-upstream = this branch was never pushed, so there is nothing to measure; unknown = it names an upstream that does not resolve, which 'cgitsync pull' or 'cgitsync push' repairs
READY ready=true complete=true gittree_created=true gittree_active=true
nflipo@zagros-fon:~/.cgs/ComplexGitSync-20261030150348$ pixi run cgitsync checkout CGS-ALPHA
cgshome=/home/nflipo/.cgs/ComplexGitSync-20261030093858 (from $CGSHOME) use_case=standalone
source=/home/nflipo/.cgs/ComplexGitSync-20261030093858/.cgitsync/state/012aba49cf46e383dcb60ee330cd80f96a7f7b86c0426a4d35c299acff64dcc4.gts (from ledger)
warning: CGSHOME (/home/nflipo/.cgs/ComplexGitSync-20261030093858) does not contain the current directory (/home/nflipo/.cgs/ComplexGitSync-20261030150348).
warning: $CGSHOME is set and outranks the current directory, so this command reads and writes that workspace, not this one. Run 'unset CGSHOME', or pass --search-dir /home/nflipo/.cgs/ComplexGitSync-20261030150348, to work here instead.
git_command=git checkout CGS-ALPHA
READY ready=true complete=true gittree_created=true gittree_active=true branch=CGS-ALPHA
repos:
ComplexGitSync (root) [ALIGNED] @5b0a120 br=CGS-ALPHA fb=main
└── DocComplexGitSync (leaf) [ALIGNED] @ed83921 br=CGS-ALPHA fb=main
log_file=/home/nflipo/.cgs/ComplexGitSync-20261030093858/.cgitsync/logs/checkout-20261030T161253783986Z.log
nflipo@zagros-fon:~/.cgs/ComplexGitSync-20261030150348$ pixi run cgitsync status
cgshome=/home/nflipo/.cgs/ComplexGitSync-20261030093858 (from $CGSHOME) use_case=standalone
source=/home/nflipo/.cgs/ComplexGitSync-20261030093858/.cgitsync/state/012aba49cf46e383dcb60ee330cd80f96a7f7b86c0426a4d35c299acff64dcc4.gts (from ledger)
warning: CGSHOME (/home/nflipo/.cgs/ComplexGitSync-20261030093858) does not contain the current directory (/home/nflipo/.cgs/ComplexGitSync-20261030150348).
warning: $CGSHOME is set and outranks the current directory, so this command reads and writes that workspace, not this one. Run 'unset CGSHOME', or pass --search-dir /home/nflipo/.cgs/ComplexGitSync-20261030150348, to work here instead.
summary ready=true complete=true use_case=standalone profile=user cgitsync_branch=CGS-ALPHA repos=2 dirty=0 staged=0 ahead=0 behind=0 unmeasured=2 recorded_mismatch=0 errors=0
REPOSITORY         PATH  SCOPE    LOCAL_BRANCH  UPSTREAM_BRANCH  LOCAL  SYNC         HEAD      RECORDED
-------------------------------------------------------------------------------------------------------
DocComplexGitSync  docs  project  CGS-ALPHA     -                clean  no-upstream  ed83921b  ed83921b
ComplexGitSync     .     project  CGS-ALPHA     -                clean  no-upstream  5b0a120c  5b0a120c
warning: split branch 'docs/molonari-cgs-8-5-0' — ComplexGitSync: live; DocComplexGitSync: absent
info: closed branch 'alpha-tech' — ComplexGitSync: closed; DocComplexGitSync: absent
info: closed branch 'memory-dev' — ComplexGitSync: closed; DocComplexGitSync: closed
legend: SYNC — synced/ahead/behind/diverged are measured against the upstream branch; no-upstream = this branch was never pushed, so there is nothing to measure; unknown = it names an upstream that does not resolve, which 'cgitsync pull' or 'cgitsync push' repairs
READY ready=true complete=true gittree_created=true gittree_active=true
nflipo@zagros-fon:~/.cgs/ComplexGitSync-20261030150348$ pixi run cgitsync branch --list
usage: cgitsync branch [-h] <subcommand> ...
cgitsync branch: error: the following arguments are required: <subcommand>
'branch --list' is now 'branch list'.
nflipo@zagros-fon:~/.cgs/ComplexGitSync-20261030150348$ pixi run cgitsync branchlist
usage: cgitsync [-h] [--version] <command> ...
cgitsync: error: argument command: invalid choice: 'branchlist' (choose from 'initialise', 'bootstrap', 'release', 'status', 'view-tree', 'validate', 'pull', 'fetch', 'autofix', 'checkout', 'branch', 'add', 'rm', 'commit', 'merge', 'push', 'tag', 'submodules', 'verify', 'memory', 'self-history', 'omniscience', 'discover', 'repo', 'env', 'unlock', 'help')
Did you mean 'branch'?
nflipo@zagros-fon:~/.cgs/ComplexGitSync-20261030150348$ pixi run cgitsync branch list
cgshome=/home/nflipo/.cgs/ComplexGitSync-20261030093858 (from $CGSHOME) use_case=standalone
source=/home/nflipo/.cgs/ComplexGitSync-20261030093858/.cgitsync/state/012aba49cf46e383dcb60ee330cd80f96a7f7b86c0426a4d35c299acff64dcc4.gts (from ledger)
warning: CGSHOME (/home/nflipo/.cgs/ComplexGitSync-20261030093858) does not contain the current directory (/home/nflipo/.cgs/ComplexGitSync-20261030150348).
warning: $CGSHOME is set and outranks the current directory, so this command reads and writes that workspace, not this one. Run 'unset CGSHOME', or pass --search-dir /home/nflipo/.cgs/ComplexGitSync-20261030150348, to work here instead.
git_command=git for-each-ref refs/heads refs/remotes/origin
cgitsync_branch=CGS-ALPHA  (origin as of the last fetch; cgitsync fetch refreshes it)
  8.5.0                    local          all 2 repositories
* CGS-ALPHA                local, origin  all 2 repositories
  docs/molonari-cgs-8-5-0  origin         missing in: DocComplexGitSync
  main                     local, origin  all 2 repositories
closed:
  alpha-tech               origin         closed/alpha-tech
  memory-dev               origin         closed/memory-dev
warning: split branch 'docs/molonari-cgs-8-5-0' — ComplexGitSync: live; DocComplexGitSync: absent
info: closed branch 'alpha-tech' — ComplexGitSync: closed; DocComplexGitSync: absent
info: closed branch 'memory-dev' — ComplexGitSync: closed; DocComplexGitSync: closed
nflipo@zagros-fon:~/.cgs/ComplexGitSync-20261030150348$ cd examples/
nflipo@zagros-fon:~/.cgs/ComplexGitSync-20261030150348/examples$ git rm complexgitsync4dev.cgs 
rm 'examples/complexgitsync4dev.cgs'
nflipo@zagros-fon:~/.cgs/ComplexGitSync-20261030150348/examples$ cp ~/APOUB/ComplexGitSync/examples/complexgitsync-* ./
nflipo@zagros-fon:~/.cgs/ComplexGitSync-20261030150348/examples$ pixi run cgitsync add 
cgshome=/home/nflipo/.cgs/ComplexGitSync-20261030093858 (from $CGSHOME) use_case=standalone
source=/home/nflipo/.cgs/ComplexGitSync-20261030093858/.cgitsync/state/012aba49cf46e383dcb60ee330cd80f96a7f7b86c0426a4d35c299acff64dcc4.gts (from ledger)
warning: CGSHOME (/home/nflipo/.cgs/ComplexGitSync-20261030093858) does not contain the current directory (/home/nflipo/.cgs/ComplexGitSync-20261030150348/examples).
warning: $CGSHOME is set and outranks the current directory, so this command reads and writes that workspace, not this one. Run 'unset CGSHOME', or pass --search-dir /home/nflipo/.cgs/ComplexGitSync-20261030150348/examples, to work here instead.
git_command=git add --all
skipped DocComplexGitSync: nothing to stage
skipped ComplexGitSync: nothing to stage
staged=0 skipped=2
note: no repository in scope had anything to stage. Check 'cgitsync status' for where your changes actually live, and add --private if they are in a private/local repository.
READY ready=true complete=true gittree_created=true gittree_active=true
repos:
ComplexGitSync (root) [ALIGNED] @5b0a120 br=CGS-ALPHA fb=main
└── DocComplexGitSync (leaf) [ALIGNED] @ed83921 br=CGS-ALPHA fb=main
nflipo@zagros-fon:~/.cgs/ComplexGitSync-20261030150348/examples$ pixi run cgitsync commit -m "cgitsync-8.5.0 work on standardisation of .cgs depending on X profile"
cgshome=/home/nflipo/.cgs/ComplexGitSync-20261030093858 (from $CGSHOME) use_case=standalone
source=/home/nflipo/.cgs/ComplexGitSync-20261030093858/.cgitsync/state/012aba49cf46e383dcb60ee330cd80f96a7f7b86c0426a4d35c299acff64dcc4.gts (from ledger)
warning: CGSHOME (/home/nflipo/.cgs/ComplexGitSync-20261030093858) does not contain the current directory (/home/nflipo/.cgs/ComplexGitSync-20261030150348/examples).
warning: $CGSHOME is set and outranks the current directory, so this command reads and writes that workspace, not this one. Run 'unset CGSHOME', or pass --search-dir /home/nflipo/.cgs/ComplexGitSync-20261030150348/examples, to work here instead.
git_command=git commit -m 'cgitsync-8.5.0 work on standardisation of .cgs depending on X profile'
skipped DocComplexGitSync: nothing staged
skipped ComplexGitSync: nothing staged
committed=0 skipped=2
note: no repository in scope had staged changes. Check 'cgitsync status' for where your changes actually live, and add --private if they are in a private/local repository.
READY ready=true complete=true gittree_created=true gittree_active=true message='cgitsync-8.5.0 work on standardisation of .cgs depending on X profile'
repos:
ComplexGitSync (root) [ALIGNED] @5b0a120 br=CGS-ALPHA fb=main
└── DocComplexGitSync (leaf) [ALIGNED] @ed83921 br=CGS-ALPHA fb=main
nflipo@zagros-fon:~/.cgs/ComplexGitSync-20261030150348/examples$ pixi run cgitsync push
cgshome=/home/nflipo/.cgs/ComplexGitSync-20261030093858 (from $CGSHOME) use_case=standalone
source=/home/nflipo/.cgs/ComplexGitSync-20261030093858/.cgitsync/state/012aba49cf46e383dcb60ee330cd80f96a7f7b86c0426a4d35c299acff64dcc4.gts (from ledger)
warning: CGSHOME (/home/nflipo/.cgs/ComplexGitSync-20261030093858) does not contain the current directory (/home/nflipo/.cgs/ComplexGitSync-20261030150348/examples).
warning: $CGSHOME is set and outranks the current directory, so this command reads and writes that workspace, not this one. Run 'unset CGSHOME', or pass --search-dir /home/nflipo/.cgs/ComplexGitSync-20261030150348/examples, to work here instead.
git_command=git push (-u origin <branch> when upstream is missing)
{"operation": "CGS-PUSH", "event": "command_end", "command": "push", "status": "error", "error": "push stopped part-way: Git command failed (git push -u origin CGS-ALPHA): To github.com:flipoyo/ComplexGitSync.git\n ! [rejected]        CGS-ALPHA -> CGS-ALPHA (non-fast-forward)\nerror: failed to push some refs to 'github.com:flipoyo/ComplexGitSync.git'\nhint: Updates were rejectedbecause the tip of your current branch is behind\nhint: its remote counterpart. Integrate the remote changes (e.g.\nhint: 'git pull ...') before pushing again.\nhint: See the 'Note about fast-forwards' in 'git push --help' for details.\ncompleted: DocComplexGitSync (docs) (origin/CGS-ALPHA (upstream set))\nfailed: ComplexGitSync (.)\nnot attempted: none\nNothing was rolled back and no State was recorded. Once the cause is fixed, run 'cgitsync push' again: what completed is not repeated.", "tree_lifecycle_state": "READY"}
log_file=/home/nflipo/.cgs/ComplexGitSync-20261030093858/.cgitsync/logs/push-20261030T162108Z.log
cgitsync push: push stopped part-way: Git command failed (git push -u origin CGS-ALPHA): To github.com:flipoyo/ComplexGitSync.git
 ! [rejected]        CGS-ALPHA -> CGS-ALPHA (non-fast-forward)
error: failed to push some refs to 'github.com:flipoyo/ComplexGitSync.git'
hint: Updates were rejected because the tip of your current branch is behind
hint: its remote counterpart. Integrate the remote changes (e.g.
hint: 'git pull ...') before pushing again.
hint: See the 'Note about fast-forwards' in 'git push --help' for details.
completed: DocComplexGitSync (docs) (origin/CGS-ALPHA (upstream set))
failed: ComplexGitSync (.)
not attempted: none
Nothing was rolled back and no State was recorded. Once the cause is fixed, run 'cgitsync push' again: what completed is not repeated.
nflipo@zagros-fon:~/.cgs/ComplexGitSync-20261030150348/examples$ pixi run cgitsync status
cgshome=/home/nflipo/.cgs/ComplexGitSync-20261030093858 (from $CGSHOME) use_case=standalone
source=/home/nflipo/.cgs/ComplexGitSync-20261030093858/.cgitsync/state/012aba49cf46e383dcb60ee330cd80f96a7f7b86c0426a4d35c299acff64dcc4.gts (from ledger)
warning: CGSHOME (/home/nflipo/.cgs/ComplexGitSync-20261030093858) does not contain the current directory (/home/nflipo/.cgs/ComplexGitSync-20261030150348/examples).
warning: $CGSHOME is set and outranks the current directory, so this command reads and writes that workspace, not this one. Run 'unset CGSHOME', or pass --search-dir /home/nflipo/.cgs/ComplexGitSync-20261030150348/examples, to work here instead.
summary ready=true complete=true use_case=standalone profile=user cgitsync_branch=CGS-ALPHA repos=2 dirty=0 staged=0 ahead=0 behind=0 unmeasured=1 recorded_mismatch=0 errors=0
REPOSITORY         PATH  SCOPE    LOCAL_BRANCH  UPSTREAM_BRANCH   LOCAL  SYNC         HEAD      RECORDED
--------------------------------------------------------------------------------------------------------
DocComplexGitSync  docs  project  CGS-ALPHA     origin/CGS-ALPHA  clean  synced       ed83921b  ed83921b
ComplexGitSync     .     project  CGS-ALPHA     -                 clean  no-upstream  5b0a120c  5b0a120c
warning: split branch 'docs/molonari-cgs-8-5-0' — ComplexGitSync: live; DocComplexGitSync: absent
info: closed branch 'alpha-tech' — ComplexGitSync: closed; DocComplexGitSync: absent
info: closed branch 'memory-dev' — ComplexGitSync: closed; DocComplexGitSync: closed
legend: SYNC — synced/ahead/behind/diverged are measured against the upstream branch; no-upstream = this branch was never pushed, so there is nothing to measure; unknown = it names an upstream that does not resolve, which 'cgitsync pull' or 'cgitsync push' repairs
READY ready=true complete=true gittree_created=true gittree_active=true


DevPlanTicket for no-upstream fixing.
