import numpy as np
from astropy.time.sofa_time import iau_gd2gc
import manage as man
import sys

cos=np.cos
sin=np.sin
atan=np.arctan
atan2=np.arctan2

def km(values):
    newlist=[]
    for i in range(len(values)):
        x=values[i][0]/1000
        y=values[i][1]/1000
        z=values[i][2]/1000
        point=[x,y,z]
        newlist.append(point)
    return newlist

#basically copied outright from its C implementation in SOFA
def iauGd2gce(values):
    newlist=[]
    a=6378137.0 #semi-major axis from WGS84
    inv_f=298.257223563 #inverse of the flattening from WGS84
    for i in range(len(values)):
        lat=values[i][0] #phi in the source code - in radians
        lon=values[i][1] #elon in the source code - in radians
        height=values[i][2] #height in metres
        sp=sin(lat)
        cp=cos(lat)
        f=1/inv_f
        w=1-f
        w=w*w
        d=cp*cp+w*sp*sp
        ac=a/np.sqrt(d)
        a_s=w*ac
        r=(ac+height)*cp
        x=r*cos(lon)
        y=r*sin(lon)
        z=(a_s+height)*sp
        point=[x,y,z]
        newlist.append(point)
    return newlist

#inverse of the above function
def iauGc2gde(values):
    newlist=[]
    a=6378137.0 #from WGS84
    inv_f=298.257223563 #from WGS84
    f=1/inv_f
    for i in range(len(values)):
        x=values[i][0]
        y=values[i][1]
        z=values[i][2]
        aeps2=a*a*1e-32
        e2=(2-f)*f
        e4t=e2*e2*1.5
        ec2=1-e2
        ec=np.sqrt(ec2)
        b=a*ec
        p2=(x*x)+(y*y)
        if p2 !=0:
            lon=atan2(y,x)
        else:
            lon=0
        absz=np.abs(z)
        if p2 > aeps2:
            p=np.sqrt(p2)
            s0=absz/a
            pn=p/a
            zc=ec*s0
            c0=ec*pn
            c02=c0*c0
            c03=c02*c0
            s02=s0*s0
            s03=s02*s0
            a02=c02+s02
            a0=np.sqrt(a02)
            a03=a02*a0
            d0=(zc*a03)+(e2*s03)
            f0=(pn*a03)-(e2*c03)
            b0=e4t*s02*c02*pn*(a0-ec)
            s1=(d0*f0)-(b0*s0)
            cc=ec*(f0*f0-b0*c0)
            phi=atan(s1/cc)
            s12=s1*s1
            cc2=cc*cc
            height=((p*cc)+(absz*s1)-(a*np.sqrt(ec2*s12+cc2)))/np.sqrt(s12+cc2)
        else:
            phi=np.pi/2
            height=absz-b
        if z < 0:
            phi=-phi
        point=[phi,lon,height]
        newlist.append(point)
    return newlist

def convert_iau_gd2gc(values):
    n=1 # refers to WGS84 reference ellipsoid
    newlist=[]
    for i in range(len(values)):
        lat=values[i][0]
        lon=values[i][1]
        height=values[i][2]
        point=iau_gd2gc(n,lon,lat,height)
        newlist.append(point)
    return newlist

gmrt_gc=[1656318.94,5797865.99,2073213.72]
aro_gc=[918013.75,-4346166.16,4561993.93] 
eff_gc=[4033949.50, 486989.40, 4900430.8]
lofar_gc=[3826577.462, 461022.624, 461022.624]  

gc_coords=[aro_gc,gmrt_gc,eff_gc]

aro_gd=[0.802074,4.920553,260.4]
gmrt_gd=[0.333297,1.292411,407.0]
eff_gd=[0.88182470,0.12014168,416.72]
gmrt_gd_1=[0.33323752922569944, 1.2924253519073263, 407]

gd_coords=[aro_gd,gmrt_gd,eff_gd,gmrt_gd_1]

gen_gc_coords=iauGd2gce(gd_coords)
    
differences_iauGd2gce=[]
for i in range(len(gc_coords)):
    diff=[]
    for j in range(len(gc_coords[i])):
        point=(gen_gc_coords[i][j]-gc_coords[i][j])
        diff.append(point)
    differences_iauGd2gce.append(diff)

gen_gc_coords=convert_iau_gd2gc(gd_coords)

differences_iau_gd2gc=[]
for i in range(len(gc_coords)):
    diff=[]
    for j in range(len(gc_coords[i])):
        point=(gen_gc_coords[i][j]-gc_coords[i][j])
        diff.append(point)
    differences_iau_gd2gc.append(diff)
