import sys
import numpy as np
import pylab
import matplotlib
#I have simplified the original function. Henceforth, n is the same as N-nought, and k is the same as tau. N(t)=n(e^((-t*ln2)/k))=n(e^ln2)(e^-t/k)=2n(e^-t/k), where n and k are starting conditions specified in the command line.
print """
Radioactive decay.
First column: time in seconds
Second column: number of remaining atoms
"""
n=float(sys.argv[2]) #Takes the third raw input in the command line, and changes it from a string to a float.
k=float(sys.argv[1]) #Takes the second raw input in the command line and changes it froma string to a float.
a=k*(np.log(2*n)) # We don't want time to go to infinity - we need some limiting factor. Once N is at one (one atom remaining), the sample will have almost completely decayed. If we take the original function N(t)=n(e^((-t*ln2)/k)) and solve for t when N=1, we get an 'end' time as a function of k and n. I have called it 'a' to get rid of some of the mess in my while loop.
t=0
N=n

while t<int(a):
    print t,int(N) #Since N represents the number of atoms, print the nearest integer - it doesn't make sense to have a fraction of an atom.
    t=t+k
    N=(2.*n)*(np.exp(-t/k))
print 'At times greater than this, there is only one atom or less remaining.'
