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
#create an empty list to store timestamps in
masterlist=[]
#define the rate at which timestamps should appear
nanoseconds=15.
samples=2.**24
rate=(nanoseconds/10**9)*samples
#begin outer loop at node33 to be looped over all nodes up to node48
n=33
while n<49:
#node34's clock was off by about 14 minutes, need to boot it forward to 
#match the other sequence values
    if n == 34:
#node34 timestamp's are increased by the difference between its first entry and
#node33's first entry(which is nearly the same as the first entry for all other
#node timestamp files - see each node's MasterTimeStamp.dat file)
#node34 follows the same procedure as the others, with extra time added
        mastertime=[]
#within node34, extract the times from every timestamp file
        i=1
        while i<5:
#identifies the name of each timestamp file within a given node's 
#directory
            fname='node{0}/timestamp_voltage.all.0329_june29.{1}.dat'.format(n,i)
#if fname points to a real file, extract the times
            try:
                times=man.LoadData(fname)
                #year=man.IterativeIntAppend(times,0) irrelevant for our purpose
                #month=man.IterativeIntAppend(times,1)
#include day to account for possibility of observations spanning a transition 
#between days
                day=man.IterativeIntAppend(times,2) 
                hour=man.IterativeIntAppend(times,3)
                minute=man.IterativeIntAppend(times,4)
                seconds=man.IterativeIntAppend(times,5)
                frac=man.IterativeFloatAppend(times,6) #fraction of second

                time=[] #create empty list for times from each timestamp file
                for j in range(len(times)):
#point is in seconds, and has no real meaning as a time measurment - it is only
#the difference that concerns us in this instance
                    point=(day[j]*3600*24)+(hour[j]*3600)+(minute[j]*60)+(seconds[j])+(frac[j])+799.67499
                    time.append(point)
                for j in range(len(time)):
#add the time and the disk to which it was written (timestamp number minus 1) 
#to the masterlist within the node
                    point=[time[j],i-1]
                    mastertime.append(point)
#add the time, disk and the node on which it was written to the masterlist
                    pt=[time[j],i-1,n-33]
                    masterlist.append(pt)
#print a status update to screen and go to the next timestamp
                print "Done node{0}/timestamp_voltage.all.0329_june29.{1}.dat".format(n,i)
                i+=1 
#if a timestamp file is missing, report it and go to the next one
            except IOError:
                print "Missing node{0}/timestamp_voltage.all.0329_june29.{1}.dat".format(n,i)
                i+=1
                pass

#sort the file within the node to be in chronological order                
            mastertime.sort() 
#check that the sort worked by making sure that there are no negative values in
#the consecutive differences in the sorted list
            check=Differences(mastertime,0)
            for j in range(len(check)):
                if check[j]<0:
                    print 'Sort failed'
                else:
                    pass
#name the file that will result and put it in the appropriate node direactory
        #name='node{0}/SequencedTimeStamp.dat'.format(n)
        #WriteFileCols(mastertime,name)
#print another status update to screen
        print 'Done sequenced time stamp node{0}'.format(n)
        n+=1   

#if the node number is not 34, the timestamps begin at the same time
    else:
        mastertime=[]
#within node, extract the times from every timestamp file
        i=1
        while i<5:
#identifies the name of each timestamp file within a given node's 
#directory
            fname='node{0}/timestamp_voltage.all.0329_june29.{1}.dat'.format(n,i)
#if fname points to a real file, extract the times
            try:
                times=man.LoadData(fname)
                #year=man.IterativeIntAppend(times,0) irrelevant for our purpose
                #month=man.IterativeIntAppend(times,1)
#include day to account for possibility of observations spanning a transition 
#between days
                day=man.IterativeIntAppend(times,2) 
                hour=man.IterativeIntAppend(times,3)
                minute=man.IterativeIntAppend(times,4)
                seconds=man.IterativeIntAppend(times,5)
                frac=man.IterativeFloatAppend(times,6) #fraction of second

                time=[] #create empty list for times from each timestamp file
                for j in range(len(times)):
#point is in seconds, and has no real meaning as a time measurment - it is only
#the difference that concerns us in this instance
                    point=(day[j]*3600*24)+(hour[j]*3600)+(minute[j]*60)+(seconds[j])+(frac[j])
                    time.append(point)
                for j in range(len(time)):
