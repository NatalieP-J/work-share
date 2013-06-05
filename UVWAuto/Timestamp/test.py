import io
import struct 

infilename = '/mnt/disk3/gsbuser/EoR/xaa'

def main():
        buffer_reader = io.open(infilename,'br')
        buffer = buffer_reader.read()
	for i in range(len(buffer)):       
		text = struct.unpack_from('<s1',buffer[i])# this step unpacks the hex decimal from the buffer
		print(text[0][2])
		print(text[0][3])
main()
