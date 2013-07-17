import numpy as np
import sys
import argparse
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description="Generate plag")
parser.add_argument('infile', help='file name')
parser.add_argument('ntimes', help='ntimes', type=int)
parser.add_argument('nchan', help='nchan', type=int)
parser.add_argument('nfreq', help='number of frequencies.',type=int)
parser.add_argument('ngate', help='number of gates',type=int)

args = parser.parse_args()

ntimes = args.ntimes
nchan = args.nchan
nfreq = args.nfreq
ngate = args.ngate
ncorr = nchan*(nchan+1)/2

print args.infile

def amap1(i, j, n):
    return ((2*n*i - i**2 + i) / 2) + (j - i)

def gmap(i, j, n):
    if i>j:
        return amap1(j-1, i-1, n)
    else:
        return amap1(i-1, j-1, n)

def im(i, j, nt_l=False, nt_u=False):
    if not nt_l:
        M = np.transpose(abs(getlag(gmap(i,j,nchan))))
        plt.imshow(M, extent=[0,2.5,0,1.5])
        [plt.vlines(2.5/16.*(1+i),0,1.5,color='green') for i in range(16)]
        ax = pylab.gca()
        ax.yaxis.set_visible(False)
        ax.xaxis.set_visible(False)
        pylab.show()

    elif nt_l and nt_u:
        M = np.transpose(abs(getlag2(gmap(i,j,nchan),nt_l,nt_u)))
        plt.imshow(M, extent=[0,2.5,0,1.5])
        [plt.vlines(2.5/16.*(1+i),0,1.5,color='green') for i in range(16)]
        ax = pylab.gca()
        ax.yaxis.set_visible(False)
        ax.xaxis.set_visible(False)
        pylab.show()
    else:
        print "You have a problem"

    return M

"""Reads in either all-gate or onegate visibilities"""
if ngate==16:
    f1 = np.fromfile(args.infile, dtype=np.complex64, count=(ntimes*ngate*ncorr*nfreq))
    f1 = f1.reshape((-1, ngate, ncorr, nfreq))
    favg = f1.mean(axis=1)[:, np.newaxis, :, :]
    fsub = (1.0 + 1.0 / ngate) * f1 - favg
    print fsub.shape
    del favg
elif ngate==1: 
    f1 = np.fromfile(args.infile, dtype=np.float32, count=(ntimes*ngate*ncorr*nfreq))
    fsub = f1.reshape((-1, ngate, ncorr, nfreq))
    print fsub.shape
else:
    print "Wrong number of gates"

del f1

flag1 = np.fft.fft(fsub * np.blackman(nfreq)[np.newaxis, np.newaxis, np.newaxis, :], axis=3)

getlag = lambda n: np.transpose(np.fft.fftshift(flag1[:, :, n, :], axes=[2]), axes=(1,0,2)).copy().reshape(-1, nfreq)

getlag2 = lambda n,nt_l,nt_u: np.transpose(np.fft.fftshift(flag1[nt_l:nt_u, :, n, :], axes=[2]), axes=(1,0,2)).copy().reshape(-1, nfreq)

getsub = lambda n: np.transpose(fsub[:, :, n, :], axes=(1,0,2)).copy().reshape(-1, nfreq)


