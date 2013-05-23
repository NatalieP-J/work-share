#Ellipse fitting code was modified from code found at:
# nicky.vanforeest.com/misc/fitEllipse/fitEllipse

import numpy as np
from numpy.linalg import eig, inv

#DEFINE FUNCTIONS

#fit ellipse takes a pair of points (x,y) and returns
def fitEllipse(x,y):
    x = x[:,np.newaxis] #newaxis is None returns True
    y = y[:,np.newaxis]
    D =  np.hstack((x*x, x*y, y*y, x, y, np.ones_like(x)))
#hstack takes a sequence of arrags and stacks them horizntally
    S = np.dot(D.T,D) #dot takes the dot product of two arrays
    C = np.zeros([6,6]) #zeros creates an array of zeros
    C[0,2] = C[2,0] = 2; C[1,1] = -1 #modifies C to contain non-zero values
    E, V =  eig(np.dot(inv(S), C))
 #find eigenvalues and right eigenvectors for a square array
    n = np.argmax(np.abs(E)) #index of the maximum value
    a = V[:,n]
    return a

def ellipse_center(a):
    b,c,d,f,g,a = a[1]/2, a[2], a[3]/2, a[4]/2, a[5], a[0]
    num = b*b-a*c
    x0=(c*d-b*f)/num
    y0=(a*f-b*d)/num
    return np.array([x0,y0])

def ellipse_angle_of_rotation( a ):
    b,c,d,f,g,a = a[1]/2, a[2], a[3]/2, a[4]/2, a[5], a[0]
    return 0.5*np.arctan(2*b/(a-c))

def ellipse_axis_length( a ):
    b,c,d,f,g,a = a[1]/2, a[2], a[3]/2, a[4]/2, a[5], a[0]
    up = 2*(a*f*f+c*d*d+g*b*b-2*b*d*f-a*c*g)
    down1=(b*b-a*c)*( (c-a)*np.sqrt(1+4*b*b/((a-c)*(a-c)))-(c+a))
    down2=(b*b-a*c)*( (a-c)*np.sqrt(1+4*b*b/((a-c)*(a-c)))-(c+a))
    res1=np.sqrt(up/down1)
    res2=np.sqrt(up/down2)
    return np.array([res1, res2])

points=[(-0.0381,-0.0091),(-0.0657,0.0354),(-0.0701,0.0712),(-0.0689,0.1041),(-0.0634,0.1235),(-0.0575,0.1486),(-0.0521,0.1513),(-0.0381,0.1623),(0.0356,0.1054),(0.0350,0.0532)]

dat=np.array(points)
x=dat[:, 0]
y=dat[:, 1]
R=np.arange(0,2*np.pi,0.01)

a = fitEllipse(x,y)
center = ellipse_center(a)
phi = ellipse_angle_of_rotation(a)
axes = ellipse_axis_length(a)

print "center = ",  center
print "angle of rotation = ",  phi
print "axes = ", axes

a, b = axes
xx = center[0] + a*np.cos(R)*np.cos(phi) - b*np.sin(R)*np.sin(phi)
yy = center[1] + a*np.cos(R)*np.sin(phi) + b*np.sin(R)*np.cos(phi)


from pylab import *
plot(x,y,'o')
xlim([0.1,-0.15])
ylim([-0.05,0.2])
plot(xx,yy, color = 'red')
show()


