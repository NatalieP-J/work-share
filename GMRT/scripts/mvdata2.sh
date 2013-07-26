#!/bin/sh -x

name=$(echo $1 | d s=/=_=g) 
echo Session name: $name

#Transfer data from nodes 33-49 to nodes 111-118, each in its own screen
screen -d -m -S $name
#screen -S $name zombie qr

screen -S $name -X screen scp -pr -c blowfish 192.168.17.33:$1.node0 192.168.17.33:$1.node0.norm $2
screen -S $name -X screen scp -pr -c blowfish 192.168.17.41:$1.node8 192.168.17.41:$1.node8.norm $3

for ((i=112 ; i<119 ; i++)) ; do
    screen -S $name -X screen ssh node$i "scp -pr -c blowfish node$((i-78)):$1.node$((i-33-78)) node$((i-78)):$1.node$((i-33-78)).norm $2" 
    screen -S $name -X screen ssh node$i "scp -pr -c blowfish node$((i-70)):$1.node$((i-33-70)) node$((i-70)):$1.node$((i-33-70)).norm $3" 
done

#screen -S $name -X screen ssh  node118 "scp -pr -c blowfish 192.168.17.49:$1.node15 192.168.17.49:$1.node15.norm $3"