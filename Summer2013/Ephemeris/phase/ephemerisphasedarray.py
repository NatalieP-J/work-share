import numpy as np
from astropy.time import Time
from astropy.coordinates.angles import Angle
from astropy.constants import c
import astropy.units as u
import de405
import observability
from pulsar import ELL1Ephemeris
from barycentre import JPLEphemeris
import matplotlib.pyplot as plt


deg2rad = np.pi/180.

eph1957 = ELL1Ephemeris('psrj1959.par')
jpleph = JPLEphemeris(de405)
#********adjust 3 min for delay********
mjd = Time('2013-05-16 23:40:00', scale='utc').mjd
mjd = Time(mjd, format='mjd', scale='utc',
           lon=(74*u.deg+02*u.arcmin+59.07*u.arcsec).to(u.deg).value,
           lat=(19*u.deg+05*u.arcmin+47.46*u.arcsec).to(u.deg).value)

start=mjd.tdb.mjd #start time in mjd
time_jd=mjd.tdb.jd #start time in jd
end=(1+(3./60))/24 #length of observations (from timestamp files?)
finish=start+end #end time
delay=[] #empty array to hold delay times
original_delay=[] #empty array to hold delays
original_period=[] #empty array to hold the initial period for each time
doppler_period=[] #empty array to hold doppler shifted period
rv=[] #empty array to hold relative velocities of the system
time_elapsed=[]
time_orig=start
real_time=[]
while time_orig<finish:
    time=time_orig
    print "Time left: {0}\n".format(finish-time) 
    f_p=eph1957.evaluate('F',time,t0par='PEPOCH')#pulse frequency
    P_0=1./f_p #pulse period

     # direction to target
    dir_1957 = eph1957.pos(time)

    # Delay from and velocity of centre of earth to SSB (lt-s and v/c)
    posvel_earth = jpleph.compute('earth', time_jd)
    pos_earth = posvel_earth[:3]/c.to(u.km/u.s).value
    vel_earth = posvel_earth[3:]/c.to(u.km/u.day).value

    d_earth = np.sum(pos_earth*dir_1957, axis=0)
    v_earth = np.sum(vel_earth*dir_1957, axis=0)
    
    time+=d_earth/(3600*24)
    time_jd+=d_earth/(3600*24)

    mjd = Time(time, format='mjd', scale='utc',
           lon=(74*u.deg+02*u.arcmin+59.07*u.arcsec).to(u.deg).value,
           lat=(19*u.deg+05*u.arcmin+47.46*u.arcsec).to(u.deg).value)

    #GMRT from tempo2-2013.3.1/T2runtime/observatory/observatories.dat
    xyz_gmrt = (1656318.94, 5797865.99, 2073213.72)
    # Rough delay from observatory to center of earth
    # mean sidereal time (checked it is close to rf_ephem.utc_to_last)
    lmst = (observability.time2gmst(mjd)/24. + mjd.lon/360.)*2.*np.pi
    coslmst, sinlmst = np.cos(lmst), np.sin(lmst)
    # rotate observatory vector
    xy = np.sqrt(xyz_gmrt[0]**2+xyz_gmrt[1]**2)
    pos_gmrt = np.array([xy*coslmst, xy*sinlmst,
                         xyz_gmrt[2]*np.ones_like(lmst)])/c.si.value
    vel_gmrt = np.array([-xy*sinlmst, xy*coslmst,
                          np.zeros_like(lmst)]
                        )*2.*np.pi*366.25/365.25/c.to(u.m/u.day).value
    # take inner product with direction to pulsar
    d_topo = np.sum(pos_gmrt*dir_1957, axis=0)
    v_topo = np.sum(vel_gmrt*dir_1957, axis=0)
    
    time+=d_topo/(3600*24)
    
    # orbital delay and velocity (lt-s and v/c)
    d_orb = eph1957.orbital_delay(time)
    v_orb = eph1957.radial_velocity(time)
    
   
    #total relative velocity
    total_rv = - v_topo - v_earth + v_orb
    rv.append(total_rv)

    L=(1/(1+total_rv))#multiplying factor to find doppler frequency
    f_dp=f_p*L #doppler shifted frequency
    P_dp=1./f_dp #doppler shifted period
    doppler_period.append(P_dp)
    d_doppler=P_dp-P_0 #delay due to doppler shift

    total_delay = -d_topo - d_earth + d_orb
        
    mjd_delay=total_delay/(60*60*24)#convert from seconds to days
    
    arrival=time_orig+mjd_delay #arrival time
    ist_fix=arrival+(5.5/24)#shifted to Indian Standard Time
    delay.append(ist_fix)
    period=P_dp*(1000./(60*60*24)) 
    time_orig+=period

t = Time(delay,format='mjd',scale='utc',precision=9)
time_ist=t.iso #convert from mjd to iso

    #write the data to file
with open("PhasedArrayArrival.dat","w") as data:
    for i in range(len(time_ist)):
        data.write("{0} \t {1} \n".format(time_ist[i],doppler_period[i]))
freq=[]
for i in range(len(doppler_period)):
    point=1./doppler_period[i]
    freq.append(point)

fdot=(freq[len(freq)-1]-freq[0])/(end*60*60*24)
#sqr_real_time=[]
#for i in range(len(real_time)):
    #point=(real_time[i])**2
    #sqr_real_time.append(point)

#MODEL
#term3=[]
#for i in range(len(sqr_real_time)):
    #point=f_dot*sqr_real_time[i]
    #term3.append(point)
#term2=[]
#for i in range(len(real_time)):
    #point=f_p*real_time[i]
    #term2.append(point)
#term1=[start]*len(real_time)

#cycle_model=[]
#phase_model=[]
#for i in range(len(real_time)):
    #point=term1[i]+term2[i]+term3[i]
    #cycle_model.append(point)
    #point=point-int(point)
    #phase_model.append(point)

#FIT
#fdot=0.004
#f=1/0.00160731229639699

#term3=[]
#for i in range(len(sqr_real_time)):
    #point=fdot*sqr_real_time[i]
    #term3.append(point)
#term2=[]
#for i in range(len(real_time)):
    #point=f*real_time[i]
    #term2.append(point)
#term1=[start]*len(real_time)

#cycle_fit=[]
#phase_fit=[]
#for i in range(len(real_time)):
    #point=term1[i]+term2[i]+term3[i]
    #cycle_fit.append(point)
    #point=point-int(point)
    #phase_fit.append(point)

#plt.plot(real_time,phase_model,color='b')
#plt.plot(real_time,phase_fit,color='r')
#plt.xlabel("Time (mjd)")
#plt.ylabel("Phase")
#plt.savefig("PhasedArray1.png")
#plt.show()

#TOA

#TOA=[]
#for i in range(len(real_time)):
    #point=phase_model[i]*doppler_period[i]
    #TOA.append(point)

#plt.plot(TOA,phase_model)
#plt.show()
#plt.savefig("TOA Offset.png")
