from pulsar import ELL1Ephemeris
import numpy as np
c=3e8
#PSR B1957+20

#Ue-Li's information:
#May 17, 05:17 IST 
#P0=0.00160731229639699
#toa residual = (340-0.008*(i-120)^2)*P0
#i in integration times of 4.0266 seconds
P_a=0.00160731229639699 #seconds
#i=time/4.0266 #seconds - integration time
#toa_res=(340-0.008*(i-120)**2)*P_a
f_a=1./P_a
FDOTa=-2.4707e-4 #???


#ATNF information
P_b=0.00160740168480632
f_b=1./P_b
PDOTb=1.68515E-20  
FDOTb=-PDOTb/((P_b)**2)

#ephemeris.py information
P_c=0.001607401696775832
f_c=622.12202587929698
PDOTc=1.6851499999999999e-20
FDOTc=-PDOTc/((P_c)**2)

#circular motion equations
def acceleration(radius,mass):
    a=mass*(6.67e-11)/radius**2
    return a
def velocity(acceleration,radius):
    v=np.sqrt(acceleration*radius)
    return v
def c_velocity(acceleration,radius):
    v=np.sqrt(acceleration*radius)
    return v/c
def doppler(velocity,frequency):
    f=(1/(1+velocity))*frequency
    return f
def doppler_deriv(velocity,frequency,fdot):
    a=(-fdot*c/frequency)*((1+velocity/c)**2)
    return a
def c_doppler_deriv(velocity,frequency,fdot):
    a=(-fdot/frequency)*((1+velocity)**2)
    return a
def v_doppler(frequency,f_0):
    v=((f_0/frequency)-1)
    return v
Mo=2e30
AU=1.5e11
lt_s=c

a_1=acceleration(AU,Mo)
a_2=acceleration(6000000,5.972e24)
a_3=acceleration(2.676759e7,0.024777*Mo)
a_tot=(a_1+a_2+a_3)
v_1=c_velocity(a_1,AU)
v_2=-c_velocity(a_2,600000)
v_3=-c_velocity(a_3,2.676759e7)
v_tot1=(v_1+v_2+v_3)
f_check1=doppler(v_tot1,f_b)
a_checkc=c_doppler_deriv(v_tot1,f_c,FDOTc)
a_checkb=c_doppler_deriv(v_tot1,f_b,FDOTb)
a_checka=c_doppler_deriv(v_tot1,f_a,FDOTa)

v_topo=9.5356724374771848e-08
v_earth=-7.1290634749186945e-05
v_orb=-1.0343685148542651e-05
v_tot2=v_topo+v_earth+v_orb
f_check2=doppler(v_tot2,f_b)
a_checkc=c_doppler_deriv(v_tot2,f_c,FDOTc)
a_checkb=c_doppler_deriv(v_tot2,f_b,FDOTb)
a_checka=c_doppler_deriv(v_tot2,f_a,FDOTa)
