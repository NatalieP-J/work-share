#!/bin/sh -x

#scp -pr -c blowfish 192.168.17.33:$1.node0 192.168.17.33:$1.node0.norm $2
#screen -S $name -X screen scp -pr -c blowfish 192.168.17.41:$1.node8 192.168.17.41:$1.node8.norm $3

for ((i=33 ; i<49 ; i++)) ; do
    ssh node$i " scp -pr -c blowfish /mnt/EoR[abcd]/jroy/timestamp_voltage* /mnt/code/gsbuser/panli19" 
done

#screen -S $name -X screen ssh  node118 "scp -pr -c blowfish 192.168.17.49:$1.node15 192.168.17.49:$1.node15.norm $3"
