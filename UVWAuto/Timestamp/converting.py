import astropy.units as u
from astropy.time import Time
import manage as man
import observability
import numpy as np
import sys

def WriteFileCols(values1,values2,fname):
    with open(fname,"w") as data:
        for i in range(len(values1)):
            data.write("{0}\t{1}\n".format(values1[i],values2[i]))

try:
#file path
    fname=sys.argv[1]
#name of converted file
    name=sys.argv[2]

#File is formatted with spaces in between year, month, day etc. For some reason
# the seconds and anything less than seconds are also specified separately
#Loading in the data provides an array where each element has format [yyyy mm d
# hh mm ss 0.lessthanseconds]

    times=man.LoadData(fname)

#make lists for each element - these will be combined later into a format 
# astropy can recognize
    year=man.IterativeStrAppend(times,0)
    month=man.IterativeStrAppend(times,1)
    day=man.IterativeStrAppend(times,2)
    hour=man.IterativeStrAppend(times,3)
    minute=man.IterativeStrAppend(times,4)

#put the seconds back together
    seconds=[]
    for i in range(len(times)-2):
        a=man.IterativeIntAppend(times,5)
        b=man.IterativeFloatAppend(times,6)
        point=a[i]+b[i]
        seconds.append(point)

#formatting for astropy
    time=[]
    for i in range(len(times)-2):
        point="{0}-{1}-{2} {3}:{4}:{5}".format(year[i],month[i],day[i],hour[i],minute[i],seconds[i])
        time.append(point)

#create Modified Julian Date time object
    t=Time(time, format='iso',scale='utc')
    mjd=t.mjd

    tjd=mjd-40000 #Convert modified Julian Date to truncated Julian Date
    ist_fix=mjd-(5.5/24)

#Create an astropy Time object that includes the coordinates of GMRT
    mjd = Time(ist_fix, format='mjd', scale='utc')


#convert the mjd to Greenwich mean sidereal time
    gmst=observability.time2gmst(mjd)
    rad_gmst=gmst*(np.pi/12)

    WriteFileCols(tjd,rad_gmst,name)

except IndexError:
    print "Usage: python converting.py <file to be converted> <output file>"

except IOError:
    print "Enter a valid path to an existing file to be converted."
