import numpy as np
import manage as man
from astropy.time import Time
from astropy.constants import c
from astropy import units as units
import sys


#function takes a list of coordinate sets (a list of (x,y,z) points) and finds
#the baseline of each set with respect to the first one
def Baseline(coords):
    newlist=[]
    for i in range(len(coords)):
        x=coords[0][0]-coords[i][0]
        y=coords[0][1]-coords[i][1]
        z=coords[0][2]-coords[i][2]
        baseline=[x,y,z]
        newlist.append(baseline)
    return newlist

def FloatMaker(values):
    newlist=[]
    for i in range(len(values)):
        point=float(values[i])
        newlist.append(point)
    return newlist

#this function takes a list of Greenwich mean sidereal times, a list of 
#longitudes and right ascension (all in radians), and calculates the hour angle
#(also in radians) at each longitude for each time
def HourAngle(GMST,RA):
    newlist=[]
    for i in range(len(GMST)):
        hour=GST[i]-RA
        newlist.append(hour)
    return newlist


def microseconds(values):
    newlist=[]
    for i in range(len(values)):
        for j in range(len(values[i])):
            u=values[i][j][0]
            v=values[i][j][1]
            w=values[i][j][2]
            c=299792458.0
            u=(u/c)*1e6
            v=(v/c)*1e6
            w=(w/c)*1e6
            point=[u,v,w]
            newlist.append(point)
    return newlist

           
#this function takes a list of coordinate sets, a list of hour angles at given
#longitudes over time and declination, and outputs u v w coordinates for each 
#longitude over time
def UVW(BL,h,d):
    newlist=[]
    for j in range(len(h)):
        timeset=[]
        for i in range(len(BL)):
            B_x=BL[i][0]
            B_y=BL[i][1]
            B_z=BL[i][2]
            u=B_x*sin(h[j][i])+B_y*cos(h[j][i])
            v=-B_x*sin(d)*cos(h[j])+B_y*sin(d)*sin(h[j])+B_z*cos(d)
            w=B_x*cos(d)*cos(h[j])-B_y*cos(d)*sin(h[j])+B_z*sin(d)
            uvw=[u,v,w]
            timeset.append(uvw)
        newlist.append(timeset)
    return newlist


#this function writes the results to file for future examination 
#it is the WriteFile function in manage.py modified for a list of lists
def WriteFileDelay(values,fname):
    with open(fname,"w") as data:
        for i in range(len(values)):
            for j in range(len(values[i])):
                data.write("{0}".format(values[i][j][2]))




try:


#import from command line the file containing the GST's and an output file
    name_timestamp=sys.argv[1]
    name_out=sys.argv[2] 

#File is formatted with spaces in between year, month, day etc. For some reason
# the seconds and anything less than seconds are also specified separately
#Loading in the data provides an array where each element has format [yyyy mm d
# hh mm ss 0.lessthanseconds]

    times=man.LoadData(name_timestamp)

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

    print 'Done tjd_utc'
    
    

    ###CHANGE THIS FOR SOURCE: INPUT IN RADIANS####
#May 17 2013: b1919+21
ra=5.0715791948861657 
dec=0.38240013618954616
#May 17 2013: b1957+20
#ra=5.2368626022705502
#dec=0.36375085679967373
#June 11 2013: b1937+21
#ra=5.149701586646474
#dec=0.37724768183081842
#June 29 2013: b0329+54
#ra=0.9338347801769575
#dec=0.953358324077975
################################################

sin=np.sin
cos=np.cos

MJD=[]
for i in range(len(TJD)):
    mjd=TJD[i]+40000
    MJD.append(mjd)

t=Time(MJD,format='mjd',scale='utc')
time=t.iso


#this program takes a set of X Y Z coordinates for various antennas or 
#observatories, calculates their baselines with respect to a given observatory
#for now, this reference point will be ARO because that is the location of 
#writing
#start out with only two observatories and work up from there

#ABOUT THE OBSERVATORIES
data=man.LoadDataTab('VLBIantennacoord.dat')
aro=data[3][:3]
aro=FloatMaker(aro)
gmrt=data[2][:3]
gmrt=FloatMaker(gmrt)
eff=data[4][:3]
eff=FloatMaker(eff)
lofar=data[5][:3]
lofar=FloatMaker(lofar)
observatories=[aro,gmrt,eff,lofar]


baseline=Baseline(observatories)

#TESTING CONSISTENCY
antenna=man.LoadData('pycoords60_2013.dat')
for i in range(len(antenna)):
    antenna[i].pop(3)
baseline_gmrt=[]    
for i in range(len(antenna)):
    points=[]
    for j in range(len(antenna[i])):
        point=float(antenna[i][j])
        points.append(point)
    baseline_gmrt.append(points)

baseline_gmrt=Baseline(baseline_gmrt)

#now that we have baselines, we want to convert X Y Z system to u v w system and
#extract the w value

#ABOUT THE SOURCE
#import GST from timestamp files run through tjd2gst
#hour = hour angle relative to local meridian
#dec = declination relative to the celestial equator

hour=HourAngle(GST,ra)
hour_gmrt=HourAngle(GST,ra)
uvw=UVW(baseline,hour,dec)
uvw_gmrt=UVW(baseline_gmrt,hour_gmrt,dec)                       
ms_gmrt=microseconds(uvw_gmrt)
ms_vlbi=microseconds(uvw)

WriteFileDelay(uvw_gmrt,'GMRT_metres_{0}'.format(name_out))
WriteFileDelay(ms_gmrt,'GMRT_microsec_{0}'.format(name_out))
WriteFileDelay(uvw,'VLBI_metres_{0}'.format(name_out))
WriteFileDelay(ms_vlbi,'VLBI_microsec_{0}'.format(name_out))
    
except IOError:
    print "Please enter a file to be converted and the name of the output file"


#


