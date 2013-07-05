import manage as man
import numpy as np
nanoseconds=15.
samples=2.**24
rate=(nanoseconds/10**9)*samples
timestamp=[]
master=[]
n=33
while n<49:
    dupe_test=True
    print 'Writing node{0} generated sequence file'.format(n)
    stamp_number=[]
    fname='node{0}/SequencedTimeStamp.dat'.format(n)
    sequence=man.LoadDataTab(fname)
    time=man.IterativeFloatAppend(sequence,1)
    disk=man.IterativeIntAppend(sequence,0)
    j=2
    stamp_number.append(int(j))
    i=0
    k=0
    duplicates=[' ']*len(time)
    while j < (len(time)):
        while i < (len(time)-2):
            interval=time[i+1]-time[i]
            if interval == 0:
                print '\tduplicate at sequence {0}'.format(int(j))
                dupe_test=False
                stamp_number.append(int(j))
                i+=2
            if interval > rate:
                point=interval/rate
                point=np.around(point,decimals=0)
                j+=point
                if point > 1:
                    k+=(point-1)
                stamp_number.append(int(j))
                i+=1
            else:
                j+=1
                stamp_number.append(int(j))
                i+=1
    check=man.Differences(stamp_number)
    for k in range(len(check)):
        if check[k]==0:
            duplicates[k]='duplicate'
            duplicates[k+1]='duplicate'
    name='node{0}/generated_sequence.dat'.format(n)
    man.WriteFile3Cols(stamp_number,disk,duplicates,name)
    print '\tMissed {0} time stamps total'.format(int(k))
    if dupe_test is False:
        print '\tDuplicates exist'
    n+=1
