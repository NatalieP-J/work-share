import manage as man
from astropy.time import Time
import numpy as np


#list stamp formats
stamps=[]
stamps.append('.2013-07-26T18:31:14')

no_split_time=[]

#define the rate at which timestamps should appear
nanoseconds=15.
samples=2.**24
rate=(nanoseconds/10**9)*samples

#parser=argparse.ArgumentParser()

#optional arguments to specifiy which nodes to loop over and the stamp (source)
#parser.add_argument('--tot', type=int,default=16, help="Total number of nodes")
#parser.add_argument('--min', type=int,default=17, help="Minimum node number")
#parser.add_argument('--sta', type=int,default=3,help='''Choose a source to evaluate a sequence file for - run sequence_functions and type stamps for full list ''')

#parse command line
#args=parser.parse_args()
#min_node=args.min
#tot=args.tot
#source=args.sta

#stamp = stamps[source]


#Import times from timestamps and merges for a node across all disks
#i goes from 0 to 4 because older files span 1-4 while newer ones span 0-3
#This means that at least one timestamp is reported missing for every node
def ImportTime_MergeDisks_SORT(node,stamp_ID):
    """ Return a list of modified timestamps suitable for sequencing.
        Report missing timestamp files.

        Keyword Arguments:
            node -- an integer node number
            stamp_ID -- a string used to uniquely identify a file
                    eg if the file name is timestamp.2013-07-25T01:30:00.1.dat,
                    the stamp_ID is '.2013-07-25T01:30:00'

    """
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

#Merges times across all nodes, and checks that they all begin at the same
#time - if they do not, adjusts values accordingly by a constant and reports 
#the error
#Above feature accounts for systematic clock error in node18 and node34, since
#rectified (hopefully)
#outputs a masterlist of timestamps merged across all nodes
def Time_MergeNodes_SORT(min_node,tot,stamp_ID,clock_fix):
    """ Return a numerically sorted list of timestamps merged across all nodes. 
        Report nodes that are missing all timestamp files.
        Apply a time adjustment if called for.

        Keyword Arguments
            min_node -- the smallest node number, an integer
            tot -- the total number of nodes, an integer
            stamp_ID -- a string used to uniquely identify a file
                    eg if the file name is timestamp.2013-07-25T01:30:00.1.dat,
                    the stamp_ID is '.2013-07-25T01:30:00'
            clock_fix -- if True, code adjusts each timestamp by a constant value
                    for a node whose start time is different from the others
                    *STILL IN BETA*

    """
    masterlist = []
    time = []
    max_node = min_node + tot
    n = min_node
    beginners = []
    while n < max_node:
        mastertime = ImportTime_MergeDisks_SORT(n,stamp_ID)
        try:
            start = mastertime[0]
            beginners.append(start)
        except IndexError:
            print 'Missing all timestamps on node{0}'.format(n)
        for i in range(len(mastertime)):
            masterlist.append(mastertime[i])
        n+=1
    if clock_fix is True:
        starter = CheckStartTimes(beginners)
        interval = starter[0]
        problem_node = starter[1]
        number_prob_nodes = []
        node_prob = []
        for i in range(len(interval)):
            if np.around(interval[i],decimals=0) not in number_prob_nodes:
                number_prob_nodes.append(interval[i])
                node_prob.append(problem_node[i])
        for j in range(len(number_prob_nodes)):
            for i in range(len(interval)):
                if interval[i] == number_prob_nodes[j]:
                    bump_val = number_prob_nodes[j]
                    n = min_node
                    counter =[]
                    while n < max_node:
                        m = n - min_node
                        total = node_prob.count(m)
                        if total == 1: 
                            pass
                        else:
                            print 'Clock error on node{0}.'.format(n)
                            counter.append(n)
                            n+=1
                        prob = counter[0]
                for k in range(len(masterlist)):
                    if masterlist[k][2] == prob:
                        masterlist[k][0] += bump_val
    print '{0} clock errors'.format(len(number_prob_nodes))
    masterlist.sort()
    return masterlist

