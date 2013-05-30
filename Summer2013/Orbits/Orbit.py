from scipy.optimize import leastsq
import numpy as np
from numpy.linalg import eig, inv
import matplotlib.pyplot as plt
import argparse

#This code takes projected semi-major axis, period, longitude of ascending node
#and inclination and plots a circular orbit of a star with those parameters as 
#it would appear on the sky. It then randomizes the generated points and 
#attempts to fit an elliptical orbit back to it using least squares.


#ASSUMPTIONS
#That the orbit of the pulsar is small enough (ie, a is small) that the sky can
#be approximated as a plane in that region

#That the semi-major axis lies along the direction of right ascension rather 
#than the declination (when writing initial equation for the ellipse). This is 
#quite unfounded, and I am still thinking about how to fix it.

#That the time of ascending node marks the beginning of an orbit (the beginning
#being when the polar angle is zero)  - there is no reason for this to be the 
#case

#That the errors are constant values, and that the smaller error will be in the
#direction of right ascension - again, there is no reason for this to be the 
#case

#OTHER FIXES
#I suspect my use of arrays is unnecessarily complicated and would like to put 
#some time into simplifying them.

#I would like to set up a response that tells you for a given time, how many 
#orbits have passed since the time of ascending node

#Weight the least squares average so a number related to a smaller error has a 
#greater weight

#Create an command line argument parser. 
parser=argparse.ArgumentParser()

#Add command line options
#Required arguments
#Orbital inclination for the generated orbit
parser.add_argument('--i', type=float, required=True, help=''' The inclination of the orbit in radians.''')
#Longitude of the ascending node
parser.add_argument('--l', type=float, required=True, help=''' The longitude of the ascending node in radians''')
#Period of the orbit
parser.add_argument('--T', type=float, required=True, help=''' The period of the orbit in seconds. ''')
#Projected semi-major axis
parser.add_argument('--a', type=float, required=True, help=''' The length of the projected semi-major axis of the system in arcseconds.''')

#Optional arguments
#time of ascending node defaults to zero for the sake of simplicity
parser.add_argument('--t_0', type=float, default=0, help=''' The time of ascending node as a Julian Date.''') 
#time defaults to an interval below
parser.add_argument('--time', type=float, help=''' The Julian Date of a time in the orbit relative to the time of ascending node..''')
#number of measurements per orbit - defaults to 10
parser.add_argument('--meas', type=int, default=10, help=''' The number of equally spaced measurements taken over the course of one orbit.''')
#number of orbits defaults to 1
parser.add_argument('--orb', type=float, default=1, help=''' The number of orbits the star completes. Default value is one.''')
#proper motion in either direction - defaults to zero
parser.add_argument('--rapm', type=float, default=0, help=''' The proper motion of the orbit in the direction of right ascension in arcseconds per second.''')
parser.add_argument('--decpm', type=float, default=0, help=''' The proper motion of the orbit in the direction of declination in arcseconds per second.''')


#Parse the command line arguments
args=parser.parse_args()

#Defining variables from input
i=args.i #inclination
l=args.l #longitude of ascending node
P=args.T #period of orbit
maj=args.a #projected semi major axis
n=args.meas #number of orbit
t_0=args.t_0 #time of ascending node
time=args.time #a particular time at which the orbital position is predicted
orb=args.orb #number of orbits to be simulated
ra_pm=args.rapm #proper motion in the direction of right ascension
dec_pm=args.decpm #proper motion in the direction of declination

if time==None: #if no specific time is specified
    time=np.linspace(t_0,(orb*2*P*np.pi)+t_0,n*orb)
    #set time to be the interval from time of ascending node to the specified 
    #number of orbital periods later, divided into 'n' measurements per orbit

#DEFINING FUNCTIONS

#Define a function that take time, initial time, semi-major axis, period, proper
#motion in the directions of right ascension and declination, inclination and 
#longitude of ascending node and creates a list of points in the orbit

def apparent_orbit(t,ti,a,p,v,u,ang,rot):
    #Define the minor axis of the ellipse in terms of the major axis and the 
    #inclination 
    b=a*np.cos(ang)
    #Write basic parametric equations for an ellipse
    x=a*np.cos((t-ti)/p) 
    y=b*np.sin((t-ti)/p)
    #Now rotate the ellipse according to the longitude of the ascending node 
    #and incorporate the proper motion
    mod_x=-x*np.sin(rot)+y*np.cos(rot)+v*(t-ti)
    mod_y=x*np.cos(rot)+y*np.sin(rot)+u*(t-ti)
    return (mod_x,mod_y)

#Choose random modified x and y from a Gaussian centred at the original 
#point with an standard deviation specified by 'scale' - essentially, choose
#a point within the errors of the original one.

def Randomize(x,y):
    mod_x=np.random.normal(loc=x,scale=1e-10)
    mod_y=np.random.normal(loc=y,scale=1e-7)
    return (mod_x,mod_y)


#A function that calculates the difference between input y values and the y 
#values of an ellipse with parameters ang and rot, two angles that describe its
#eccentricity and rotation around the origin, respectively
#residuals_y takes two parameters, y-values, and time and returns a list
    
