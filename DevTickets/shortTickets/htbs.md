HydrologicalTwinBetaSeries first Specs. Based on htas, cgs, and a cawaqs pipeline.  htas should be centered on its hypercube only not the .bin coming from cawaqs output. This is wrong because depends on the forward model of the pipeline.

htas protects the hypercube of state variables read from the current .bin. They should appear explicitly in their class state variables and hypercubes. 

Then htbs will be based on htas and its classes taking as inputs fwdModel outputs. This is a data type of a fwd model. The reading of it for filling up the hypercubes belong to the data class method, the data class being of type of the fwd model. 

htbs will add an invariant data class that holds the description of the boundary conditions and parameters necessary for running a pipeline. Their format are the cawaqs ones. Neuman boundary conditions are flux forcings (rainfall, etp, upstream discharge for river network that are at the frontier, same for aquifer unit (layer) boundary, as well as withdrawals in river and aquifer units) We may have DIRICHLET and CAUCHY BC at the frontiers or on river cells for aquifer units alone. The parameters invariant are the cawaqs ones.

a pipeline will contain the forward model gitrepo hash (SemVer), it will generate with a pre-processing the input-data and the fwd model CMD file, run the compiled fwdModel on it and generate output DATA. Those output data are for now the htas .bin inputs. For htbs the input will be a fwdmodel output DATA Repo

htbs is a project dependent on cgitsync. it couples operating spaces, such as htas, pipeline (fwd model for the POC), DATA invariant. The first use of the pipeline is from invariant DATA, a compiled fwdModel (cawaqs for the POC and its pre-proc) to resimulate bit-bit the fwdModel OUTPUT DATA that are provided  as an input of htas. Once it is proven, htbs is ALIVE, ALPHA otherwise

Project required: github.com:flipoyo/complexGitSync branch HT-BETA
github.com:flipoyo/HydrologicalTwinAlphaSeries branch HT-BETA
gitlab.com:cawaqs/cawaqs branch HT-BETA
First Twin to comme in gitlab.com:htas1/ht-synthcase-1 which holds cawaqs/gtest/testcases

Overall structure with OperatingSpaces (OSp) of order1 inspired by github.com:flipoyo/MOLONARI1D branch CGS-MOLO
Incoming coupling with gitlab.com:cawaqs/gviz/cawaqsviz for serving fwdModel output and protecting the data and the hypercube with htas deployed on a GATE not directly accessible by the client where cawaqsviz is running (ie independent server)