#add the time and the disk to which it was written (timestamp number minus 1) 
#to the masterlist within the node
                    point=[time[j],i-1]
                    mastertime.append(point)
#add the time, disk and the node on which it was written to the masterlist
                    pt=[time[j],i-1,n-33]
                    masterlist.append(pt)
#print a status update to screen and go to the next timestamp
                print "Done node{0}/timestamp_voltage.all.0329_june29.{1}.dat".format(n,i)
                i+=1 
#if a timestamp file is missing, report it and go to the next one
            except IOError:
                print "Missing node{0}/timestamp_voltage.all.0329_june29.{1}.dat".format(n,i)
                i+=1
                pass

#sort the file within the node to be in chronological order                
            mastertime.sort() 
#check that the sort worked by making sure that there are no negative values in
#the consecutive differences in the sorted list
            check=Differences(mastertime,0)
            for j in range(len(check)):
                if check[j]<0:
                    print 'Sort failed'
                else:
                    pass
#name the file that will result and put it in the appropriate node direactory
        #name='node{0}/SequencedTimeStamp.dat'.format(n)
        #WriteFileCols(mastertime,name)
#print another status update to screen
        print 'Done sequenced time stamp node{0}'.format(n)
        n+=1 
        
#sort the masterlist      
masterlist.sort()

duplicates=[' ']*len(masterlist)
        
stamp_number=[] #a list to store the timestamp identifiers 
j=2 #the timestamp identifier, beginning at two
# add the first timestamp identifier (since the intervals will be one less than
# the length of the masterlist)
stamp_number.append(int(j)) 
intervals=[]
#diagnostic indices that track how often the various if statments are satisfied
m=0
n=0
for i in range(len(masterlist)-1):
#calculate intervals between consecutive entries in the masterlist
    interval=masterlist[i+1][0]-masterlist[i][0]
    intervals.append(interval)
#if anywhere the difference between the consecutive entries is less than zero
#the sort failed: report it
    if interval < 0:
        print 'masterlist sort failed'
#if rounded values of the interval is zero, do not increment j - assign both 
#timestamps the same j value
    if np.around(interval,decimals=1) == 0:
        stamp_number.append(int(j))
#if they are from the same node, timestamps are duplicates - report it in the 
#duplicate list
        if masterlist[i+1][2]==masterlist[i][2]:
            duplicates[i]='duplicate'
            duplicates[i+1]='duplicate'
        m+=1
#if rounded value of the interval is not zero, increment j by the number of 
#times the interval is greater than the rate
    if np.around(interval,decimals=1) > 0:
        point=interval/rate
        point=np.around(point,decimals=0)
        j+=point
        stamp_number.append(int(j))
        n+=1

#print out diagnostic information

print '''Diagnostics:
\t Length of masterlist: {0}
\t Length of stamp_number: {1}
\t Length of intervals: {2}
\t Zero if statment was called {3} times
\t Greater than rate if statement was called {4} times
 '''.format(len(masterlist),len(stamp_number),len(intervals),int(m),int(n))

#add the stamp number to every entry in the masterlist
for i in range(len(masterlist)):
    masterlist[i].append(stamp_number[i])
    masterlist[i].append(duplicates[i])

#print sequence number, disk, and duplication (if applicable) to a file for each
#node, coordinating the stamp_number across all nodes
def WriteFile3Cols(values,fname):
    with open(fname,"w") as data:
        for i in range(len(values)):
            data.write("{0} {1} {2}\n".format(values[i][0],values[i][1],values[i][2]))
n=33
while n < 49:
    name='node{0}/coordinated_generated_sequence.dat'.format(n)
    master=[]
    node=n-33
    for i in range(len(masterlist)):
        if masterlist[i][2] == node:
            point=[masterlist[i][3], masterlist[i][1], masterlist[i][4]]
            master.append(point)
    WriteFile3Cols(master,name)
    n+=1
#print the master sequence file, with sequence number, disk, node and 
#duplication (if applicable)
def WriteFile4Cols(values,fname):
    with open(fname,"w") as data:
        for i in range(len(values)):
            data.write("{0} {1} {2} {3}\n".format(values[i][0],values[i][1],values[i][2],values[i][3]))

name='MasterSequenceFile.dat'
master=[]
for i in range(len(masterlist)):
    point=[masterlist[i][3],masterlist[i][1],(masterlist[i][2]+33),masterlist[i][4]]
    master.append(point)
WriteFile4Cols(master,name)


            
