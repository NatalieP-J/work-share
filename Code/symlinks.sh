#!/bin/sh -x                                                                                                                                                                      
#By Natalie Price-Jones Aug 2 2013
#Recommend double checking all paths and the list of valid disks (called valid_disks) in DISKS_check.py before running this script
#requires password input 3 times if run from node111

#This script locates all .node[0-15] across all nodes and on each node either moves or symbolic links them to a specified disk.
#Cases currently accounted for: both node files missing (breaks with an error messages), one nodes file missing, or both node files present


FILE=b2016+28_Aug16_21.node #should be whatever is used to identify files during an 'ls' search
NAME=b2016+28_Aug16_21 #full part of the file name preceding the .node
SCAN=_21.node #format _[scan number].node is required
STEM=/mnt/*/gsbuser/TSAS/node* #location of files used to identify them during an 'ls' search
DISKOUT=disk2 #disk the files should be linked to
PATHOUT=/mnt/$DISKOUT/gsbuser/TSAS #used to double check that all symlinks are present

#list the files at their existing locations and write them into a file to be read by the python script
for ((i=111;i<119;i++));
do
ssh node$i "ls $STEM/*$FILE* | sed -e "s:.*mnt/:$i-:" -e "s:/gsbuser.*$SCAN:-:" | grep -v ".*fs0" | grep -v ".*norm" >> /mnt/software/gsbuser/TSAS/TSAS_FS/RUN/symlinks/disks$NAME.dat";
done

#for each node, read in the file containing location information and deal with the file according to a set of cases
for ((i=111;i<119;i++));
do
ssh node$i "python /mnt/software/gsbuser/TSAS/TSAS_FS/RUN/symlinks/DISKS_check.py /mnt/software/gsbuser/TSAS/TSAS_FS/RUN/symlinks/disks$NAME.dat $DISKOUT $NAME $i"
done

rm /mnt/software/gsbuser/TSAS/TSAS_FS/RUN/symlinks/disks$NAME.dat

#now list the files are the desired location to confirm things worked
for ((i=111;i<119;i++));
do 
ssh node$i "ls $PATHOUT/*$FILE* -lthr"
done
