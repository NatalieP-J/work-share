import manage as man
from astropy.time import Time
import numpy as np
def WriteFileCols(values,fname):
    with open(fname,"w") as data:
        for i in range(len(values)):
            data.write("{0} {1}\n".format(values[i][0],values[i][1]))
def WriteFile3Cols(values,fname):
    with open(fname,"w") as data:
        for i in range(len(values)):
            data.write("{0} {1} {2}\n".format(values[i][0],values[i][1],values[i][2]))
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
    if n == 34:
        #right now, unsophisticated - just boots node34 forward ~ 14 minute so 
        #it matches everything else
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
                    point=(day[j]*3600*24)+(hour[j]*3600)+(minute[j]*60)+(seconds[j])+(frac[j])+799.67499
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
        name='node{0}/SequencedTimeStamp.dat'.format(n)
        WriteFileCols(mastertime,name)
        print 'Done sequenced time stamp node{0}'.format(n)
        n+=1   
    else:
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

        name='node{0}/SequencedTimeStamp.dat'.format(n)
        WriteFileCols(mastertime,name)
        print 'Done sequenced time stamp node{0}'.format(n)
        n+=1      
      
masterlist.sort()
        
stamp_number=[]
intervals=[]
rounded_nums=[]
j=2
stamp_number.append(int(j))
i=0
m=0
n=0
pts=[]
for i in range(len(masterlist)-1):
    interval=masterlist[i+1][0]-masterlist[i][0]
    intervals.append(interval)
    rounded=np.around(interval,decimals=1)
    rounded_nums.append(rounded)
for k in range(len(intervals)):
    if intervals[k] < 0:
        print 'Sort failed'
    if np.around(intervals[k],decimals=1) == 0:
        stamp_number.append(int(j))
        m+=1
    if np.around(intervals[k],decimals=1) > 0:
        point=interval/rate
        point=np.around(point,decimals=0)
        pts.append(point)
        j+=point
        stamp_number.append(int(j))
        n+=1

print '''Diagnostics:
\t Length of masterlist: {0}
\t Length of stamp_number: {1}
\t Length of intervals: {2}
\t Zero if statment was called {3} times
\t Greater than rate if statement was called {4} times
 '''.format(len(masterlist),len(stamp_number),len(intervals),int(m),int(n))

for i in range(len(masterlist)):
    masterlist[i].append(stamp_number[i])

n=33
while n < 49:
    name='node{0}/coordinated_generated_sequence.dat'.format(n)
    master=[]
    node=n-33
    for i in range(len(masterlist)):
        if masterlist[i][2] == node:
            point=[masterlist[i][3], masterlist[i][1]]
            master.append(point)
    WriteFileCols(master,name)
    n+=1

name='MasterSequenceFile.dat'
master=[]
for i in range(len(masterlist)):
    point=[masterlist[i][3],masterlist[i][1],(masterlist[i][2]+33)]
    master.append(point)
WriteFile3Cols(master,name)

            
