import manage as man
from astropy.time import Time
import numpy as np
def WriteFile(values,fname):
    with open(fname,"w") as data:
        for i in range(len(values)):
            data.write("{0}\t{1}\n".format(values[i][1],values[i][0]))
def Differences(values,index):
    new_list=[]
    i=0
    while i < (len(values)-1):
        point=values[i+1][index]-values[i][index]
        new_list.append(point)
        i+=1
    return new_list
masterlist=[]
nanoseconds=15.
samples=2.**24
rate=(nanoseconds/10**9)*samples
n=33
while n<49:
    mastertime=[]
    i=1
    while i<5:
        fname='node{0}/timestamp_voltage.all.0329_june29.{1}.dat'.format(n,i)
        try:
            times=man.LoadData(fname)
            year=man.IterativeIntAppend(times,0)
            month=man.IterativeIntAppend(times,1)
            day=man.IterativeIntAppend(times,2)
            hour=man.IterativeIntAppend(times,3)
            minute=man.IterativeIntAppend(times,4)
            seconds=man.IterativeIntAppend(times,5)
            frac=man.IterativeFloatAppend(times,6)

            time=[]
            for j in range(len(times)):
                point=(day[j]*3600*24)+(hour[j]*3600)+(minute[j]*60)+(seconds[j])+(frac[j])
                time.append(point)
            for j in range(len(time)):
                point=[time[j],i-1]
                mastertime.append(point)
                pt=[time[j],i-1,n-33]
                masterlist.append(pt)
            print "Done node{0}/timestamp_voltage.all.0329_june29.{1}.dat".format(n,i)
            i+=1 
        except IOError:
            print "Missing node{0}/timestamp_voltage.all.0329_june29.{1}.dat".format(n,i)
            i+=1
            pass
        
    mastertime.sort()   

    #check=Differences(mastertime,0)
    #while j < len(check):
        #point=np.around(check[j],decimals=1)
        #if point==0:
            #mastertime.pop(j-1)
            #print 'Removed duplicate time at location {0}'.format(j-1)
        #j+=1

    name='node{0}/SequencedTimeStamp.dat'.format(n)
    WriteFile(mastertime,name)
    print 'Done sequenced time stamp node{0}'.format(n)
    n+=1
pts=[]
check=Differences(masterlist,0)
for i in range(len(check)):
    point=check[i]-rate
    pts.append(point)
    
