echo " "
echo "Usage : rename_at_all.csh  src_fname dest_fname dir"
echo "src file name : "$1;
echo "dest file name : "$2;
echo "target directory : "$3; 
echo " "
for ((i=17;i<27; i++)); do echo -n node${i}"  "; ssh node${i} "cd $3; pwd; mv $1 $2"; done 
echo "all done !"

