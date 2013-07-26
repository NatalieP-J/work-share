#!/bin/sh -x                                                                                                                                                                      
FILE=*Aug22_5.node*
NAME=3c84b_Aug22_5
SCAN=_5.node
STEM=/mnt/*/gsbuser/TSAS/node*
DISKOUT=disk3
PATHOUT=/mnt/$DISKOUT/TSAS

rm /mnt/software/gsbuser/EoR/Fringestop/disks_$NAME.dat

for ((i=111;i<119;i++));
do
ssh node$i "ls $STEM/$FILE | sed -e "s:.*mnt/:$i-:" -e "s:/gsbuser.*$SCAN:-:" | grep -v ".*fs0" | grep -v ".*norm" >> /mnt/software/gsbuser/TSAS/TSAS_FS/RUN/symlinks/disks_$NAME.dat";
done

python /mnt/software/gsbuser/TSAS/TSAS_FS/RUN/symlinks/disk_check.py /mnt/software/gsbuser/TSAS/TSAS_FS/RUN/symlinks/disks_$NAME.dat $DISKOUT $NAME

for ((i=111;i<119;i++));
do 
ssh node$i "ls $PATHOUT/$FILE -lthr"
done