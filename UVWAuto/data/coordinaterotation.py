import numpy as np
import manage as man
cos=np.cos
sin=np.sin
#rotating coordinates into xyz frame
gmrt_lon=(74+(2./60)+(59.07/3600))*(np.pi/180)

def LoadData(fname):
    f=open(fname,'r')
    data=[]
    for line in f.readlines():
        data.append(line.replace('\n','').split('\t'))
    f.close()
    return data

def WriteFileCols(values1,values2,fname):
    with open(fname,"w") as data:
        for i in range(len(values1)):
            data.write("{0}\t{1}\n".format(values1[i],values2[i]))

data=LoadData('coords30_2013_gmrt.dat')
x=man.IterativeFloatAppend(data,1)
y=man.IterativeFloatAppend(data,0)

def rotate_x_ccw(values1,values2,longitude):
    newlist=[]
    for i in range(len(values1)):
        a=values1[i]
        b=values2[i]
        mod_val=a*cos(longitude)-b*sin(longitude)
        newlist.append(mod_val)
    return newlist
def rotate_y_ccw(values1,values2,longitude):
    newlist=[]
    for i in range(len(values1)):
        a=values1[i]
        b=values2[i]
        mod_val=a*sin(longitude)+b*cos(longitude)
        newlist.append(mod_val)
    return newlist
def rotate_x_cw(values1,values2,longitude):
    newlist=[]
    for i in range(len(values1)):
        a=values1[i]
        b=values2[i]
        mod_val=a*cos(longitude)+b*sin(longitude)
        newlist.append(mod_val)
    return newlist
def rotate_y_cw(values1,values2,longitude):
    newlist=[]
    for i in range(len(values1)):
        a=values1[i]
        b=values2[i]
        mod_val=-a*sin(longitude)+b*cos(longitude)
        newlist.append(mod_val)
    return newlist

x_prime=rotate_x_ccw(x,y,gmrt_lon)
y_prime=rotate_y_ccw(x,y,gmrt_lon)
#Matches our exisiting coordinates
WriteFileCols(x_prime,y_prime,'CounterClockwiseRotation.dat')
x_prime=rotate_x_cw(x,y,gmrt_lon)
y_prime=rotate_y_cw(x,y,gmrt_lon)
#Not a match for existing coordinates
WriteFileCols(x_prime,y_prime,'ClockwiseRotation.dat')
