#unpacks the hexadecimal from buffer
def unpack(in):
        text = struct.unpack_from('<s1',in)# this step unpacks the hex decimal from the buffer
        b1 = bin(int(text[2], 16))[2:].zfill(4) #trasnlate hex into binary and fill in the zeros
        b2 = bin(int(text[3],16)))[2:].zfill(4)
        return([b1,b2])


