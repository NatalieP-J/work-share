import manage as man
import sys

def WriteFileCols(values1,values2,fname):
    with open(fname,"w") as data:
        for i in range(len(values1)):
            data.write("{0}\t{1}\n".format(values1[i],values2[i]))

def LoadDataSpace(fname):
    f=open(fname,'r')
    data=[]
    for line in f.readlines():
        data.append(line.replace('\n','').split('  '))
    f.close()
    return data

fname=sys.argv[1]

data=LoadDataSpace(fname)
data=data[0:65]
glomp=man.IterativeStrAppend(data,4)
antenna=man.IterativeIntAppend(data,1)

frequency=156.*1e6 #per Greg's email
speed=299792458.0 #from astropy
wvlength=speed/frequency


#NOTE THAT THIS VALUE MAY NEED TO BE NEGATIVE
delay=[]
for i in range(len(glomp)):
    point=float(glomp[i][:-9])*wvlength
    delay.append(point)


WriteFileCols(antenna,delay,"delay_{0}".format(fname))
