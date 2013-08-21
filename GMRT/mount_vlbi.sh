ssh node33 "umount /mnt/vlbia; 
umount /mnt/vlbib; 
umount /mnt/vlbic; 
umount /mnt/vlbid;
mount /dev/sdc1 /mnt/vlbia;
mount /dev/sdd1 /mnt/vlbib;
mount /dev/sde1 /mnt/vlbic;
mount /dev/sdf1 /mnt/vlbid"
ssh node34 "umount /mnt/vlbia;
umount /mnt/vlbib;
umount /mnt/vlbic;
umount /mnt/vlbid;
mount /dev/sde2 /mnt/vlbia;
mount /dev/sdf2 /mnt/vlbib;
mount /dev/sdc2 /mnt/vlbic;
mount /dev/sdd2 /mnt/vlbid"
ssh node35 "umount /mnt/vlbia;
umount /mnt/vlbib;
umount /mnt/vlbic;
umount /mnt/vlbid;
mount /dev/sdc1 /mnt/vlbia;
mount /dev/sdd1 /mnt/vlbib;
mount /dev/sde1 /mnt/vlbic;
mount /dev/sdf1 /mnt/vlbid"
ssh node36 "umount /mnt/vlbia;
umount /mnt/vlbib;
umount /mnt/vlbic;
umount /mnt/vlbid;
mount /dev/sdb1 /mnt/vlbia;
mount /dev/sdc1 /mnt/vlbib;
mount /dev/sdd1 /mnt/vlbic;
mount /dev/sde1 /mnt/vlbid"
ssh node37 "umount /mnt/vlbia;
umount /mnt/vlbib;
umount /mnt/vlbic;
umount /mnt/vlbid;
mount /dev/sdc1 /mnt/vlbia;
mount /dev/sdd1 /mnt/vlbib;
mount /dev/sde1 /mnt/vlbic;
mount /dev/sdf1 /mnt/vlbid"
ssh node38 "umount /mnt/vlbia;
umount /mnt/vlbib;
umount /mnt/vlbic;
umount /mnt/vlbid;
mount /dev/sde3 /mnt/vlbia;
mount /dev/sdf3 /mnt/vlbib;
mount /dev/sdc3 /mnt/vlbic;
mount /dev/sdd3 /mnt/vlbid"
ssh node40 "umount /mnt/vlbia;
umount /mnt/vlbib;
umount /mnt/vlbic;
umount /mnt/vlbid;
mount /dev/sda3 /mnt/vlbia;
mount /dev/sdb3 /mnt/vlbib;
mount /dev/sdc3 /mnt/vlbic;
mount /dev/sdd3 /mnt/vlbid"
ssh node45 "umount /mnt/vlbia;
umount /mnt/vlbib;
umount /mnt/vlbic;
umount /mnt/vlbid;
mount /dev/sde2 /mnt/vlbia;
mount /dev/sdb2 /mnt/vlbib;
mount /dev/sdc2 /mnt/vlbic;
mount /dev/sdd2 /mnt/vlbid"
ssh node46 "umount /mnt/vlbia;
umount /mnt/vlbib;
umount /mnt/vlbic;
umount /mnt/vlbid;
mount /dev/sde2 /mnt/vlbia;
mount /dev/sdb2 /mnt/vlbib;
mount /dev/sdc2 /mnt/vlbic;
mount /dev/sdd2 /mnt/vlbid"
ssh node47 "umount /mnt/vlbia;
umount /mnt/vlbib;
umount /mnt/vlbic;
umount /mnt/vlbid;
mount /dev/sda2 /mnt/vlbia;
mount /dev/sdb2 /mnt/vlbib;
mount /dev/sdc2 /mnt/vlbic;
mount /dev/sdd2 /mnt/vlbid"
ssh node48 "umount /mnt/vlbia;
umount /mnt/vlbib;
umount /mnt/vlbic;
umount /mnt/vlbid;
mount /dev/sda3 /mnt/vlbia;
mount /dev/sdb3 /mnt/vlbib;
mount /dev/sdc3 /mnt/vlbic;
mount /dev/sdd3 /mnt/vlbid"
for ((i=33;i<51;i++)); do echo $i; ssh node$i "df -h";done