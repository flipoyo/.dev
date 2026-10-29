Graph (G) Mounting Ergonomy - PoE
G{NAME,NODE,EDGE,OP} - CORR OP not OP*. G->*G is automatically synchronised with the results of OP.isPoE. OP* is OP.poe if and only if OP.isPoE is TRUE 
System protocol

.PUBLIC, PoE {1,1,1,1} Sigma=4
VOID

.USER=.USER-PUBLIC, PoE {1,1,0,0} Sigma=2
> git clone GitRepo-G
> cd $G-NAME
> git clone GitRepo-ComplexGitSync
> cd ComplexGitSync 
> pixi run cgitsync initialise install.cgs



.DEV=.DEV-LOCAL, PoE {1,0,0,0} Sigma=1
Same as .USER 
> pixi run cgitsync bootstrap $HOME/.cgs/$G-NAME/$G-NAME-dev.cgs


.OPX=.OPX-DISTANT, PoE {0,0,0,0} Sigma=0
Same as .USER 
> pixi run cgitsync bootstrap $HOME/.cgs/$G-NAME/$G-NAME-opx.cgs


From this protocol DevPlanTicket for gx4g-main MemoryMount
G.PoE-->G*

---

## Closed 2026-10-29: turned into a plan

Planned as `openTickets/gx4g-main_1-1_MemoryMount_DevPlanTicket.md` (owner, through `AskUserQuestion`: filed
here under a new prefix `gx4g-main_`; the PoE vector is what a level exposes; the scope is the whole install
protocol plus the class `OP` as ComplexGitSync's boundary class, to test CGS-ALPHA under internal requests from G
and external requests from GX4G). The owner's words above are unchanged.