#generate timestamps ~0.251 seconds apart
#still doesn't quite do what I need
def GenTimestamps(start,end,stamp_ID):
    """ Generate timestamps ~0.251 seconds apart"""
    fname = "gentimestamp{0}.dat".format(stamp_ID)
    nanoseconds=15.
    samples=2.**24
    rate=(nanoseconds/10**9)*samples
    with open(fname,"w") as data:
        data.write("{0}\n".format(start))
        i=0
        while i<=end:
            data.write("{0}\n".format(i))
            i+=rate

#checks that each file starts at the same time and identifies the nodes that
#do not conform
def CheckStartTimes(starter_values):
    """ Check that each pair of values in the list are within 0.3 of each other
        when rounded to one decimal place.
        Return a list of differences and the indices of the pairs associated 
        with them.
            starter_values -- a list of values
    """
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
            j+=1
        i+=1
    newlist.append(interval)
    newlist.append(problem_node)
    return newlist

#assigns sequence numbers to the timestamp file and identifies duplicate
#timestamps - takes a masterlist of timestamps merged across all disks and 
#nodes and outputs a masterlist
def SequenceTimestamp(masterlist):
    """ Assign a sequence number to each value in the list.
        Identify duplicate timestamps (if on the same node) and give them 
        the same sequence number.
        Return a list of which the elements are sequence number, disk number, 
        node number and duplicate string
            masterlist -- a list of timestamps prepared by 
                ImportTime_MergeDisks_SORT
                or TimestampSplitter_ClockError 
                or TimestampSplitter
    """
    nanoseconds=15.
    samples=2.**24
    rate=(nanoseconds/10**9)*samples #???
    rate = 0.335
    num_entries = (masterlist[len(masterlist)-1][0]-masterlist[0][0])
    num_entries = num_entries/rate
    num_entries = int(num_entries)
    newlist=[' ']*num_entries
    duplicates=[' ']*num_entries
    m=0  
    n=0
    stamp_number=[] 
    j=2 
    k=0
    stamp_number.append(int(j)) 
    for i in range(len(masterlist)-1):
        interval=masterlist[i+1][0]-masterlist[i][0]

        if interval < 0:
            print 'masterlist sort failed'

        if np.around(interval,decimals=1) == 0:
            stamp_number.append(int(j))
            newlist[k] = masterlist[i]
            newlist[k+1] = masterlist[i]
            k+=2
            m+=1

        if np.around(interval,decimals=1) > 0:
            point=interval/rate
            point=np.around(point,decimals=0)
            point=int(point)
            newlist[k]=masterlist[i]
            k+=1
            if point > 1:
                for f in range(point-1):
                    place_holder = ['N/A',3,'N/A','N/A']
                    newlist[k] = place_holder
                    k+=1
                    stamp_number.append(-1)
            j+=point
            stamp_number.append(int(j))
            n+=1
    newlist2=[]
    for i in range(len(newlist)):
        if newlist[i]==' ':
            print 'Empty space'
            #newlist2.append(['N/A',3,'N/A','N/A',-1])
        else:
            newlist2.append(newlist[i])
            newlist2[i].append(stamp_number[i])
            newlist2[i].append(duplicates[i])
    newlist=newlist2
    
    print '''Diagnostics
    \t Zero if statment was called {0} times
    \t Greater than rate if statement was called {1} times
    '''.format(int(m),int(n))
    
    return newlist

#write masterlist produced by SequenceTimestamp to the appropriate sequence 
#files
def CreateSequenceFile(min_node,tot,masterlist,stamp_ID):
    """ Write a list of sequenced timestamps to appropriately named files.
        Create a master sequence file.
            min_node -- the smallest node number, an integer
            tot -- the total number of nodes, an integer
            masterlist -- a list whose elements look like 
                [modified timestamp, disk number, node number, timestamp, 
                sequence number, duplicate string]
                Output of SequenceTimestamp
            stamp_ID -- a string used to uniquely identify a file
                    eg if the file name is timestamp.2013-07-25T01:30:00.1.dat,
                    the stamp_ID is '.2013-07-25T01:30:00'
    """
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
        point=[masterlist[i][4],masterlist[i][1],masterlist[i][2],masterlist[i][5]]
        master.append(point)
    man.WriteFile4Cols(master,name)

