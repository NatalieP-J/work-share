from scipy.optimize import leastsq
import numpy as np
from numpy.linalg import eig, inv
import matplotlib.pyplot as plt
import argparse


parser=argparse.ArgumentParser()

#Required arguments
parser.add_argument('--i', type=float, required=True, help=''' The inclination of the orbit in radians.''')
parser.add_argument('--l', type=float, required=True, help=''' The longitude of the ascending node in radians''')
parser.add_argument('--T', type=float, required=True, help=''' The period of the orbit in seconds. ''')
parser.add_argument('--a', type=float, required=True, help=''' The length of the projected semi-major axis of the system in arcseconds.''')
parser.add_argument('--t_0', type=float, default=0, help=''' The time of ascending node in seconds.''')

#Optional arguments
#Either --time or --meas is required
parser.add_argument('--time', type=float, help=''' A time in the orbit relative to the time of ascending node.''')
parser.add_argument('--meas', type=int, default=10, help=''' The number of equally spaced measurements taken over the course of one orbit.''')
parser.add_argument('--orb', type=float, default=1, help=''' The number of orbits the star completes. Default value is one.''')
parser.add_argument('--rapm', type=float, default=0, help=''' The proper motion of the orbit in the direction of right ascension''')
parser.add_argument('--decpm', type=float, default=0, help=''' The proper motion of the orbit in the direction of declination''')


args=parser.parse_args()

#Defining variables from input
i=args.i
l=args.l
n=args.meas
P=args.T
maj=args.a
t_0=args.t_0
time=args.time
orb=args.orb
ra_pm=args.rapm
dec_pm=args.decpm

if time==None:
    time=np.linspace(0,orb*2*P*np.pi,n*orb)

#Question 1
#problem here - this function assumes that the major axis is in the direction of right ascension.

def apparent_orbit(t,ti,a,p,v,u,ang,rot):
    output=[]
    b=a*np.cos(ang)
    x=a*np.cos((t-ti)/p)
    y=b*np.sin((t-ti)/p)
    mod_x=-x*np.sin(rot)+y*np.cos(rot)+v*(t-ti)
    mod_y=x*np.cos(rot)+y*np.sin(rot)+u*(t-ti)
    point=[mod_x,mod_y]
    output.append(point)
    return output

points=np.array(apparent_orbit(time,t_0,maj,P,ra_pm,dec_pm,i,l))
ra=points[:,0]
dec=points[:,1]


try: 
    len(time)
    plt.plot(ra,dec,'o',color='blue')
    plt.xlabel('right ascension relative to the centre of orbit in arcseconds')
    plt.ylabel('declination relative to the centre of orbit in arcseconds')
    #plt.show()
except TypeError:
    for i in range(len(ra)):
        print 'The right ascension relative to the centre of orbit is:'
        print str(ra[i]) + ' arcseconds'
    for i in range(len(dec)):
        print 'The declination relative to the centre of orbit is:'
        print str(dec[i]) + ' arcseconds'

#Question 2


#Question 3

def residuals(p,y,t):
    ang,rot=p
    mi=maj*np.cos(ang)
    el_x=maj*np.cos((t-t_0)/P)
    el_y=mi*np.sin((t-t_0)/P)
    mod_x=-el_x*np.sin(rot)+el_y*np.cos(rot)+ra_pm*(t-t_0)
    mod_y=el_x*np.cos(rot)+el_y*np.sin(rot)+dec_pm*(t-t_0)
    err=y-mod_y
    return err

p0=[1,1]

plsq=leastsq(residuals,p0[:],args=(ran_dec,time))
print plsq[0]

#Randomizing x and y
def Randomize(x,y):
    output=[]
    mod_x=np.random.normal(loc=x,scale=1e-10)
    mod_y=np.random.normal(loc=y,scale=1e-5)
    point=[mod_x,mod_y]
    output.append(point)
    return output

values=np.array(Randomize(ra,dec))

ran_ra=values[:,0]
ran_ra=ran_ra[:,0]


ran_dec=values[:,1]
ran_dec=ran_dec[:,0]


fig=plt.figure()
ax=fig.add_subplot(111)
ax.plot(ran_ra,ran_dec,'o',color='red')
ax.plot(ra,dec,'o',color='blue')
#plt.show()


#Question 3

def residuals(p,y,t):
    ang,rot=p
    mi=maj*np.cos(ang)
    el_x=maj*np.cos((t-t_0)/P)
    el_y=mi*np.sin((t-t_0)/P)
    mod_x=-el_x*np.sin(rot)+el_y*np.cos(rot)+ra_pm*(t-t_0)
    mod_y=el_x*np.cos(rot)+el_y*np.sin(rot)+dec_pm*(t-t_0)
    err=y-mod_y
    return err

x=np.linspace(0,10)
y_true=3*x+1
y_meas=np.random.normal(loc=y,scale=0.1)

def residual(p,y,x):
    m,b=p
    err=y-(m*x+b)
    return err

p0=[3,1]

plsq=leastsq(residual,p0,args=(y_meas,x))
print plsq[0]
