#!/bin/bash

DISK1=$1
DISK2=$2

STEM1=/mnt/$DISK1/gsbuser/EoR
STEM2=/mnt/$DISK2/gsbuser/EoR

FILE=$3

for node in node{111..118}
  do
  ssh -n $node "for num in {0..16}; do ln -s $STEM1/$FILE.node\$num $STEM2/$FILE.node\$num; done"
done