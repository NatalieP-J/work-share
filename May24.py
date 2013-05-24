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


if time==None and n==None:
    print 'Please choose a time or a number of measurements per orbit.'
if time==None:
    time=np.linspace(0,orb*2*P*np.pi,n*orb)

#Question 1
#problem here - this function assumes that the major axis is in the direction of right ascension.

def apparent_orbit(t,ti,a,p,v,u,ang,rot):
    output=[]
    b=a*np.cos(ang)
    x=a*np.cos((t-ti)/p)
    y=b*np.sin((t-ti)/p)
    mod_x=x*np.sin(rot)-y*np.cos(rot)+v*(t-ti)
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

print ran_ra
print len(ran_ra)

ran_dec=values[:,1]
ran_dec=ran_dec[:,0]

print ran_dec
print len(ran_dec)

b=maj*np.cos(i)
x=maj*np.cos((time-t_0)/P)
y=b*np.sin((time-t_0)/P)
mod_x=x*np.sin(l)-y*np.cos(l)+ra_pm*(time-t_0)
mod_y=x*np.cos(l)+y*np.sin(l)+dec_pm*(time-t_0)
print mod_x
print len(mod_x)
print mod_y
print len(mod_y)

print ran_ra-mod_x

#Question 3
class func:
    def __init__(self,ang,rot):
        self.ang=ang
        self.rot=rot
    def residual(self,x,y):
        mi=maj*np.cos(self.ang)
        el_x=maj*np.cos((time-t_0)/P)
        el_y=mi*np.sin((time-t_0)/P)
        mod_x=el_x*np.sin(self.rot)-el_y*np.cos(self.rot)+ra_pm*(time-t_0)
        mod_y=el_x*np.cos(self.rot)+el_y*np.sin(self.rot)+dec_pm*(time-t_0)
        mod_x=np.array(mod_x)
        mod_y=np.array(mod_y)
        res_y=y-mod_y
        res_x=x-mod_x
        return (np.sqrt((res_x)**2),np.sqrt((res_y)**2))

f=func(1,1)

plsq=leastsq(f.residual,(1,1),args=(ran_ra,ran_dec))

print plsq


fig=plt.figure()
ax=fig.add_subplot(111)
ax.plot(ran_ra,ran_dec,'o',color='red')
ax.plot(ra,dec,'o',color='blue')
plt.show()

