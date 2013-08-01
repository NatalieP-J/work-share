from sequence_functions import GenTimestamps
import sys

source = int(sys.argv[1])

if source == 0:
	START='Fri Jul 26 20:30:00 UTC 2013'
	END=5760
	STAMPID='_July26_1810'
	GenTimestamps(START,END,STAMPID)

if source == 1:
	START='Fri Jul 26 22:11:00 UTC 2013'
	END=720
	STAMPID='_July26_1919'
	GenTimestamps(START,END,STAMPID)

if source == 2:
	START='Fri Jul 26 22:31:00 UTC 2013'
	END=600
	STAMPID='_July26_1957'
	GenTimestamps(START,END,STAMPID)

if source == 3:
	START='Sat Jul 27 20:54:00 UTC 2013'
	END=4080
	STAMPID='_July27_1810'
	GenTimestamps(START,END,STAMPID)

if source == 4:
	START='Sat Jul 27 22:05:00 UTC 2013'
	END=840
	STAMPID='_July27_1919'
	GenTimestamps(START,END,STAMPID)

if source == 5:
	START='Sat Jul 27 22:26:00 UTC 2013'
	END=2040
	STAMPID='_July27_2111'
	GenTimestamps(START,END,STAMPID)