#write masterlist produced by SequenceTimestamp to the appropriate sequence 
#files
def CreateSequenceAROFile(min_node,tot,masterlist,stamp_ID):
    """ Write a list of sequenced timestamps to appropriately named files.
        Create a master sequence file.
            min_node -- the smallest node number, an integer
            tot -- the total number of nodes, an integer
            masterlist -- a list whose elements look like 
                [modified timestamp, disk number, node number, timestamp, 
                sequence number, duplicate string]
                Output of SequenceTimestamp
            stamp_ID -- a string used to uniquely identify a file
                    eg if the file name is timestamp.2013-07-25T01:30:00.1.dat,
                    the stamp_ID is '.2013-07-25T01:30:00'
    """
    n=min_node
    max_node = min_node + tot
    while n < max_node:
        name='node{0}/sequence{1}.mod.dat'.format(n,stamp_ID)
        master=[]
        for i in range(len(masterlist)):
            point=[masterlist[i][4], masterlist[i][1]]
            master.append(point)
        man.WriteFileCols(master,name)
        n+=1

#Check differences between consecutive values in a list
def Differences(values,index):
    """Find the difference between consecutive elements in a list"""
    newlist=[]
    for i in range(len(values)-1):
        point=values[i+1][index]-values[i][index]
        newlist.append(point)
    return newlist

#sort existing sequence files into numerical order by sequence numbers
def SortSequence(min_node,tot,stamp_ID):
    """Sort a sequence file by sequence number
            min_node -- the smallest node number, an integer
            tot -- the total number of nodes, an integer
            stamp_ID -- a string used to uniquely identify a file
                    eg if the file name is timestamp.2013-07-25T01:30:00.1.dat,
                    the stamp_ID is '.2013-07-25T01:30:00'
    """
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

#Compare produced seqeunce file with original one
def SequenceCompare(min_node,tot,stamp_ID):
    """Compare a produced sequence file with the original one"""
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

#Merge timestamps into a master timestamp file
def TimestampMerge(min_node,tot,stamp_ID):
    """Merge timestamps files across nodes and write merged list to file"""
    masterlist=[]
    diff=[]
    n=min_node
    max_node = min_node + tot
    while n < max_node:
        mastertime=[]
        j=0
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
                for i in range(len(times)):
                    a=man.IterativeIntAppend(times,5)
                    b=man.IterativeFloatAppend(times,6)
                    point=a[i]+b[i]
                    if np.remainder(i,100) == 0:
                        print 'Done {0} of {1} seconds'.format(i,len(times))
                    seconds.append(point)

                time=[]
                for i in range(len(times)):
                    point="{0}-{1}-{2} {3}:{4}:{5}".format(year[i],month[i],day[i],hour[i],minute[i],seconds[i])
                    if np.remainder(i,100) == 0:
                        print 'Done {0} of {1} stamps'.format(i,len(times))
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
                    masterlist.append(point)
                print "Done node{0}/timestamp{1}.{2}.dat".format(n,stamp_ID,j)
                j+=1 
            except IOError:
                print "Missing node{0}/timestamp{1}.{2}.dat".format(n,stamp_ID,j)
                j+=1
                pass

        mastertime.sort()
        name='node{0}/MergedTimeStamp{1}.dat'.format(n,stamp_ID)
        man.WriteFileCols(mastertime,name)
        print 'Done master time stamp node{0}'.format(n)
        n+=1
    masterlist.sort()
    name='MasterTimeStamp{0}.dat'.format(stamp_ID)

