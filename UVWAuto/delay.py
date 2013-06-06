import manage as man
import sys

def WriteFileCols(values1,values2,values3,fname):
    with open(fname,"w") as data:
        for i in range(len(values1)):
            data.write("{0}\t{1}\t{2}\n".format(values1[i],values2[i],values3[i]))

def LoadDataSpace(fname):
    f=open(fname,'r')
    data=[]
    for line in f.readlines():
        data.append(line.replace('\n','').split('  '))
    f.close()
    return data

fname=sys.argv[1]

data=LoadDataSpace(fname)

glomp=man.IterativeStrAppend(data,4)
antenna=man.IterativeIntAppend(data,1)

direc=[]
delay=[]
for i in range(len(glomp)):
    point=float(glomp[i][-9:])
    direc.append(point)
    point=float(glomp[i][:-9])
    delay.append(point)


WriteFileCols(antenna,delay,direc,"delay_{0}".format(fname)))
