import scipy.optimize
from scipy.optimize import leastsq
import numpy as np
from numpy.linalg import eig, inv
import matplotlib
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
def apparent_orbit(t,ti,a,ang,p,rot,v,u):
    output=[]
    b=a*np.cos(ang)
    x=a*np.cos((ti+t)/p)
    y=b*np.sin((ti+t)/p)
    mod_x=y*np.cos(rot)-x*np.sin(rot)+v*(ti+t)
    mod_y=x*np.cos(rot)+y*np.sin(rot)+u*(ti+t)
    point=[mod_x,mod_y]
    output.append(point)
    return output

points=np.array(apparent_orbit(time,t_0,maj,i,P,l,ra_pm,dec_pm))
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
ran_ra=np.random.normal(loc=ra,scale=1e-10)
ran_dec=np.random.normal(loc=dec,scale=1e-4)

print ran_ra
print ran_dec


#Question 3

fig=plt.figure()
ax=fig.add_subplot(111)
ax.plot(ran_ra,ran_dec,'o',color='red')
ax.plot(ra,dec,'o',color='blue')
ax.plot()
plt.show()
