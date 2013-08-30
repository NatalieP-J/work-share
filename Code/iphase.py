import numpy as np
from astropy.time import Time
import manage as man
import sys
from numpy.polynomial import Polynomial

#script that calculates iphase using a few different methods and compares them

def LoadData(fname):
    f=open(fname,'r')
    data=[]
    for line in f.readlines():
        data.append(line.replace('\n','').split('\t'))
    f.close()
    return data

def WriteFileCols(values1,values2,values3,fname):
    with open(fname,"w") as data:
        for i in range(len(values1)):
            data.write("{0} \t {1} \t {2} \n".format(values1[i],values2[i],values3[i]))

toa_name=sys.argv[1] #Name of arrival times file 
data=LoadData(toa_name) 
times=man.IterativeStrAppend(data,0)
start=Time(times[0],format='iso',scale='utc').mjd
toa=Time(times,format='iso',scale='utc').mjd
#Take a smaller sample to test code
toa=toa[:100]

f_0=1./float(data[0][1])
f_e=1./float(data[len(data)-1][1])
total_time=toa[len(toa)-1]-toa[0]
time_passed=total_time*60*60*24
f_dot=(f_0-f_e)/time_passed

#create a list of testing times t
t1=[]
i=0
while i < 200:
    point=(float(data[0][1])*i)
    point=point/(60*60*24)
    point=point+start
    t1.append(point)
    i+=1 

phase1=[]
for j in range(len(t1)):
    for i in range(len(toa)-1):
        if t1[j] > toa[i]:
            period=(toa[i+1]-toa[i])/1000
            #period=float(data[0][1])
            iphase=np.remainder((16*((t1[j]-toa[i])/period)),16)
            phase1.append(iphase)

t2=[]
i=0
while i < 200:
    point=(float(data[0][1])*i)
    t2.append(point)
    i+=1

phase2=[]
phasepol=Polynomial([f_0,f_dot]).integ(1,0.,0)
for i in range(len(t2)):
    phase=phasepol(t2[i])
    iphase=np.remainder(phase*16,16)
    phase2.append(iphase)

phase3=[]
phasepol=Polynomial([f_0]).integ(1,0,0)
for i in range(len(t2)):
    phase=phasepol(t2[i])
    iphase=np.remainder(phase*16,16)
    phase3.append(iphase)

name="RawResults.dat"
WriteFileCols(phase1,phase2,phase3,name)
print 'Wrote to {0}'.format(name)
