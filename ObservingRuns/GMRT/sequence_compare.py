import manage as man

n=33
while n < 49:
    try:
        fname='node{0}/generated_sequence.dat'.format(n)
        gen_sequence=man.LoadData(fname)
        gen_stamp=man.IterativeIntAppend(gen_sequence,0)
        fname='node{0}/sequence.sorted.dat'.format(n)
        sequence=man.LoadData(fname)
        k=0
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
                        if point != difference[i-1]:
                            k+=1
                i+=1
            print '\t{0} mismatched timestamps'.format(k)
        else:
            print 'Generated time stamp longer than actual file for node{0}'.format(n)
        name='node{0}/sequence_difference.dat'.format(n)
        man.WriteFile(difference,name)
        n+=1
    except IOError:
        print 'Missing sequence file on node{0}'.format(n)
        n+=1
        pass
   
    
