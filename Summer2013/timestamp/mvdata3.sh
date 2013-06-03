#!/bin/sh -x

#scp -pr -c blowfish 192.168.17.33:$1.node0 192.168.17.33:$1.node0.norm $2
#screen -S $name -X screen scp -pr -c blowfish 192.168.17.41:$1.node8 192.168.17.41:$1.node8.norm $3

for ((i=112 ; i<119 ; i++)) ; do
    ssh node$i "echo scp -pr -c blowfish node$((i-78)):$1 $2" 
    ssh node$i "echo scp -pr -c blowfish node$((i-70)):$1 $2" 
done

#screen -S $name -X screen ssh  node118 "scp -pr -c blowfish 192.168.17.49:$1.node15 192.168.17.49:$1.node15.norm $3"