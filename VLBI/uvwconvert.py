import numpy as np
import manage as man
from astropy.time import Time
from astropy.constants import c
from astropy import units as units
import sys

def FloatMaker(values):
    newlist=[]
    for i in range(len(values)):
        point=float(values[i])
        newlist.append(point)
    return newlist

#import from command line the file containing the GST's and an output file
name_GST=sys.argv[1]
name_out=sys.argv[2]

####CHANGE THIS FOR SOURCE: INPUT IN RADIANS####
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
TJD_GMST=man.LoadData(str(name_GST))
sin=np.sin
cos=np.cos
GST=man.IterativeFloatAppend(TJD_GMST,1)
TJD=man.IterativeFloatAppend(TJD_GMST,0)
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
aro_lon=float(data[9][1])
gmrt=data[2][:3]
gmrt=FloatMaker(gmrt)
gmrt_lon=float(data[10][1])
eff=data[4][:3]
eff=FloatMaker(eff)
eff_lon=float(data[11][1])
observatories=[aro,gmrt,eff]
lon=[aro_lon,gmrt_lon,eff_lon]



#function takes a list of coordinate sets (a list of (x,y,z) points) and finds
#the baseline of each set with respect to the first one
def Baseline(coords,index):
    newlist=[]
    for i in range(len(coords)):
        x=coords[index][0]-coords[i][0]
        y=coords[index][1]-coords[i][1]
        z=coords[index][2]-coords[i][2]
        baseline=[x,y,z]
        newlist.append(baseline)
    return newlist

baseline=Baseline(observatories,0)

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

baseline_gmrt=Baseline(baseline_gmrt,2)

lon_gmrt=gmrt_lon

#now that we have baselines, we want to convert X Y Z system to u v w system and
#extract the w value

#ABOUT THE SOURCE
#import GST from timestamp files run through tjd2gst
#hour = hour angle relative to local meridian
#dec = declination relative to the celestial equator

#this function takes a list of Greenwich mean sidereal times, a list of 
#longitudes and right ascension (all in radians), and calculates the hour angle
#(also in radians) at each longitude for each time
def HourAngle(GMST,longitude,RA):
    newlist=[]
    for i in range(len(GMST)):
        check_values=[]
        for j in range(len(longitude)):
            hour=GST[i]-longitude[j]-RA
            check_values.append(hour)
        newlist.append(check_values)
    return newlist

hour=HourAngle(GST,lon,ra)

def HourAngleGMRT(GMST,longitude,RA):
    newlist=[]
    for i in range(len(GMST)):
        hour=GST[i]-longitude-RA
        newlist.append(hour)
    return newlist

hour_gmrt=HourAngleGMRT(GST,lon_gmrt,ra)
            
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
            v=-B_x*sin(d)*cos(h[j][i])+B_y*sin(d)*sin(h[j][i])+B_z*cos(d)
            w=B_x*cos(d)*cos(h[j][i])-B_y*cos(d)*sin(h[j][i])+B_z*sin(d)
            uvw=[u,v,w]
            timeset.append(uvw)
        newlist.append(timeset)
    return newlist

uvw=UVW(baseline,hour,dec)

def UVWGMRT(BL,h,d):
    newlist=[]
    for j in range(len(h)):
        timeset=[]
        for i in range(len(BL)):
            B_x=BL[i][0]
            B_y=BL[i][1]
            B_z=BL[i][2]
            u=B_x*sin(h[j])+B_y*cos(h[j])
            v=-B_x*sin(d)*cos(h[j])+B_y*sin(d)*sin(h[j])+B_z*cos(d)
            w=B_x*cos(d)*cos(h[j])-B_y*cos(d)*sin(h[j])+B_z*sin(d)
            uvw=[u,v,w]
            timeset.append(uvw)
        newlist.append(timeset)
    return newlist
uvw_gmrt=UVWGMRT(baseline_gmrt,hour_gmrt,dec)           

def microseconds(values):
    masterlist=[]
    for i in range(len(values)):
        newlist=[]
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
        masterlist.append(newlist)
    return masterlist
            
ms_gmrt=microseconds(uvw_gmrt)
ms_vlbi=microseconds(uvw)

#this function writes the results to file for future examination 
#it is the WriteFile function in manage.py modified for a list of lists
def WriteFile(values,fname):
    with open(fname,"w") as data:
        for i in range(len(values)):
            for j in range(len(values[i])):
                data.write("{0}\n".format(values[i][j][2]))

WriteFile(uvw_gmrt,'GMRT_metres_{0}'.format(name_out))
WriteFile(ms_gmrt,'GMRT_microsec_{0}'.format(name_out))
WriteFile(uvw,'VLBI_metres_{0}'.format(name_out))
WriteFile(ms_vlbi,'VLBI_microsec_{0}'.format(name_out))


