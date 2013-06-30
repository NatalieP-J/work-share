import manage as man
import numpy as np
nanoseconds=15.
samples=2.**24
rate=(nanoseconds/10**9)*samples
timestamp=[]
n=33
while n<49:
    stamp_number=[]
    fname='node{0}/SequencedTimeStamp.dat'.format(n)
    sequence=man.LoadDataTab(fname)
    time=man.IterativeFloatAppend(sequence,1)
    disk=man.IterativeIntAppend(sequence,0)
    j=2
    i=0
    while i < (len(time)-2):
        stamp_number.append(int(j))
        interval=time[i+1]-time[i]
        if interval*(60*60*24) > rate:
            point=(interval*(60*60*24))/rate
            point=np.around(point,decimals=0)
            j+=point
        else:
            j+=1
        i+=1
    name='node{0}/generated_sequence.dat'.format(n)
    man.WriteFileCols(stamp_number,disk,name)
    print 'Wrote node{0} generated sequence file'.format(n)
    n+=1
