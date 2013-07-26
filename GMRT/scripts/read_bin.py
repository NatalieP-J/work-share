import io
import struct
from numpy import empty
from numpy import zeros
from numpy import sum
from numpy import around
from fft_solo import fft_do
from fft_solo import get_freq

outfilename = '/mnt/code/gsbuser/panli19/1919+21.pgm'
infilename = '/mnt/disk3/gsbuser/EoR/xaa'

size = 1024 # we take 1024 points and fft it
nbFold = 500 # average 500 samples into one
timespan = 1/float(33333333)*1024 # because 1024 data points cover this time span?


def main():
# them method to read in the file has been changed to buffer_reader

	#read into buffer. EAch byte contains 8 bits which packs two 4-bits hexadecimal numbers
	buffer_reader = io.open(infilename,'br')
	buffer = buffer_reader.read()
	bufSize = len(buffer)	

	#CreatePGM
	createPGM(size,bufSize/float(size)/float(nbFold),outfilename)

	#Read and process
	r = 0 #keep track of rows we want 500
	c = -1 #keep track of columns we want 1024
        temp1024 = empty([nbFold,size],dtype='float16')

	for i in range(bufSize):
	        text = struct.unpack_from('<s1',buffer[i])# this step unpacks the hex decimal from the buffer
		try:		
			c+=1
			temp1024[r,c]=convert(text[0][2])
			c+=1
			temp1024[r,c]=convert(text[0][3])
		except IndexError:
			print(text)
	
		if c%size-1 == 0:
			r+=1

		if (r+1)*(c+1) == size*nbFold-1:
                        toappend = getPGM(foldit(temp1024))
                        os.system('echo '+toappend+' >> '+outfilename)
			k = 0
			r = 0
			c = -1

		

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

def foldit(array,size):
        #take a matrix of size fold*size and then average each bin
        folded = empty(1,size)
        for i in range(size):
                folded[i] = numpy.sum(folded[0:,i])
        return(array)

def createPGM(width,height,outfilename):
        #We write out a pgm file
        fout = open(outfilename,'wb')
        pgmHeader = 'P5' + '\n' + str(width) + '  ' + str(height) + '  ' + str(255) + '\n'
        fout.write(pgmHeader)
        fout.close()

#def unpack(in):
#	text = struct.unpack_from('<s1',in)# this step unpacks the hex decimal from the buffer
#	b1 = bin(int(text[2], 16))[2:].zfill(4) #trasnlate hex into binary and fill in the zeros
#	b2 = bin(int(text[3],16)))[2:].zfill(4)
#	return([b1,b2])

def convert(q):
        #convert hexadecimal into decimal. also since telescope can only read 1 digit
        #data > 8 will be converted to negative
        q = int(q,16)
        if q > 7:
                q-=16
        return q

main()

