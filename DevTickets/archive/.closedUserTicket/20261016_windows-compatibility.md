i have a windows user who reported that ~/.cgs is not accessible through its bash prompt. This is a bug for the windows compatibility. He also had to use \\ at some point in the terminal when doing tuto1. This is a compatibility issue with windows. The CLI should be linux-like only as long as the export CGSHOME="linux-format" worked in a windows prompt. 

Message from the user :
"
 les ~ ne fonctionnent pas, il faut mettre les chemins en entier

 Pour certaines commandes il faut aussi mettre des \\ sinon le terminal comprend \ comme un espace"


Report where windows may not work, for that you can try to execute the corrected tutos in a windows virtual machine.