from numpy import *
from fft import fft

filename = "/mnt/disk3/gsbuser/EoR/xaa"

def main():
	data = fromfile(filename,dtype="uint8")
	actual_data = zeros(data.size*2) #after processing, because I don't know how to read less than 8 bits at a time
	
	#processing
	for i in range(data.size):
		temp = asscalar(data[i]) #convert to native python type
		temp  = convert(temp)	
		actual_data[2*i+1] = temp[0]
		actual_data[2*i+1] = temp[1]

	print(actual_data[0:10])


#because apparently the data is in single bit hexadecimal
#we read in 8 bits integer, turn it into hexadecimal, turn said hexa back
#to int, then separate the positive and the negative
#tested to work the way it's intended to

def convert(decimal):
	hexa = hex(decimal)
	dec = [int(hexa[2],16),int(hexa[3],16)]
	
	#if the telescope records up and including 7, it's positive, otherwise it's negative
	if dec[0] > 7:
		dec[0] = -1*(16-dec[0])
	if dec[1] > 7:
		dec[1] = -1*(16-dec[1])
	return dec

main()
