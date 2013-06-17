import numpy as np
from astropy.time import Time
import manage as man
import sys

def LoadData(fname):
    f=open(fname,'r')
    data=[]
    for line in f.readlines():
        data.append(line.split('\n'))
    f.close()
    return data

toa_name=sys.argv[1] #Name of arrival times file
times=LoadData(toa_name)
times=man.IterativeStrAppend(times,0)
start=Time(times[0],format='iso',scale='utc').mjd
toa=Time(times,format='iso',scale='utc').mjd
#Take a smaller sample to test code
toa=toa[:100]

#create testing t
t=[]
i=0
while i < 200:
    point=(0.0005*i)
    point=point/(60*60*24)
    point=point+start
    t.append(point)
    i+=1 

phase=[]
for j in range(len(t)):
    for i in range(len(toa)-1):
        if t[j] > toa[i]:
            period=(toa[i+1]-toa[i])/1000
            iphase=(16*((t[j]-toa[i])/period))%16
            phase.append(iphase)
