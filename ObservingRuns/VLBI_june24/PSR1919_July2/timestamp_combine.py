import manage as man 
from astropy.time import Time
import numpy as np
def WriteFileCols(values,fname):
    with open(fname,"w") as data:
        for i in range(len(values)):
            data.write("{0}\t{1}\n".format(values[i][0],values[i][1]))

diff=[]
n=33
while n < 40:
    mastertime=[]
    j=1
    while j<5:
        fname='node{0}/timestamp_voltage.all.0329_june29.{1}.dat'.format(n,j)
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
            print "Done node{0}/timestamp_voltage.all.0329_june29.{1}.dat".format(n,j)
            j+=1 
        except IOError:
            print "Missing node{0}/timestamp_voltage.all.0329_june29.{1}.dat".format(n,j)
            j+=1
            pass

    mastertime.sort()
    name='node{0}_july2/MasterTimeStamp.dat'.format(n)
    WriteFileCols(mastertime,name)
    print 'Done master time stamp node{0}'.format(n)
    n+=1
