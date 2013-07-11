import manage as man
from astropy.time import Time
import numpy as np

#NODE34 is still 14 min early

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
masterlist_1919=[]
masterlist_1957=[]
masterlist_2016=[]
#define the rate at which timestamps should appear
nanoseconds=15.
samples=2.**24
rate=(nanoseconds/10**9)*samples
disk_type=['EoR','a_d']
#begin outer loop at node33 to be looped over all nodes up to node39
for d in range(len(disk_type)):
    n=33
    while n<40:
        if n == 34:
            mastertime_1919=[]
            mastertime_1957=[]
            mastertime_2016=[]
#within node, extract the times from every timestamp file
            i=1
            while i<5:
#identifies the name of each timestamp file within a given node's 
#directory
                fname='node{0}_july2/{1}/timestamp_voltage.all.1919_2_july2.{2}.dat'.format(n,disk_type[d],i)
#if fname points to a real file, extract the times
                try:
                    times=man.LoadData(fname)
                #year=man.IterativeIntAppend(times,0) irrelevant for our purpose
                #month=man.IterativeIntAppend(times,1)
#include day to account for possibility of observations spanning a transition 
#between days 
                    hour=man.IterativeIntAppend(times,3)
                    minute=man.IterativeIntAppend(times,4)
                    seconds=man.IterativeIntAppend(times,5)
                    frac=man.IterativeFloatAppend(times,6) #fraction of second

                    time=[] #create empty list for times from each timestamp file
                    for j in range(len(times)):
#point is in seconds, and has no real meaning as a time measurment - it is only
#the difference that concerns us in this instance
                        point=(hour[j]*3600)+(minute[j]*60)+(seconds[j])+(frac[j])+813.4349439999987
                        time.append(point)
                    for j in range(len(time)):
#add the time and the disk to which it was written (timestamp number minus 1) 
#to the masterlist within the node
                        point=[time[j],i-1,d]
                        pt=[time[j],i-1,n-33,d]
                        if 12120 <= time[j] <= 18600:
                            mastertime_1919.append(point)
                            masterlist_1919.append(pt)
                        if 18660 <= time[j] <= 25560:
                            mastertime_1957.append(point)
                            masterlist_1957.append(pt)
                        if 25680 <= time[j] <= 26400:
                            mastertime_2016.append(point)
                            masterlist_2016.append(pt)
#print a status update to screen and go to the next timestamp
                    print "Done node{0}_july2/timestamp_voltage.all.1919_2_july2.{1}.dat".format(n,i)
                    i+=1 
#if a timestamp file is missing, report it and go to the next one
                except IOError:
                    print "Missing node{0}_july2/timestamp_voltage.all.1919_2_july2.{1}.dat".format(n,i)
                    i+=1
                    pass
        
        else:
            mastertime_1919=[]
            mastertime_1957=[]
            mastertime_2016=[]
#within node, extract the times from every timestamp file
            i=1
            while i<5:
#identifies the name of each timestamp file within a given node's 
#directory
                fname='node{0}_july2/{1}/timestamp_voltage.all.1919_2_july2.{2}.dat'.format(n,disk_type[d],i)
#if fname points to a real file, extract the times
                try:
                    times=man.LoadData(fname)
                #year=man.IterativeIntAppend(times,0) irrelevant for our purpose
                #month=man.IterativeIntAppend(times,1)
#include day to account for possibility of observations spanning a transition 
#between days 
                    hour=man.IterativeIntAppend(times,3)
                    minute=man.IterativeIntAppend(times,4)
                    seconds=man.IterativeIntAppend(times,5)
                    frac=man.IterativeFloatAppend(times,6) #fraction of second

                    time=[] #create empty list for times from each timestamp file
                    for j in range(len(times)):
#point is in seconds, and has no real meaning as a time measurment - it is only
#the difference that concerns us in this instance
                        point=(hour[j]*3600)+(minute[j]*60)+(seconds[j])+(frac[j])
                        time.append(point)
                    for j in range(len(time)):
#add the time and the disk to which it was written (timestamp number minus 1) 
#to the masterlist within the node
                        point=[time[j],i-1,d]
                        pt=[time[j],i-1,n-33,d]
                        if 12120 <= time[j] <= 18600:
                            mastertime_1919.append(point)
                            masterlist_1919.append(pt)
                        if 18660 <= time[j] <= 25560:
                            mastertime_1957.append(point)
                            masterlist_1957.append(pt)
                        if 25680 <= time[j] <= 26400:
                            mastertime_2016.append(point)
                            masterlist_2016.append(pt)
#print a status update to screen and go to the next timestamp
                    print "Done node{0}_july2/timestamp_voltage.all.1919_2_july2.{1}.dat".format(n,i)
                    i+=1 
#if a timestamp file is missing, report it and go to the next one
                except IOError:
                    print "Missing node{0}_july2/timestamp_voltage.all.1919_2_july2.{1}.dat".format(n,i)
                    i+=1
                    pass

#sort the file within the node to be in chronological order                
            mastertime_1919.sort()
            mastertime_1957.sort()
            mastertime_2016.sort()

#name the file that will result and put it in the appropriate node direactory
        #name='node{0}/SequencedTimeStamp.dat'.format(n)
        #WriteFileCols(mastertime,name)
#print another status update to screen
        print 'Done sequenced time stamp node{0}'.format(n)
        n+=1 
        
#sort the masterlist      
masterlist_1919.sort()
masterlist_1957.sort()
masterlist_2016.sort()


duplicates=[' ']*len(masterlist_1919)
        
