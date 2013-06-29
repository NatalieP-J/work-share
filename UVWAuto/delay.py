import manage as man
import sys
import matplotlib.pyplot as plt

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

def LoadData(fname):
    f=open(fname,'r')
    data=[]
    for line in f.readlines():
        data.append(line.replace('\n','').split('\t'))
    f.close()
    return data

fname=sys.argv[1]
data=LoadDataSpace(fname)
c=299792458.0
#data=data[:30]
glomp=man.IterativeStrAppend(data,4)
antenna=man.IterativeIntAppend(data,1)
#uorv=man.IterativeFloatAppend(data,2)
#voru=man.IterativeFloatAppend(data,3)
#frequency=156000000.0 #per Greg's email
#speed=299792458.0 #from astropy
#wvlength=speed/frequency

#NOTE THAT THIS VALUE MAY NEED TO BE NEGATIVE
delay=[]
for i in range(len(glomp)):
    point=((float(glomp[i][:-9])/c)*10**6
    delay.append(point)

#timedat=sys.argv[2]
#data=LoadData(timedat)
#tjd=man.IterativeFloatAppend(data,0)
#mjd=[]
#for i in range(len(tjd)):
    #point=tjd[i]+40000
    #mjd.append(point)

#plt.plot(uorv,delay,'o',color='b')
#plt.plot(voru,delay,'o',color='r')
#plt.show()

WriteFileCols(antenna,delay,"delay_{0}".format(fname))
