#!/bin/sh -x
FILE=b0329+54_Aug22_4
STEM=/mnt/*/gsbuser/TSAS/node*
DISKOUT=disk3
PATHOUT=/mnt/$DISKOUT/gsbuser/TSAS/

for ((i=111;i<119;i++));
do ssh node$i "ls $STEM/$FILE";
done
