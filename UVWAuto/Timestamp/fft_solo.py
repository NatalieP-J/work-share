#May 23,2013 Li Version 1.0
#May 27,2013 Li version 1.5: I made main() into a function, and this 
#will now be called from another script. to revert changes, simply remove 
#signal as a parameter

from numpy import loadtxt
from numpy import fft
from numpy import absolute
from numpy import sort
import pylab

#constants
filename = "signal1.dat"

def main():
        #Process the data See fourier.pdf in downloads folder
        #We take the magnitude of the complex number given by fft.
        #The frequency in fft's output is given by the index. (only the first half of is useful due to Nyquist's law)
	
	#read in data with numpy loadtxt or numpy genfromtxt
	#***We only need the second column, the signal strength. 
	#***first column is needed to extract number of data points and time span
	signal = loadtxt(fname = filename,delimiter = " ")
	nbData = signal[0:,0].size	

	#plotting the data just for fun
#	pylab.plot(signal[0:,0],signal[0:,1])
#	pylab.show()

	ffted = fft_do(signal[0:,1])
	freq = get_freq(signal[0:,0].size,signal[-1,0]-signal[0,0])
	
	#plotting using scipy and matplotlib
#	pylab.plot(freq[0:],ffted[0:])
#	pylab.show()	
	

	#write results to file
	#numpy has its own data types. We use repr() function to make it into string
	outfile = open("output",'w')
	for i in range(nbData):
		outfile.write(repr(freq[i])+' '+repr(ffted[i])+'\n')
	outfile.close()

	temp = sort(ffted)

def fft_do(signal):
        #takes an numpy	array containing data points and spit out the ffted
        ffted = fft.fft(signal)
	#Calculate magnitude
        ffted = absolute(ffted)

        return(ffted)

def get_freq(nbdata,timeinterval):
        #Calculating frequency. I will use fftfreq for convenience, but I tested it against the formulas given in the book and they give the same results
	spacing = (timeinterval)/float(nbdata)
	freq = fft.fftfreq(nbdata,spacing)
	return(freq)

