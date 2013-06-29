import astropy.units as u
import manage as man

c=299792458.0

def LoadData(fname):
    f=open(fname,'r')
    data=[]
    for line in f.readlines():
        data.append(line.replace('\n','').split('\t'))
    f.close()
    return data

data=LoadData('AntennaCableDelay.dat')
data.pop(0)
delay0=man.IterativeFloatAppend(data,0)
delay1=man.IterativeFloatAppend(data,1)
for i in range(len(delay1)):
    delay0.append(delay1[i])
def MicroSeconds(values):
    newlist=[]
    for i in range(len(values)):
        point=(values[i]/c)*10**6
        newlist.append(point)
    return newlist
delay=MicroSeconds(delay0)

man.WriteFile(delay,'AntennaCableDelayMs.dat')
