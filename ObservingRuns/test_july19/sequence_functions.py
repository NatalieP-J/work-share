import manage as man
from astropy.time import Time
import numpy as np
import argparse

parser=argparse.ArgumentParser()

parser.add_argument('--tot', type=int,default=16, help="Total number of nodes")
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
stamps.append('.2013-07-24T01:50:00')
stamps.append('_split.2013-07-24T01:50:00.PSR1810')
stamps.append('_split.2013-07-24T01:50:00.PSR1919')
stamp = stamps[source]

split_time=[]
split_time.append(['july23','PSR1810',2080200,2087940])
split_time.append(['july23','PSR1919',2088000,2088600])


#define the rate at which timestamps should appear
nanoseconds=15.
samples=2.**24
rate=(nanoseconds/10**9)*samples

def ImportTime_MergeDisks_SORT(node,stamp_ID):
    newlist=[]    
    i=0
    while i < 5:
        fname='node{0}/timestamp{1}.{2}.dat'.format(node,stamp_ID,i)
        try:
            times = man.LoadData(fname)
            day = man.IterativeIntAppend(times,2)
            hour = man.IterativeIntAppend(times,3)
            minute = man.IterativeIntAppend(times,4)
            second = man.IterativeIntAppend(times,5)
            frac = man.IterativeFloatAppend(times,6)
            for j in range(len(times)):
                point = (day[j]*86400) + (hour[j]*3600) + (minute[j]*60) + second[j] + frac[j]
                point = [point,i,node,times[j]]
                newlist.append(point)
            print "Done node{0}/timestamp{1}.{2}.dat".format(node,stamp_ID,i)
            i+=1 
#if a timestamp file is missing, report it and go to the next one
        except IOError:
            print "Missing node{0}/timestamp{1}.{2}.dat".format(node,stamp_ID,i)
            i+=1
            pass
    newlist.sort()
    return newlist

def Time_MergeNodes_SORT(min_node,tot,stamp_ID):
    masterlist = []
    time = []
    max_node = min_node + tot
    n = min_node
    beginners = []
    while n < max_node:
        mastertime = ImportTime_MergeDisks_SORT (n,stamp_ID)
        start = mastertime[0]
        beginners.append(start)
        for i in range(len(mastertime)):
            masterlist.append(mastertime[i])
        n+=1
    starter = CheckStartTimes(beginners)
    interval = starter[0]
    problem_node = starter[1]
    bump_val = sum(interval)/len(interval)
    n = min_node
    counter =[]
    while n < max_node:
        m = n - min_node
        total = problem_node.count(m)
        print total
        if total == 1: 
            pass
        else:
            counter.append(n)
        n+=1
    clock_errors = len(counter)
    if clock_errors != 1:
        print 'Multiple clock errors' 
    prob = counter[0]
    for i in range(len(masterlist)):
        if masterlist[i][2] == prob:
            masterlist[i][0] += bump_val
    masterlist.sort()
    return masterlist

def GenTimestamps(time,interval,stamp_ID):
    fname = "gen_timestamp_{0}.dat".format(stamp_ID)
    start=time[0]
    day = man.IterativeIntAppend(times,2)
    hour = man.IterativeIntAppend(times,3)
    minute = man.IterativeIntAppend(times,4)
    second = man.IterativeIntAppend(times,5)
    frac = man.IterativeFloatAppend(times,6)
    end=time[len(time)]
    with open(fname,"w") as data:
        data.write("{0}\n".format(start))
        while i<= (end):
            data.write("{0}\n".format(i))
            print 'working {0}'.format(float(i)/end)
            i+=rate

def CheckStartTimes(starter_values):
    newlist=[]
    interval = []
    problem_node = []
    i=0
    while i < (len(starter_values)):
        j=0
        while j < (len(starter_values)):
            diff = starter_values[i][0] - starter_values[j][0]
            diff = np.around(diff, decimals=1)
            if diff < 0.3: #0.3 being the rate rounded to one decimal point
                pass
            else:
                interval.append(diff)
                problem_node.append(i)
                problem_node.append(j)
                print i,j,diff
            j+=1
        i+=1
    print problem_node
    newlist.append(interval)
    newlist.append(problem_node)
    return newlist


def SequenceTimestamp(masterlist):
    duplicates=[' ']*len(masterlist)
    m=0  
    n=0
    stamp_number=[] 
    j=2 

    stamp_number.append(int(j)) 
    for i in range(len(masterlist)-1):
        interval=masterlist[i+1][0]-masterlist[i][0]

        if interval < 0:
            print 'masterlist sort failed'

        if np.around(interval,decimals=1) == 0:
            stamp_number.append(int(j))

            if masterlist[i+1][2]==masterlist[i][2] and masterlist[i+1][1]!=masterlist[i][1]:
                duplicates[i]='duplicate'
                duplicates[i+1]='duplicate'
            m+=1

        if np.around(interval,decimals=1) > 0:
            point=interval/rate
            point=np.around(point,decimals=0)
            j+=point
            stamp_number.append(int(j))
            n+=1

    for i in range(len(masterlist)):
        masterlist[i].append(stamp_number[i])
        masterlist[i].append(duplicates[i])

    print '''Diagnostics
    \t Zero if statment was called {0} times
    \t Greater than rate if statement was called {1} times
    '''.format(int(m),int(n))
    
    return masterlist

def CreateSequenceFile(min_node,tot,masterlist,stamp_ID):
    n=min_node
    max_node = min_node + tot
    while n < max_node:
        name='node{0}/coordinated_generated_sequence{1}.dat'.format(n,stamp_ID)
        master=[]
        for i in range(len(masterlist)):
            if masterlist[i][2] == n:
                point=[masterlist[i][4], masterlist[i][1], masterlist[i][5]]
                master.append(point)
        man.WriteFile3Cols(master,name)
        n+=1

    name='MasterSequenceFile{0}.dat'.format(stamp_ID)
    master=[]
    for i in range(len(masterlist)):
        point=[masterlist[i][4],masterlist[i][1],(masterlist[i][2]),masterlist[i][5]]
        master.append(point)
    man.WriteFile4Cols(master,name)

