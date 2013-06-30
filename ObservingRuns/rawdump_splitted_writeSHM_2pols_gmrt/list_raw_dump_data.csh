for ((i=17;i<27; i++)); do echo -n node${i}"   "; ssh node${i} "ls -altr /mnt/raid0/jroy/raw_voltage.dat"; done
for ((i=17;i<27; i++)); do echo -n node${i}"   "; ssh node${i} "ls -altr /mnt/raid0/jroy/timestamp_voltage.dat"; done
echo "all done!"
