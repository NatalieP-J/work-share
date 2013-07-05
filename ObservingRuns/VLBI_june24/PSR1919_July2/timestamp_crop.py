import manage as man
from astropy.time import Time
import numpy as np

def WriteFile6Cols(values,fname):
    with open(fname,"w") as data:
        for i in range(len(values)):
            data.write("{0} {1}\n".format(values[i][0],values[i][1],values[i][2],values[i][3],values[i][4],values[i][5],values[i][6]))

masterlist_1919=[]
masterlist_1957=[]
masterlist_2016=[]

disk_type=['EoR','a_d']
#begin outer loop at node33 to be looped over all nodes up to node39
for d in range(len(disk_type)):
    n=33
    while n<40:
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
                    if 12120 <= time[j] <= 18600:
                        mastertime_1919.append(times[j])
                        masterlist_1919.append(times[j])
                    if 18660 <= time[j] <= 25560:
                        mastertime_1957.append(times[j])
                        masterlist_1957.append(times[j])
                    if 25680 <= time[j] <= 26400:
                        mastertime_1957.append(times[j])
                        masterlist_2016.append(times[j])
#print a status update to screen and go to the next timestamp
                print "Done node{0}_july2/timestamp_voltage.all.1919_2_july2.{1}.dat".format(n,i)
                i+=1 
#if a timestamp file is missing, report it and go to the next one
            except IOError:
                print "Missing node{0}_july2/timestamp_voltage.all.1919_2_july2.{1}.dat".format(n,i)
                i+=1
                pass

#sort the file within the node to be in chronological order                
#name the file that will result and put it in the appropriate node direactory
        #name='node{0}/SequencedTimeStamp.dat'.format(n)
        #WriteFileCols(mastertime,name)
#print another status update to screen
        print 'Done sequenced time stamp node{0}'.format(n)
        name='node{0}_july2/timestamp_1919_july2.dat'.format(n)
        man.WriteFile(mastertime_1919,name)
        name='node{0}_july2/timestamp_1957_july2.dat'.format(n)
        man.WriteFile(mastertime_1957,name)
        name='node{0}_july2/timestamp_2016_july2.dat'.format(n)
        man.WriteFile(mastertime_2016,name)
        n+=1 


name='timestamp_1919_july2.dat'
man.WriteFile(masterlist_1919,name)
name='timestamp_1957_july2.dat'
man.WriteFile(masterlist_1957,name)
name='timestamp_2016_july2.dat'
man.WriteFile(masterlist_2016,name)
        
