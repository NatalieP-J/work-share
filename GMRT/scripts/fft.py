#May 23,2013 Li Version 1.0

from numpy import loadtxt
from numpy import fft
from numpy import absolute
from numpy import sort
import pylab

#constants
filename = "signal1.dat"
nbData = 10000

def main():
	
	#read in data with numpy loadtxt or numpy genfromtxt
	#***We only need the second column, the signal strength. 
	#***first column is needed to extract number of data points and time span
	signal = loadtxt(fname = filename,delimiter = " ")

	#plotting the data just for fun
#	pylab.plot(signal[0:,0],signal[0:,1])
#	pylab.show()

	#use numpy fft to generate the output
	ffted = fft.fft(signal[0:,1])
	
	#Process the data See fourier.pdf in downloads folder
	#We take the magnitude of the complex number given by fft.
	#The frequency in fft's output is given by the index. (only the first half of is useful due to Nyquist's law)
	
	#Calculating frequency. I will use fftfreq for convenience, but I tested it against the formulas given in the book and they give the same results
	spacing = (signal[-1,0]-signal[0,0])/float(nbData)

	print(spacing)
	freq = fft.fftfreq(nbData,spacing)
	
	#Calculating magnitude
	ffted = absolute(ffted)
	
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
	print(temp[-1])
	print(temp[-2])

main()
