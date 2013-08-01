#!/bin/sh -x

#START='Fri Jul 26 20:30:00 UTC 2013'
#END=5760
#STAMPID='_July26_1810'
#SOURCE=0

#START='Fri Jul 26 22:11:00 UTC 2013'
#END=720
#STAMPID='_July26_1919'
#SOURCE=1

#START='Fri Jul 26 22:31:00 UTC 2013'
#END=600
#STAMPID='_July26_1957'
#SOURCE=2

#START='Sat Jul 27 20:54:00 UTC 2013'
#END=4080
#STAMPID='_July27_1810'
#SOURCE=3

#START='Sat Jul 27 22:05:00 UTC 2013'
#END=840
#STAMPID='_July27_1919'
#SOURCE=4

START='Sat Jul 27 22:26:00 UTC 2013'
END=2040
STAMPID='_July27_2111'
SOURCE=5

mkdir TJDtimestamps
mkdir GSTtimestamps
mkdir FinalResults

python ~/work-share/VLBI/VLBI_delays.py $SOURCE
perl ~/work-share/UVWAuto/Timestamp/Convert/convert_timestamp.perl gentimestamp$STAMPID.dat > TJDtimestamps/times$STAMPID.dat
~/work-share/UVWAuto/tjd2gst/tjd2gst.x <TJDtimestamps/times$STAMPID.dat >GSTtimestamps/GSTtimes$STAMPID.dat
python ~/work-share/VLBI/uvwconvert.py GSTtimestamps/GSTtimes$STAMPID.dat FinalResults/VLBIdelays$STAMPID.dat $SOURCE
