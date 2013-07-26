import manage as man
from astropy.time import Time
import numpy as np
import argparse

parser=argparse.ArgumentParser()

parser.add_argument('--tot', type=int,default=8, help="Total number of nodes")
parser.add_argument('--min', type=int,default=17, help="Minimum node number")
parser.add_argument('--sta', type=int,default=3,help='''Choose a source to evaluate a sequence file for - options are:
0=.20130719053400
1=.2013-07-19T05:36:00
2=_voltage.all.test_2_july19
3=_voltage.all.1810_2_july19 ''')

#parse command line
args=parser.parse_args()

min_node=args.min
tot=args.tot
max_node=min_node+tot + 1
source=args.sta

stamps=[]
stamps.append('.20130719053400')
stamps.append('.2013-07-19T05:36:00')
stamps.append('_voltage.all.test_2_july19')
stamps.append('_voltage.all.1810_2_july19')
stamp = stamps[source]

#define the rate at which timestamps should appear
nanoseconds=15.
samples=2.**24
rate=(nanoseconds/10**9)*samples

#NODE18 is early
prob = 18
bump_val = 956.8149109999999


#create an empty list to store timestamps in
masterlist=[]
sequence_begin=[]
#d

n=min_node
while n<max_node:
    if n == prob: #problem node
#within node, extract the times from every timestamp file
        i=0
        while i<5:
#identifies the name of each timestamp file within a given node's 
#directory
            fname='node{0}/timestamp{1}.{2}.dat'.format(n,stamp,i)
#if fname points to a real file, extract the times
            try:
                times=man.LoadData(fname)
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
                    point=(hour[j]*3600)+(minute[j]*60)+(seconds[j])+(frac[j])+bump_val #normalizing problem node
                    time.append(point)
                for j in range(len(time)):
#add the time and the disk to which it was written (timestamp number minus 1) 
#to the masterlist within the node
                    point=[time[j],i-1]
                    pt=[time[j],i-1,n-min_node]
                    masterlist.append(pt)
#print a status update to screen and go to the next timestamp
                print "Done node{0}/timestamp{1}.{2}.dat".format(n,stamp,i)
                i+=1 
#if a timestamp file is missing, report it and go to the next one
            except IOError:
                print "Missing node{0}/timestamp{1}.{2}.dat".format(n,stamp,i)
                i+=1
                pass
        
    else:
#within node, extract the times from every timestamp file
        i=0
        while i<5:
#identifies the name of each timestamp file within a given node's 
#directory
            fname='node{0}/timestamp{1}.{2}.dat'.format(n,stamp,i)
#if fname points to a real file, extract the times
            try:
                times=man.LoadData(fname)
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
                    point=[time[j],i-1]
                    pt=[time[j],i-1,n-min_node]
                    masterlist.append(pt)
#print a status update to screen and go to the next timestamp
                print "Done node{0}/timestamp{1}.{2}.dat".format(n,stamp,i)
                i+=1 
#if a timestamp file is missing, report it and go to the next one
            except IOError:
                print "Missing node{0}/timestamp{1}.{2}.dat".format(n,stamp,i)
                i+=1
                pass            

#sort the file within the node to be in chronological order                
        
#name the file that will result and put it in the appropriate node direactory
        #name='node{0}/SequencedTimeStamp.dat'.format(n)
        #WriteFileCols(mastertime,name)
#print another status update to screen
        print 'Done sequenced time stamp node{0}'.format(n)
        n+=1 
        
#sort the masterlist      
masterlist.sort()
mastertime=masterlist

duplicates=[' ']*len(masterlist)
m=0        
stamp_number=[] #a list to store the timestamp identifiers 
j=2 #the timestamp identifier, beginning at two
# add the first timestamp identifier (since the intervals will be one less than
# the length of the masterlist)
stamp_number.append(int(j)) 
for i in range(len(masterlist)-1):
#calculate intervals between consecutive entries in the masterlist
    interval=masterlist[i+1][0]-masterlist[i][0]
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
        if masterlist[i+1][2]==masterlist[i][2] and masterlist[i+1][3]!=masterlist[i][3]:
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

for i in range(len(masterlist)):
    masterlist[i].append(stamp_number[i])
    masterlist[i].append(duplicates[i])



#print out diagnostic information

print '''Diagnostics
\t Zero if statment was called {0} times
\t Greater than rate if statement was called {1} times
 '''.format(int(m),int(n))


#print sequence number, disk, and duplication (if applicable) to a file for
#each node, coordinating the stamp_number across all nodes

masterlist=mastertime

n=min_node
while n < max_node:
    name='node{0}/coordinated_generated_sequence.dat'.format(n)
    master=[]
    node=n-min_node
    for i in range(len(masterlist)):
        if masterlist[i][2] == node:
            point=[masterlist[i][4], masterlist[i][1], masterlist[i][3], masterlist[i][5]]
            master.append(point)
    man.WriteFile4Cols(master,name)
    n+=1
#print the master sequence file, with sequence number, disk, node and 
#duplication (if applicable)


name='MasterSequenceFile{0}.dat'.format(stamp)
master=[]
for i in range(len(masterlist)):
    point=[masterlist[i][4],masterlist[i][1],(masterlist[i][2]+min_node),masterlist[i][3],masterlist[i][5]]
    master.append(point)
man.WriteFile5Cols(master,name)
