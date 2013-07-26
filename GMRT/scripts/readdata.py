from subprocess import check_output
from subprocess import call
from numpy import empty
from numpy import zeros
from numpy import sum
from fft_solo import fft_do
from fft_solo import get_freq
import os
from numpy import around

timespan = 1/float(33333333)*1024 # because 1024 data points cover this time span?
filename = '/mnt/code/gsbuser/panli19/1919+21.pgm'

size = 1024 # we take 1024 points and fft it
nbFold = 500 # average 500 samples into one

def main():

	#readin data
	#we will read it in using linux od command then process output
	x = check_output(["od","-t","x1","/mnt/disk3/gsbuser/EoR/xaa"])
        input = x.split('\n')
#       data = zeros(len(input)*32,dtype='int8') #after process input will be stored here

	#We write out a pgm file
	width = size
	height = (len(input)-2)*32/float(size)/float(nbFold)
	fout = open(filename,'wb')
	pgmHeader = 'P5' + '\n' + str(width) + '  ' + str(height) + '  ' + str(255) + '\n'
	fout.write(pgmHeader)
	fout.close()

	k = -1 #index to keep track of when we get 1024 data points
	
	temp1024 = empty([nbFold,size],dtype='float16')
	for i in range(len(input)-2):
		
		#string processing
		temp = input[i].split(' ')
		for j in range(16):
				k = k+1
				temp1024[k/nbFold,k%size] = convert(temp[j+1][0])
				print(str(k/nbFold)+' '+str(k%size))
				k = k+1
				temp1024[k/nbFold,k%size] = convert(temp[j+1][1])
		
		#once k reaches 1023 we do fourier transformation
		if k == size*nbFold-1:
			k = -1
			toappend = getPGM(foldit(temp1024))
			os.system('echo '+toappend+' >> '+filename)	
			
			print(toappend)		
	
	if i % 81920 ==0:
			print(str(i/81920)+'0MB of data has been processed')

def convert(q):
	#convert hexadecimal into decimal. also since telescope can only read 1 digit
	#data > 8 will be converted to negative
	q = int(q,16)
        if q > 7:
                q = -1*(16-q)
        return q

	
def getPGM(temp1024):

	#input is 1024 data numpy array
	#take my array and output a line of PGM	
	ffted = fft_do(temp1024)
	
	#normalize everything to 255
	ffted = ffted/max(ffted)
	ffted = ffted*255

	#round up to integer
	ffted = around(ffted)
	
	#prepare string
	output = " " 
	for i in range(1024):
		output+=repr(ffted[i])+' '
	return(output)

def foldit(array):
	#take a matrix of size fold*size and then average each bin 
	folded = empty(1,size)
	for i in range(size):
		folded[i] = numpy.sum(folded[0:,i])
	return(array)

def createPGM(width,height,filename):
        #We write out a pgm file
#       width = size
 #      height = (len(input)-2)*32/float(size)/float(nbFold)
        fout = open(filename,'wb')
        pgmHeader = 'P5' + '\n' + str(width) + '  ' + str(height) + '  ' + str(255) + '\n'
        fout.write(pgmHeader)
        fout.close()


main()
