While working on cawaqs release i found a few ergonomy bugs for cmd release. 1 the argument 'message' of release freeze is not writen in the TAGS message. 2. The TAGS mesage displayed on the GitProvider page is not fully readable - it should be a toml format. 3. The ergonomy of release load is not good. release load should behave as a bootstrap. If no --workspace NAME argument is given, it should keep the CGSHOME that is in memory to bootstrap and overwrite what is there. If --workspace NAME is defined, it should specify export CGSHOME="NAME" as it does in the stderr bootstrap message.

Tuto 3 should integrate how to load cawaqs-C363 release. Once loaded the user should go in $CGSHOME/src and launch 
./make_Cawaqs_from_branches.sh -b C363 .
which installs cawaqs3.63
