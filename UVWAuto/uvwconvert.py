import numpy as np
import manage as man

# ************* TEST AGAINST WRITEUVCOORD DID NOT WORK *********************

####CHANGE THIS FOR SOURCE: INPUT IN RADIANS####
#May 16 2013: b1919+21
ra=5.0715791948861657 
dec=0.38240013618954616
TJD_GMST=man.LoadData('tjd2gst/4minMay16first1919GST.dat')
################################################

sin=np.sin
cos=np.cos
GST=man.IterativeFloatAppend(TJD_GMST,1)

#this program takes a set of X Y Z coordinates for various antennas or 
#observatories, calculates their baselines with respect to a given observatory
#for now, this reference point will be ARO because that it the location of 
#writing
#start out with only two observatories and work up from there

#ABOUT THE OBSERVATORIES

gmrt=[1656318.94,5797865.99,2073213.72]
gmrt_lon=(74+(2./60)+(59.07/3600))*(np.pi/180)
aro=[915400.53,-4333785.13,4579662.37]
aro_lon=(78+(4./60)+(22.95/3600))*(np.pi/180)
eff=[4033949.5,486989.4,4900430.8]
eff_lon=(6+(52./60)+(58./3600))*(np.pi/180)
observatories=[aro,gmrt,eff]
lon=[aro_lon,gmrt_lon,eff_lon]

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

baseline=Baseline(observatories)

#TESTING CONSISTENCY
antenna=man.LoadData('data/pycoords60_2013.dat')
for i in range(len(antenna)):
    antenna[i].pop(3)
baseline_test=[]    
for i in range(len(antenna)):
    points=[]
    for j in range(len(antenna[i])):
        point=float(antenna[i][j])
        points.append(point)
    baseline_test.append(points)

baseline_test=Baseline(baseline_test)

lon_test=gmrt_lon

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
        timeset=[]
        for j in range(len(longitude)):
            hour=GST[i]-longitude[j]-RA
            timeset.append(hour)
        newlist.append(timeset)
    return newlist

hour=HourAngle(GST,lon,ra)

def HourAngleTest(GMST,longitude,RA):
    newlist=[]
    for i in range(len(GMST)):
        hour=GST[i]-longitude-RA
        newlist.append(hour)
    return newlist

hour_test=HourAngleTest(GST,lon_test,ra)
            
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

def UVWTest(BL,h,d):
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
uvw_test=UVWTest(baseline_test,hour_test,dec)           

#this function writes the results to file for future examination 
#it is the WriteFile function in manage.py modified for a list of lists
def WriteFile(values1,fname):
    with open(fname,"w") as data:
        for i in range(len(values1)):
            data.write("u coordinate\t v coordinate\t w coordinate\n")
            for j in range(len(values1[i])):
                data.write("{0}\t{1}\t{2}\n".format(values1[i][j][0],values1[i][j][1],values1[i][j][2]))

WriteFile(uvw_test,'AntennaCoordinates.dat')



#########TROUBLESHOOTING#########
def Diff(values1,values2):
    newlist=[]
    for i in range(len(values1)):
        point=values1[i]-values2[i]
        newlist.append(point)
    return newlist

correct=man.LoadData('4minMay16first1919UVW.dat')
writeuv=man.IterativeFloatAppend(correct,8)
writeuv=writeuv[:-30]

def Format(values,index):
    newlist=[]
    for i in range(len(values)):
        for j in range(len(values[i])):
            point=values[i][j][index]
            newlist.append(point)
    return newlist

delay=Format(uvw_test,2)

diff=Diff(writeuv,delay) 

def WriteFileCols(values1,values2,values3,fname):
    with open(fname,"w") as data:
        for i in range(len(values1)):
            data.write('{0}\t{1}\t{2}\n'.format(values1[i],values2[i],values3[i]))

WriteFileCols(delay,writeuv,diff,'AntennaComparisonTest.dat')

def TrimList(values,iteration):
    i=0
    totlist=[]
    while i < (len(values)-1):
        newlist=[]
        if i+iteration < len(values):
            newlist.append(values[i])
            i+=iteration
        else:
            totlist.append(newlist)

change_diff=TrimList(diff,30)