#Split timestamps file on certain times (ie when 1 file contains multiple
#sources) - produces a list
def TimestampSplitter_ClockError(min_node,tot,stamp_ID,time_split):
    """ Split a list of timestamps on predefined values.
        Check for clock errors
    """
    masterlist = []
    split_mastertime = []
    write_time = []
    beginners = []
    for i in range(len(time_split)):
        write_time.append([time_split[i][1]])
        split_mastertime.append([time_split[i][1]])
    n = min_node
    max_node = min_node + tot
    sources = ['PSR1810','PSR1919']
    while n < max_node:
        mastertime = ImportTime_MergeDisks_SORT (n,stamp_ID)
        start = mastertime[0]
        beginners.append(start)
        for i in range(len(mastertime)):
            masterlist.append(mastertime[i])
        n+=1
    masterlist.sort()
    starter = CheckStartTimes(beginners)
    interval = starter[0]
    problem_node = starter[1]
    if len(interval) != 0:
            bump_val = sum(interval)/len(interval)
    else:
        bump_val = 0
    n = min_node
    counter =[]
    while n < max_node:
        m = n - min_node
        total = problem_node.count(m)
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
    for j in range(len(time_split)):
        for i in range(len(masterlist)):
            if time_split[j][2] <= masterlist[i][0] <= time_split[j][3]:
                write_time[j].append(masterlist[i][3])
                split_mastertime[j].append(masterlist[i])
        write_time[j].pop(0)
        split_mastertime[j].pop(0)
    #fname = 'node{0}/timestamp_split{1}.{2}.dat'.format(n,stamp_ID,sources[j])
    #man.WriteFileCols8(write_time[j],fname)
    return split_mastertime

def TimestampSplitter(min_node,tot,stamp_ID,time_split):
    """ Split timestamps on a predefined values"""
    masterlist = []
    split_mastertime = []
    write_time = []
    for i in range(len(time_split)):
        write_time.append([time_split[i][1]])
        split_mastertime.append([time_split[i][1]])
    n = min_node
    max_node = min_node + tot
    sources = []
    for i in range(len(time_split)):
        sources.append(time_split[i][1])
    while n < max_node:
        mastertime = ImportTime_MergeDisks_SORT(n,stamp_ID)
        for i in range(len(mastertime)):
            masterlist.append(mastertime[i])
        n+=1
    masterlist.sort()
    for j in range(len(time_split)):
        for i in range(len(masterlist)):
            if time_split[j][2] <= masterlist[i][0] <= time_split[j][3]:
                write_time[j].append(masterlist[i][3])
                split_mastertime[j].append(masterlist[i])
        write_time[j].pop(0)
        split_mastertime[j].pop(0)
        fname = 'timestamp_split{1}.{2}.dat'.format(n,stamp_ID,sources[j])
        man.WriteFileCols8(write_time[j],fname)
    return split_mastertime

def GenerateSequencing(min_node,tot,split,time_split,clock_fix,stamp_ID):
    """A parent function that runs a list of functions to produce sequence files"""
    if split is True:
        if clock_fix is True:
            master = TimestampSplitter_ClockError(min_node,tot,stamp_ID,time_split)
            for i in range(len(time_split)):
                mastertime = master[i]
                sequence = SequenceTimestamp(mastertime)
                split_stamp_ID = '_split' + stamp_ID + time_split[i][1]
                CreateSequenceFile(min_node,tot,sequence,split_stamp_ID)
        else:
            master = TimestampSplitter(min_node,tot,stamp_ID,time_split)
            for i in range(len(time_split)):
                mastertime = master[i]
                sequence = SequenceTimestamp(mastertime)
                split_stamp_ID = '_split' + stamp_ID + time_split[i][1]
                CreateSequenceFile(min_node,tot,sequence,split_stamp_ID)
    else:
        master = Time_MergeNodes_SORT(min_node,tot,stamp_ID,clock_fix)
        sequence = SequenceTimestamp(master)
        CreateSequenceFile(min_node,tot,sequence,stamp_ID)



