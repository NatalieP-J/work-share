import astropy.units as u
from astropy.time import Time
import manage as man
import observability
import numpy as np
import sys

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
    a=man.IterativeFloatAppend(times,5)
    b=man.IterativeFloatAppend(times,6)

#put the seconds back together
    seconds=[]
    for i in range(len(times)):
        point=a[i]+b[i]
        seconds.append(point)
        print 'Seconds {0} percent done'.format((float(i)/len(times))*100)
        
    print 'Done reading in times'
#formatting for astropy
    time=[]
    for i in range(len(times)):
        point="{0}-{1}-{2} {3}:{4}:{5}".format(year[i],month[i],day[i],hour[i],minute[i],seconds[i])
        time.append(point)
        print 'Formatting {0} percent done'.format((float(i)/len(times))*100)

#create Modified Julian Date time object
    t=Time(time, format='iso',scale='utc')
    mjd=t.mjd

    tjd=mjd-40000 #Convert modified Julian Date to truncated Julian Date
    
    tjd_utc=tjd-(5.5/24)
    
    man.WriteFile(tjd_utc,name)
except IOError:
    print "Please enter a file to be converted and the name of the output file"
