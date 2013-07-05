import numpy as np
from astropy.time.sofa_time import iau_gd2gc
import manage as man
import sys

cos=np.cos
sin=np.sin

gmrt_gc=[1656318.94,5797865.99,2073213.72]
aro_gc=[915400.53,-4333785.13,4579662.37] 
eff_gc=[4033949.50, 486989.40, 4900430.8] 

gc_coords=[aro_gc,gmrt_gc,eff_gc]

aro_gd=[0.802074,4.920553,260.4]
gmrt_gd=[0.333297,1.292411,660.0]
eff_gd=[0.881823,0.12027,319.0]

lon=[aro_gd[1],gmrt_gd[1],eff_gd[1]]

gd_coords=[aro_gd,gmrt_gd,eff_gd]

n=1

def gd2gc_coords(values):
    newlist=[]
    for i in range(len(values)):
        lat=values[i][0]
        lon=values[i][1]
        R=6378136.+values[i][2]
        x=R*cos(lat)*cos(lon)
        y=R*cos(lat)*sin(lon)
        z=R*sin(lat)
        point=[x,y,z]
        newlist.append(point)
    return newlist

gd2gc=gd2gc_coords(gd_coords)
    
differences1=[]
for i in range(len(gc_coords)):
    diff=[]
    for j in range(len(gc_coords[i])):
        point=(gd2gc[i][j]-gc_coords[i][j])
        diff.append(point)
    differences1.append(diff)

def find_R(values):
    newlist=[]
    for i in range(len(values1,values2)):
        X=values[i][0]
        Y=values[i][1]
        Z=values[i][2]
x=[]
y=[]
z=[]
gen_gc_coords=[]
for i in range(len(gd_coords)):
    point=iau_gd2gc(n,gd_coords[i][0],gd_coords[i][1],gd_coords[i][2])
    gen_gc_coords.append(point)
    x.append(point[0])
    y.append(point[1])
    z.append(point[2])


differences=[]
for i in range(len(gc_coords)):
    diff=[]
    for j in range(len(gc_coords[i])):
        point=(gen_gc_coords[i][j]-gc_coords[i][j])
        diff.append(point)
    differences.append(diff)

def rotate_x_ccw(valuesx,valuesy,valueslon):
    newlist=[]
    for i in range(len(valuesx)):
        a=valuesx[i]
        b=valuesy[i]
        mod_val=a*cos(valueslon[i])-b*sin(valueslon[i])
        newlist.append(mod_val)
    return newlist
def rotate_y_ccw(valuesx,valuesy,valueslon):
    newlist=[]
    for i in range(len(valuesx)):
        a=valuesx[i]
        b=valuesy[i]
        mod_val=a*sin(valueslon[i])+b*cos(valueslon[i])
        newlist.append(mod_val)
    return newlist
def rotate_x_cw(valuesx,valuesy,valueslon):
    newlist=[]
    for i in range(len(valuesx)):
        a=valuesx[i]
        b=valuesy[i]
        mod_val=a*cos(valueslon[i])+b*sin(valueslon[i])
        newlist.append(mod_val)
    return newlist
def rotate_y_cw(valuesx,valuesy,valueslon):
    newlist=[]
    for i in range(len(valuesx)):
        a=valuesx[i]
        b=valuesy[i]
        mod_val=-a*sin(valueslon[i])+b*cos(valueslon[i])
        newlist.append(mod_val)
    return newlist

x_prime=rotate_x_ccw(x,y,lon)
y_prime=rotate_y_ccw(x,y,lon)

coords=[]
for i in range(len(x_prime)):
    point=[x_prime[i],y_prime[i],z[i]]
    coords.append(point)

differences_ccw=[]
for i in range(len(gc_coords)):
    diff=[]
    for j in range(len(gc_coords[i])):
        point=coords[i][j]-gc_coords[i][j]
        diff.append(point)
    differences_ccw.append(diff)

x_prime=rotate_x_cw(x,y,lon)
y_prime=rotate_y_cw(x,y,lon)

coords=[]
for i in range(len(x_prime)):
    point=[x_prime[i],y_prime[i],z[i]]
    coords.append(point)

differences_cw=[]
for i in range(len(gc_coords)):
    diff=[]
    for j in range(len(gc_coords[i])):
        point=coords[i][j]-gc_coords[i][j]
        diff.append(point)
    differences_cw.append(diff)
