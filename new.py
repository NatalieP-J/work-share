import scipy.optimize
from scipy.optimize import leastsq
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import argparse

parser=argparse.ArgumentParser()

parser.add_argument('--i', type=float, help=''' The inclination of the orbit in arcseconds'''
)

parser.add_argument('--l', type=float, help=''' The longitude of the ascending node in arcseconds'''
)

parser.add_argument('--meas', type=int, help=''' The number of equally spaced measurements taken over the course of one orbit.'''
)

parser.add_argument('--T', type=float, required=True, help=''' The period of the orbit in seconds. '''
)

parser.add_argument('--a', type=float, required=True, help=''' The length of the projected semi-major axis of the system in arcseconds.'''
)

parser.add_argument('--t_0', type=float, help=''' The time of ascending node in seconds.'''
)
args=parser.parse_args()

#Defining variables from input
i=args.i
l=args.l
n=args.meas
T=args.T
a=args.a
t_0=args.t_0

time=np.linspace(0,2*np.pi,n)

#Apparent orbit
#need apparent major and minor axes
#inclination=inverse cosine(apparent minor/apparent major)

maj=a
mi=maj*np.cos(i)

def apparent_orbit(input):
    output=[]
    ra=maj*np.cos(input/T)*np.cos(l)
    dec=mi*np.sin(input/T)*np.sin(l)
    point=[ra,dec]
    output.append(point)
    return output

points=np.array(apparent_orbit(time))
ra=points[:,0]
dec=points[:,1]
max_ra=max(ra)
min_ra=min(ra)
plt.plot(ra,dec,'o',color='blue')
plt.xlabel('right ascension relative to the centre of the orbit in arcseconds')
plt.ylabel('declination relative to the centre of the orbit in arcseconds')
plt.xlim(-maj,maj)
plt.ylim(-maj,maj)
plt.show()
#errors

#ex=np.random.normal(loc=ra,scale=1e-10)
#ey=np.random.normal(loc=dec,scale=1e-6)
    