def Differences(values,index):
    newlist=[]
    for i in range(len(values)-1):
        point=values[i+1][index]-values[i][index]
        newlist.append(point)
    return newlist

def SortSequence(min_node,tot,stamp_ID):
    n = min_node
    max_node = min_node + tot
    if '_voltage' in stamp_ID:
        stamp_ID = stamp_ID[8:]
    while n < max_node:
        try:
            fname='node{0}/sequence{1}.dat'.format(n,stamp_ID)
            sequence=man.LoadData(fname)
            time=man.IterativeIntAppend(sequence,0)
            disk=man.IterativeIntAppend(sequence,1)
            sequence=[]
            for i in range(len(time)):
                point=[time[i],disk[i]]
                sequence.append(point)
            sequence.sort()
            check=Differences(sequence,0)
            for i in range(len(check)):
                if check[i] < 0:
                    print 'Sort failed'
            name='node{0}/sequence.sorted{1}.dat'.format(n,stamp_ID)
            man.WriteFileCols(sequence,name)
            n+=1
        except IOError:
            print 'No sequence file on node{0}'.format(n)
            n+=1
            pass

def SequenceCompare(min_node,tot,stamp_ID):
    n=min_node
    max_node = min_node + tot
    while n < max_node:
        try:
            fname='node{0}/coordinated_generated_sequence{1}.dat'.format(n,stamp_ID)
            gen_sequence=man.LoadData(fname)
            gen_stamp=man.IterativeIntAppend(gen_sequence,0)
            fname='node{0}/sequence.sorted.dat'.format(n)
            sequence=man.LoadData(fname)
            k=0
            m=0
            stamp=man.IterativeIntAppend(sequence,0)
            if len(gen_stamp)!=len(stamp): 
                diff=len(stamp)-len(gen_stamp)
                print '''Different number of timestamps for node{0}\n \t{1} in generated file\n \t{2} in actual file\n \t{3} difference'''.format(n,len(gen_stamp),len(stamp),diff)
            if len(gen_stamp)<len(stamp):
                i=0
                difference=[]
                while i < (len(gen_stamp)-1):
                    point=gen_stamp[i]-stamp[i]
                    difference.append(point)
                    if i>0:
                        if point!=0:
                            m+=1
                            if point != difference[i-1]:
                                k+=1
                    i+=1
                print '\t{0} mismatched timestamps'.format(m)
                print '\t{0} offset'.format(k)
            else:
                print 'Generated time stamp longer than actual file for node{0}'.format(n)
            name='node{0}/sequence_difference{1}.dat'.format(n,stamp_ID)
            man.WriteFile(difference,name)
            n+=1
        except IOError:
            print 'Missing sequence file on node{0}'.format(n)
            n+=1
            pass

def TimestampMerge(min_node,tot,stamp_ID):
    diff=[]
    n=min_node
    while n < max_node:
        mastertime=[]
        j=1
        while j<5:
            fname='node{0}/timestamp{1}.{2}.dat'.format(n,stamp_ID,j)
            try:
                times=man.LoadData(fname)
                year=man.IterativeStrAppend(times,0)
                month=man.IterativeStrAppend(times,1)
                day=man.IterativeStrAppend(times,2)
                hour=man.IterativeStrAppend(times,3)
                minute=man.IterativeStrAppend(times,4)

                seconds=[]
                for i in range(len(times)-2):
                    a=man.IterativeIntAppend(times,5)
                    b=man.IterativeFloatAppend(times,6)
                    point=a[i]+b[i]
                    seconds.append(point)

                time=[]
                for i in range(len(times)-2):
                    point="{0}-{1}-{2} {3}:{4}:{5}".format(year[i],month[i],day[i],hour[i],minute[i],seconds[i])
                    time.append(point)

                t=Time(time, format='iso',scale='utc')
                mjd=t.mjd
                mjd.sort()
                diff.append(mjd)
                r=Time(mjd,format='mjd',scale='utc')
                iso=r.iso
                for i in range(len(iso)):
                    point=[iso[i],j-1]
                    mastertime.append(point)
                print "Done node{0}/timestamp{1}.{2}.dat".format(n,stamp_ID,j)
                j+=1 
            except IOError:
                print "Missing node{0}/timestamp{1}.{2}.dat".format(n,stamp_ID,j)
                j+=1
                pass

        mastertime.sort()
        name='node{0}/MergedTimeStamp.dat'.format(n,stamp_ID)
        man.WriteFileCols(mastertime,name)
        print 'Done master time stamp node{0}'.format(n)
        n+=1

def TimestampSplitter(min_node,tot,stamp_ID,time_split):
    split_mastertime = []
    for i in range(len(time_split)):
        split_mastertime.append([time_split[i][1]])
    n = min_node
    max_node = min_node + tot
    sources = ['PSR1919','PSR1810']
    while n < max_node:
        mastertime = ImportTime_MergeDisks_SORT (n,stamp_ID)
        for j in range(len(split_mastertime)):
            source = sources[j]
            for i in range(len(mastertime)):
                if time_split[j][2] <= mastertime[i][0] <= time_split[j][3]:
                    split_mastertime[j].append(mastertime[i][3])
            split_mastertime[j].pop(0)
            fname = 'node{0}/timestamp_split{1}.{2}.dat'.format(n,stamp_ID,source)
            man.WriteFile(split_mastertime[j],fname)
        n+=1
    return split_mastertime