stamp_number=[] #a list to store the timestamp identifiers 
j=2 #the timestamp identifier, beginning at two
# add the first timestamp identifier (since the intervals will be one less than
# the length of the masterlist)
stamp_number.append(int(j)) 
intervals_1919=[]
#diagnostic indices that track how often the various if statments are satisfied
m=0
n=0
for i in range(len(masterlist_1919)-1):
#calculate intervals between consecutive entries in the masterlist
    interval=masterlist_1919[i+1][0]-masterlist_1919[i][0]
    intervals_1919.append(interval)
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
        if masterlist_1919[i+1][2]==masterlist_1919[i][2] and masterlist_1919[i+1][3]!=masterlist_1919[i][3]:
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

for i in range(len(masterlist_1919)):
    masterlist_1919[i].append(stamp_number[i])
    masterlist_1919[i].append(duplicates[i])

duplicates=[' ']*len(masterlist_1957)
        
stamp_number=[] #a list to store the timestamp identifiers 
j=2 #the timestamp identifier, beginning at two
# add the first timestamp identifier (since the intervals will be one less than
# the length of the masterlist)
stamp_number.append(int(j)) 
intervals_1957=[]
#diagnostic indices that track how often the various if statments are satisfied
for i in range(len(masterlist_1957)-1):
#calculate intervals between consecutive entries in the masterlist
    interval=masterlist_1957[i+1][0]-masterlist_1957[i][0]
    intervals_1957.append(interval)
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
        if masterlist_1957[i+1][2]==masterlist_1957[i][2] and masterlist_1957[i+1][3]!=masterlist_1957[i][3]:
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

for i in range(len(masterlist_1957)):
    masterlist_1957[i].append(stamp_number[i])
    masterlist_1957[i].append(duplicates[i])


duplicates=[' ']*len(masterlist_2016)
        
stamp_number=[] #a list to store the timestamp identifiers 
j=2 #the timestamp identifier, beginning at two
# add the first timestamp identifier (since the intervals will be one less than
# the length of the masterlist)
stamp_number.append(int(j)) 
intervals_2016=[]
#diagnostic indices that track how often the various if statments are satisfied
for i in range(len(masterlist_2016)-1):
#calculate intervals between consecutive entries in the masterlist
    interval=masterlist_2016[i+1][0]-masterlist_2016[i][0]
    intervals_2016.append(interval)
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
        if masterlist_2016[i+1][2]==masterlist_2016[i][2] and masterlist_2016[i+1][3]!=masterlist_2016[i][3]:
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

for i in range(len(masterlist_2016)):
    masterlist_2016[i].append(stamp_number[i])
    masterlist_2016[i].append(duplicates[i])


#print out diagnostic information

print '''Diagnostics
\t Zero if statment was called {0} times
\t Greater than rate if statement was called {1} times
 '''.format(int(m),int(n))


#print sequence number, disk, and duplication (if applicable) to a file for each
#node, coordinating the stamp_number across all nodes
def WriteFile5Cols(values,fname):
    with open(fname,"w") as data:
        for i in range(len(values)):
            data.write("{0} {1} {2}\n".format(values[i][0],values[i][1],values[i][2],values[i][3],values[i][4]))

def WriteFile4Cols(values,fname):
    with open(fname,"w") as data:
        for i in range(len(values)):
            data.write("{0} {1} {2} {3}\n".format(values[i][0],values[i][1],values[i][2],values[i][3]))

masterlist=masterlist_1919

n=33
while n < 40:
    name='node{0}_july2/1919_coordinated_generated_sequence.dat'.format(n)
    master=[]
    node=n-33
    for i in range(len(masterlist)):
        if masterlist[i][2] == node:
            point=[masterlist[i][4], masterlist[i][1], masterlist[i][3], masterlist[i][5]]
            master.append(point)
    WriteFile4Cols(master,name)
    n+=1
#print the master sequence file, with sequence number, disk, node and 
#duplication (if applicable)


name='1919_MasterSequenceFile.dat'
master=[]
for i in range(len(masterlist)):
    point=[masterlist[i][4],masterlist[i][1],(masterlist[i][2]+33),masterlist[i][3],masterlist[i][5]]
    master.append(point)
WriteFile5Cols(master,name)

masterlist=masterlist_1957

n=33
while n < 40:
    name='node{0}_july2/1957_coordinated_generated_sequence.dat'.format(n)
    master=[]
    node=n-33
    for i in range(len(masterlist)):
        if masterlist[i][2] == node:
            point=[masterlist[i][4], masterlist[i][1], masterlist[i][3],masterlist[i][5]]
            master.append(point)
    WriteFile4Cols(master,name)
    n+=1
#print the master sequence file, with sequence number, disk, node and 
#duplication (if applicable)


name='1957_MasterSequenceFile.dat'
master=[]
for i in range(len(masterlist)):
    point=[masterlist[i][4],masterlist[i][1],(masterlist[i][2]+33),masterlist[i][3],masterlist[i][5]]
    master.append(point)
WriteFile5Cols(master,name)

            
masterlist=masterlist_2016

n=33
while n < 40:
    name='node{0}_july2/2016_coordinated_generated_sequence.dat'.format(n)
    master=[]
    node=n-33
    for i in range(len(masterlist)):
        if masterlist[i][2] == node:
            point=[masterlist[i][4], masterlist[i][1], masterlist[i][3],masterlist[i][5]]
            master.append(point)
    WriteFile4Cols(master,name)
    n+=1
#print the master sequence file, with sequence number, disk, node and 
#duplication (if applicable)


name='2016_MasterSequenceFile.dat'
master=[]
for i in range(len(masterlist)):
    point=[masterlist[i][4],masterlist[i][1],(masterlist[i][2]+33),masterlist[i][3],masterlist[i][5]]
    master.append(point)
WriteFile5Cols(master,name)
