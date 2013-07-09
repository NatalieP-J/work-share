#!/bin/sh -x
MONTH=Aug
DATE=22
TARGET=b0329+54
DISKOUT=disk3
PATHOUT=/mnt/$DISKOUT/gsbuser/
for i in {111..118}
  j=i-78
  m=j-33
  for disk in {a,b,c,d,disk1,disk2,disk3,disk4}
    do ssh -n node$i "
    