def residuals_y(p,y,t):
    #ang and rot are two angles described in the parameter list p
    ang,rot=p
    #the minor axis of the ellipse is related to the major axis by the following
    mi=maj*np.cos(ang)
    #basic parametric equations for an ellipse
    el_x=maj*np.cos((t-t_0)/P)
    el_y=mi*np.sin((t-t_0)/P)
    #modfied y value that has been rotated around the origin and had proper 
    #motion incorporated
    mod_y=el_x*np.cos(rot)+el_y*np.sin(rot)+dec_pm*(t-t_0)
    #the difference between the input y values and y values on an ellipse
    err=y-mod_y
    return err

#A function that calculates the difference between input x values and the x 
#values of an ellipse with parameters ang and rot, two angles that describe its
#eccentricity and rotation around the origin, respectively
#residuals_x takes two parameters, x-values and time and returns a list
    
def residuals_x(p,x,t):
    #ang and rot are two angles described in the parameter list p
    ang,rot=p
    #the minor axis of the ellipse is related to the major axis by the following
    mi=maj*np.cos(ang)
    #basic parametric equations for an ellipse
    el_x=maj*np.cos((t-t_0)/P)
    el_y=mi*np.sin((t-t_0)/P)
    #modified x value that has been rotated around the origin and had proper 
    #motion incorporated
    mod_x=-el_x*np.sin(rot)+el_y*np.cos(rot)+ra_pm*(t-t_0)
    #the difference between the input x values and the x values on an ellipse
    err=x-mod_x
    return err

#QUESTION 1 - PLOTTING AN ORBIT

#recover a list of points from the fuction
points=np.array(apparent_orbit(time,t_0,maj,P,ra_pm,dec_pm,i,l))

#slice the list into right ascension and declination
ra=points[0] 
dec=points[1]

#if time is an interval, rather than a single value, plot the orbit
try: 
    len(time) 
    plt.plot(ra,dec,'o',color='blue',linestyle='none')
    plt.xlabel('right ascension relative to the centre of orbit in arcseconds')
    plt.ylabel('declination relative to the centre of orbit in arcseconds')

#QUESTION 2 - RANDOMIZE THE VALUES IN THE ELLIPSE

    j=0 #an index representing the number of times the fitter has run
    parameters=[] #an empty list to hold the results of each iteration

#Run the fitter 100 times
    while j<100:
#Randomizing right ascension and declination

#recover a list of points from the function
        values=np.array(Randomize(ra,dec)) 

#slice the list into right ascension and declination
        ran_ra=values[0]#randomized right ascension
        ran_dec=values[1]#randomized declination

#QUESTION 3 - FIT AN ELLIPSE TO RANDOM DATA

#initial guess for parameters. p0[0] is inclination, p0[1] is longitude
#this guess is used by the leastsq function
        p0=[i,l]

#minimize the squares of the y residuals, taking input y to be the randomized 
#declination and the guess as given above
#returns an array of the two predicted parameters
        dec_lsq=leastsq(residuals_y,p0,args=(ran_dec,time))

#minimize the squares of the x residuals, taking input x to be the randomized 
#right ascension and the guess as given above
#returns an array of the two predicted parameters
        ra_lsq=leastsq(residuals_x,p0,args=(ran_ra,time))

#take the average of the parameters generates by the optimizing leastsq function
        lsq=np.array((ra_lsq[0]+dec_lsq[0])/2)

#divide lsq into inclination and longitude    
        inclination=lsq[0]
        longitude=lsq[1]

#add each pair to parameters list
        values=[inclination, longitude]
        parameters.append(values)

#increment j to continue to the next iteration
        j+=1

#Extract inclination and longitude into separate lists total_inc and total_long
    total_inc=[]
    total_long=[]
    for i in range(len(parameters)):
        total_inc.append(parameters[i][0])
        total_long.append(parameters[i][1])

#Average each list to find the values for inclination and longitude found by 
#the fitter
    inc = sum(total_inc)/len(total_inc)
    lon = sum(total_long)/len(total_long)

#Calculate the standard deviation over the dataset
    inc_error=[]
    long_error=[]
    for i in range(len(parameters)):
        inc_error.append(abs(total_inc[i]-inclination))
        long_error.append(abs(total_long[i]-longitude))

    inclination_error = sum(inc_error)/len(inc_error)
    longitude_error = sum(long_error)/len(long_error)

#Print the results to the shell
    print ''
    print 'The inclination is: '
    print str(inc) + '+/-' + str(inclination_error)
    print ''
    print 'The longitude of ascending node is: '
    print str(lon) + '+/-' + str(longitude_error)

#Plot the new ellipse
    time=np.linspace(t_0,(orb*2*P*np.pi)+t_0,1000)
    points=np.array(apparent_orbit(time,t_0,maj,P,ra_pm,dec_pm,inc,lon))
    ra=points[0] 
    dec=points[1]
    plt.plot(ra,dec,color='red')
    plt.show()
#if time is a single value, print the right ascension and declination at
#that time
except TypeError:
    print 'The right ascension relative to the centre of orbit is:'
    print str(ra) + ' arcseconds'
    print 'The declination relative to the centre of orbit is:'
    print str(dec) + ' arcseconds'
